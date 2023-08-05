import itertools
import logging
import operator

import dask.dataframe as dd
import numpy as np
from dask.blockwise import Blockwise
from dask.highlevelgraph import HighLevelGraph, MaterializedLayer
from dask.layers import DataFrameIOLayer
from dask.utils import M, apply, is_arraylike

from dask_sql._compat import PQ_IS_SUPPORT, PQ_NOT_IN_SUPPORT

logger = logging.getLogger(__name__)


def attempt_predicate_pushdown(ddf: dd.DataFrame) -> dd.DataFrame:
    """Use graph information to update IO-level filters

    The original `ddf` will be returned if/when the
    predicate-pushdown optimization fails.

    This is a special optimization that must be called
    eagerly on a DataFrame collection when filters are
    applied. The "eager" requirement for this optimization
    is due to the fact that `npartitions` and `divisions`
    may change when this optimization is applied (invalidating
    npartition/divisions-specific logic in following Layers).
    """

    # Check that we have a supported `ddf` object
    if not isinstance(ddf, dd.DataFrame):
        raise ValueError(
            f"Predicate pushdown optimization skipped. Type {type(ddf)} "
            f"does not support predicate pushdown."
        )
    elif not isinstance(ddf.dask, HighLevelGraph):
        logger.warning(
            f"Predicate pushdown optimization skipped. Graph must be "
            f"a HighLevelGraph object (got {type(ddf.dask)})."
        )
        return ddf

    # We were able to extract a DNF filter expression.
    # Check that we have a single IO layer with `filters` support
    io_layer = []
    for k, v in ddf.dask.layers.items():
        if isinstance(v, DataFrameIOLayer):
            io_layer.append(k)
            creation_info = (
                (v.creation_info or {}) if hasattr(v, "creation_info") else {}
            )
            if (
                "filters" not in creation_info.get("kwargs", {})
                or creation_info["kwargs"]["filters"] is not None
            ):
                # No filters support, or filters is already set
                return ddf
    if len(io_layer) != 1:
        # Not a single IO layer
        return ddf
    io_layer = io_layer.pop()

    # Bail if any filters are already present in ddf
    existing_filters = (
        ddf.dask.layers[io_layer].creation_info.get("kwargs", {}).get("filters")
    )
    if existing_filters:
        return ddf

    # Start by converting the HLG to a `RegenerableGraph`.
    # Succeeding here means that all layers in the graph
    # are regenerable.
    try:
        dsk = RegenerableGraph.from_hlg(ddf.dask)
    except (ValueError, TypeError):
        logger.warning(
            "Predicate pushdown optimization skipped. One or more "
            "layers in the HighLevelGraph was not 'regenerable'."
        )
        return ddf

    # Extract a DNF-formatted filter expression
    name = ddf._name
    try:
        filters = dsk.layers[name]._dnf_filter_expression(dsk)
        if not isinstance(filters, frozenset):
            # No filters encountered
            return ddf
        filters = filters.to_list_tuple()
    except (ValueError, TypeError):
        # DNF dispatching failed for 1+ layers
        logger.warning(
            "Predicate pushdown optimization skipped. One or more "
            "layers has an unknown filter expression."
        )
        return ddf

    # Regenerate collection with filtered IO layer
    try:
        return dsk.layers[name]._regenerate_collection(
            dsk,
            # TODO: shouldn't need to specify index=False after dask#9661 is merged
            new_kwargs={io_layer: {"filters": filters, "index": False}},
        )
    except ValueError as err:
        # Most-likely failed to apply filters in read_parquet.
        # We can just bail on predicate pushdown, but we also
        # raise a warning to encourage the user to file an issue.
        logger.warning(
            f"Predicate pushdown failed to apply filters: {filters}. "
            f"Please open a bug report at "
            f"https://github.com/dask-contrib/dask-sql/issues/new/choose "
            f"and include the following error message: {err}"
        )

        return ddf


class Or(frozenset):
    """Helper class for 'OR' expressions"""

    def to_list_tuple(self):
        # NDF "or" is List[List[Tuple]]
        def _maybe_list(val):
            if isinstance(val, tuple) and val and isinstance(val[0], (tuple, list)):
                return list(val)
            return [val]

        return [
            _maybe_list(val.to_list_tuple())
            if hasattr(val, "to_list_tuple")
            else _maybe_list(val)
            for val in self
        ]


class And(frozenset):
    """Helper class for 'AND' expressions"""

    def to_list_tuple(self):
        # NDF "and" is List[Tuple]
        return tuple(
            val.to_list_tuple() if hasattr(val, "to_list_tuple") else val
            for val in self
        )


def to_dnf(expr):
    """Normalize a boolean filter expression to disjunctive normal form (DNF)"""

    # Credit: https://stackoverflow.com/a/58372345
    if not isinstance(expr, (Or, And)):
        if not isinstance(expr, tuple):
            raise TypeError(f"expected tuple, got {expr}")
        result = Or((And((expr,)),))
    elif isinstance(expr, Or):
        result = Or(se for e in expr for se in to_dnf(e))
    elif isinstance(expr, And):
        total = []
        for c in itertools.product(*[to_dnf(e) for e in expr]):
            conjunction = [se for e in c for se in e if isinstance(se, tuple)]
            total.append(And(conjunction))
        result = Or(total)
    return result


# Define all supported comparison functions
# (and their mapping to a string expression)
_comparison_symbols = {
    operator.eq: "==",
    operator.ne: "!=",
    operator.lt: "<",
    operator.le: "<=",
    operator.gt: ">",
    operator.ge: ">=",
    np.greater: ">",
    np.greater_equal: ">=",
    np.less: "<",
    np.less_equal: "<=",
    np.equal: "==",
    np.not_equal: "!=",
}

# Define all regenerable "pass-through" ops
# that do not affect filters.
_pass_through_ops = {M.fillna, M.astype}

# Define set of all "regenerable" operations.
# Predicate pushdown is supported for graphs
# comprised of `Blockwise` layers based on these
# operations
_regenerable_ops = (
    set(_comparison_symbols.keys())
    | {
        operator.and_,
        operator.or_,
        operator.getitem,
        operator.inv,
        M.isin,
        M.isna,
    }
    | _pass_through_ops
)

# Specify functions that must be generated with
# a different API at the dataframe-collection level
_special_op_mappings = {
    M.fillna: dd._Frame.fillna,
    M.isin: dd._Frame.isin,
    M.isna: dd._Frame.isna,
    M.astype: dd._Frame.astype,
}

# Convert _pass_through_ops to respect "special" mappings
_pass_through_ops = {_special_op_mappings.get(op, op) for op in _pass_through_ops}


def _preprocess_layers(input_layers):
    # NOTE: This is a Layer-specific work-around to deal with
    # the fact that `dd._Frame.isin(values)` will add a distinct
    # `MaterializedLayer` for the `values` argument.
    # See: https://github.com/dask-contrib/dask-sql/issues/607
    skip = set()
    layers = input_layers.copy()
    for key, layer in layers.items():
        if key.startswith("isin-") and isinstance(layer, Blockwise):
            indices = list(layer.indices)
            for i, (k, ind) in enumerate(layer.indices):
                if (
                    ind is None
                    and isinstance(layers.get(k), MaterializedLayer)
                    and isinstance(layers[k].get(k), (np.ndarray, tuple))
                ):
                    # Replace `indices[i]` with a literal value and
                    # make sure we skip the `MaterializedLayer` that
                    # we are now fusing into the `isin`
                    value = layers[k][k]
                    value = value[0](*value[1:]) if callable(value[0]) else value
                    indices[i] = (value, None)
                    skip.add(k)
            layer.indices = tuple(indices)
    return {k: v for k, v in layers.items() if k not in skip}


class RegenerableLayer:
    """Regenerable Layer

    Wraps ``dask.highlevelgraph.Blockwise`` to ensure that a
    ``creation_info`` attribute  is defined. This class
    also defines the necessary methods for recursive
    layer regeneration and filter-expression generation.
    """

    def __init__(self, layer, creation_info):
        self.layer = layer  # Original Blockwise layer reference
        self.creation_info = creation_info

    def _regenerate_collection(
        self,
        dsk,
        new_kwargs: dict = None,
        _regen_cache: dict = None,
    ):
        """Regenerate a Dask collection for this layer using the
        provided inputs and key-word arguments
        """

        # Return regenerated layer if the work was
        # already done
        _regen_cache = _regen_cache or {}
        if self.layer.output in _regen_cache:
            return _regen_cache[self.layer.output]

        # Recursively generate necessary inputs to
        # this layer to generate the collection
        inputs = []
        for key, ind in self.layer.indices:
            if ind is None:
                if isinstance(key, (str, tuple)) and key in dsk.layers:
                    continue
                inputs.append(key)
            elif key in self.layer.io_deps:
                continue
            else:
                inputs.append(
                    dsk.layers[key]._regenerate_collection(
                        dsk,
                        new_kwargs=new_kwargs,
                        _regen_cache=_regen_cache,
                    )
                )

        # Extract the callable func and key-word args.
        # Then return a regenerated collection
        func = self.creation_info.get("func", None)
        if func is None:
            raise ValueError(
                "`_regenerate_collection` failed. "
                "Not all HLG layers are regenerable."
            )
        regen_args = self.creation_info.get("args", [])
        regen_kwargs = self.creation_info.get("kwargs", {}).copy()
        regen_kwargs = {k: v for k, v in self.creation_info.get("kwargs", {}).items()}
        regen_kwargs.update((new_kwargs or {}).get(self.layer.output, {}))
        result = func(*inputs, *regen_args, **regen_kwargs)
        _regen_cache[self.layer.output] = result
        return result

    def _dnf_filter_expression(self, dsk):
        """Return a DNF-formatted filter expression for the
        graph terminating at this layer
        """
        op = self.creation_info["func"]
        if op in _comparison_symbols.keys():
            func = _blockwise_comparison_dnf
        elif op in (operator.and_, operator.or_):
            func = _blockwise_logical_dnf
        elif op == operator.getitem:
            func = _blockwise_getitem_dnf
        elif op == dd._Frame.isin:
            func = _blockwise_isin_dnf
        elif op == dd._Frame.isna:
            func = _blockwise_isna_dnf
        elif op == operator.inv:
            func = _blockwise_inv_dnf
        elif op in _pass_through_ops:
            func = _blockwise_pass_through_dnf
        else:
            raise ValueError(f"No DNF expression for {op}")

        return func(op, self.layer.indices, dsk)


class RegenerableGraph:
    """Regenerable Graph

    This class is similar to ``dask.highlevelgraph.HighLevelGraph``.
    However, all layers in a ``RegenerableGraph`` graph must be
    ``RegenerableLayer`` objects (which wrap ``Blockwise`` layers).
    """

    def __init__(self, layers: dict):
        self.layers = layers

    @classmethod
    def from_hlg(cls, hlg: HighLevelGraph):
        """Construct a ``RegenerableGraph`` from a ``HighLevelGraph``"""

        if not isinstance(hlg, HighLevelGraph):
            raise TypeError(f"Expected HighLevelGraph, got {type(hlg)}")

        _layers = {}
        for key, layer in _preprocess_layers(hlg.layers).items():
            regenerable_layer = None
            if isinstance(layer, DataFrameIOLayer):
                regenerable_layer = RegenerableLayer(layer, layer.creation_info or {})
            elif isinstance(layer, Blockwise):
                tasks = list(layer.dsk.values())
                if len(tasks) == 1 and tasks[0]:
                    kwargs = {}
                    if tasks[0][0] == apply:
                        op = tasks[0][1]
                        options = tasks[0][3]
                        if isinstance(options, dict):
                            kwargs = options
                        elif (
                            isinstance(options, tuple)
                            and options
                            and callable(options[0])
                        ):
                            kwargs = options[0](*options[1:])
                    else:
                        op = tasks[0][0]
                    if op in _regenerable_ops:
                        regenerable_layer = RegenerableLayer(
                            layer,
                            {
                                "func": _special_op_mappings.get(op, op),
                                "kwargs": kwargs,
                            },
                        )

            if regenerable_layer is None:
                raise ValueError(f"Graph contains non-regenerable layer: {layer}")

            _layers[key] = regenerable_layer

        return RegenerableGraph(_layers)


def _get_blockwise_input(input_index, indices: list, dsk: RegenerableGraph):
    # Simple utility to get the required input expressions
    # for a Blockwise layer (using indices)
    key = indices[input_index][0]
    if indices[input_index][1] is None:
        return key
    return dsk.layers[key]._dnf_filter_expression(dsk)


def _inv(symbol: str):
    if symbol == "in" and not PQ_NOT_IN_SUPPORT:
        raise ValueError("This version of dask does not support 'not in'")
    return {
        ">": "<",
        "<": ">",
        ">=": "<=",
        "<=": ">=",
        "in": "not in",
        "not in": "in",
        "is": "is not",
        "is not": "is",
    }.get(symbol, symbol)


def _blockwise_comparison_dnf(op, indices: list, dsk: RegenerableGraph):
    # Return DNF expression pattern for a simple comparison
    left = _get_blockwise_input(0, indices, dsk)
    right = _get_blockwise_input(1, indices, dsk)

    if is_arraylike(left) and hasattr(left, "item") and left.size == 1:
        left = left.item()
        # Need inverse comparison in read_parquet
        return to_dnf((right, _inv(_comparison_symbols[op]), left))
    if is_arraylike(right) and hasattr(right, "item") and right.size == 1:
        right = right.item()
    return to_dnf((left, _comparison_symbols[op], right))


def _blockwise_logical_dnf(op, indices: list, dsk: RegenerableGraph):
    # Return DNF expression pattern for logical "and" or "or"
    left = _get_blockwise_input(0, indices, dsk)
    right = _get_blockwise_input(1, indices, dsk)

    vals = []
    for val in [left, right]:
        if not isinstance(val, (tuple, Or, And)):
            raise TypeError(f"Invalid logical operand: {val}")
        vals.append(to_dnf(val))

    if op == operator.or_:
        return to_dnf(Or(vals))
    elif op == operator.and_:
        return to_dnf(And(vals))
    else:
        raise ValueError


def _blockwise_getitem_dnf(op, indices: list, dsk: RegenerableGraph):
    # Return dnf of key (selected by getitem)
    key = _get_blockwise_input(1, indices, dsk)
    return key


def _blockwise_pass_through_dnf(op, indices: list, dsk: RegenerableGraph):
    # Return dnf of input collection
    return _get_blockwise_input(0, indices, dsk)


def _blockwise_isin_dnf(op, indices: list, dsk: RegenerableGraph):
    # Return DNF expression pattern for a simple "in" comparison
    left = _get_blockwise_input(0, indices, dsk)
    right = _get_blockwise_input(1, indices, dsk)
    return to_dnf((left, "in", tuple(right)))


def _blockwise_isna_dnf(op, indices: list, dsk: RegenerableGraph):
    # Return DNF expression pattern for `isna`
    if not PQ_IS_SUPPORT:
        raise ValueError("This version of dask does not support 'is' predicates.")
    left = _get_blockwise_input(0, indices, dsk)
    return to_dnf((left, "is", None))


def _blockwise_inv_dnf(op, indices: list, dsk: RegenerableGraph):
    # Return DNF expression pattern for the inverse of a comparison
    expr = _get_blockwise_input(0, indices, dsk).to_list_tuple()
    new_expr = []
    count = 0
    for conjunction in expr:
        new_conjunction = []
        for col, op, val in conjunction:
            count += 1
            new_conjunction.append((col, _inv(op), val))
        new_expr.append(And(new_conjunction))
    if count > 1:
        # Havent taken the time to think through
        # general inversion yet.
        raise ValueError("inv(DNF) case not implemented.")
    return to_dnf(Or(new_expr))
