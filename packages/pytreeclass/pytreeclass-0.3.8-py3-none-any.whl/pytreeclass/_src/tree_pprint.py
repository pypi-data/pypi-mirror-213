# Copyright 2023 PyTreeClass authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations

import dataclasses as dc
import functools as ft
import inspect
import math
from collections.abc import MutableMapping, MutableSequence
from itertools import chain
from types import FunctionType
from typing import Any, Callable, Iterable, Literal

import jax
import jax.tree_util as jtu
import numpy as np
from jax import custom_jvp
from jax.util import unzip2
from typing_extensions import TypedDict, Unpack

from pytreeclass._src.tree_util import (
    IsLeafType,
    Node,
    construct_tree,
    tree_leaves_with_trace,
    tree_map_with_trace,
)


class PPSpec(TypedDict):
    indent: int
    kind: Literal["REPR", "STR"]
    width: int
    depth: int | float


PyTree = Any
PP = Callable[[Any, Unpack[PPSpec]], str]
ORDER_KEY = ["B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"]
from_iterable = chain.from_iterable


def pp(node: Any, **spec: Unpack[PPSpec]) -> str:
    if spec["depth"] < 0:
        return "..."

    # avoid circular import by importing
    from pytreeclass import TreeClass

    if isinstance(node, ft.partial):
        text = f"Partial({func_pp(node.func, **spec)})"
    elif isinstance(node, (FunctionType, custom_jvp)):
        text = func_pp(node, **spec)
    elif isinstance(node, jax.ShapeDtypeStruct):
        text = shape_dtype_pp(node, **spec)
    elif isinstance(node, tuple) and hasattr(node, "_fields"):
        text = namedtuple_pp(node, **spec)
    elif isinstance(node, MutableSequence):
        text = list_pp(node, **spec)
    elif isinstance(node, tuple):
        text = tuple_pp(node, **spec)
    elif isinstance(node, set):
        text = set_pp(node, **spec)
    elif isinstance(node, MutableMapping):
        text = dict_pp(node, **spec)
    elif dc.is_dataclass(node):
        text = dataclass_pp(node, **spec)
    elif isinstance(node, TreeClass):
        text = treeclass_pp(node, **spec)
    elif isinstance(node, (np.ndarray, jax.Array)) and spec["kind"] == "REPR":
        text = numpy_pp(node, **spec)
    else:
        text = general_pp(node, **spec)

    return format_width(text, width=spec["width"])


def pps(xs: Iterable[Any], pp: PP, **spec: Unpack[PPSpec]) -> str:
    if spec["depth"] == 0:
        return "..."

    spec["indent"] += 1
    spec["depth"] -= 1

    text = (
        "\n"
        + "\t" * spec["indent"]
        + (", \n" + "\t" * spec["indent"]).join(pp(x, **spec) for x in xs)
        + "\n"
        + "\t" * (spec["indent"] - 1)
    )

    return format_width(text, width=spec["width"])


def key_value_pp(x: tuple[str, Any], **spec: Unpack[PPSpec]) -> str:
    return f"{x[0]}:{pp(x[1], **spec)}"


def attr_value_pp(x: tuple[str, Any], **spec: Unpack[PPSpec]) -> str:
    return f"{x[0]}={pp(x[1], **spec)}"


def general_pp(node: Any, **spec: Unpack[PPSpec]) -> str:
    text = f"{node!r}" if spec["kind"] == "REPR" else f"{node!s}"

    if "\n" not in text:
        return text

    return ("\n" + "\t" * (spec["indent"])).join(text.split("\n"))


def shape_dtype_pp(node: Any, **spec: Unpack[PPSpec]) -> str:
    """Pretty print a node with dtype and shape"""
    shape = f"{node.shape}".replace(",", "")
    shape = shape.replace("(", "[")
    shape = shape.replace(")", "]")
    shape = shape.replace(" ", ",")
    dtype = f"{node.dtype}".replace("int", "i")
    dtype = dtype.replace("float", "f")
    dtype = dtype.replace("complex", "c")
    return dtype + shape


def numpy_pp(node: np.ndarray | jax.Array, **spec: Unpack[PPSpec]) -> str:
    """Replace np.ndarray repr with short hand notation for type and shape"""

    base = shape_dtype_pp(node, **spec)

    if not issubclass(node.dtype.type, (np.integer, np.floating)) or node.size == 0:
        return base

    # Extended repr for numpy array, with extended information
    # this part of the function is inspired by
    # lovely-jax https://github.com/xl0/lovely-jax

    # handle interval
    low, high = np.min(node), np.max(node)
    interval = "(" if math.isinf(low) else "["
    is_integer = issubclass(node.dtype.type, np.integer)
    interval += f"{low},{high}" if is_integer else f"{low:.2f},{high:.2f}"
    interval += ")" if math.isinf(high) else "]"  # resolve closed/open interval
    interval = interval.replace("inf", "∞")  # replace inf with infinity symbol
    # handle mean and std
    mean, std = f"{np.mean(node):.2f}", f"{np.std(node):.2f}"

    return f"{base}(μ={mean}, σ={std}, ∈{interval})"


def func_pp(func: Callable, **spec: Unpack[PPSpec]) -> str:
    # Pretty print function
    # Example:
    #     >>> def example(a: int, b=1, *c, d, e=2, **f) -> str:
    #         ...
    #     >>> func_pp(example)
    #     "example(a, b, *c, d, e, **f)"
    del spec
    args, varargs, varkw, _, kwonlyargs, _, _ = inspect.getfullargspec(func)
    args = (", ".join(args)) if len(args) > 0 else ""
    varargs = ("*" + varargs) if varargs is not None else ""
    kwonlyargs = (", ".join(kwonlyargs)) if len(kwonlyargs) > 0 else ""
    varkw = ("**" + varkw) if varkw is not None else ""
    name = getattr(func, "__name__", "")
    text = f"{name}("
    text += ", ".join(item for item in [args, varargs, kwonlyargs, varkw] if item != "")
    text += ")"
    return text


def list_pp(node: list, **spec: Unpack[PPSpec]) -> str:
    return "[" + pps(node, pp=pp, **spec) + "]"


def tuple_pp(node: tuple, **spec: Unpack[PPSpec]) -> str:
    return "(" + pps(node, pp=pp, **spec) + ")"


def set_pp(node: set, **spec: Unpack[PPSpec]) -> str:
    return "{" + pps(node, pp=pp, **spec) + "}"


def dict_pp(node: dict, **spec: Unpack[PPSpec]) -> str:
    return "{" + pps(node.items(), pp=key_value_pp, **spec) + "}"


def namedtuple_pp(node: Any, **spec: Unpack[PPSpec]) -> str:
    name = type(node).__name__
    kvs = node._asdict().items()
    return name + "(" + pps(kvs, pp=attr_value_pp, **spec) + ")"


def dataclass_pp(node: Any, **spec: Unpack[PPSpec]) -> str:
    name = type(node).__name__
    kvs = ((f.name, vars(node)[f.name]) for f in dc.fields(node) if f.repr)
    return name + "(" + pps(kvs, pp=attr_value_pp, **spec) + ")"


def treeclass_pp(node: Any, **spec: Unpack[PPSpec]) -> str:
    # avoid circular import by importing here
    from pytreeclass import fields

    name = type(node).__name__
    skip = [f.name for f in fields(node) if not f.repr]
    kvs = ((k, v) for k, v in vars(node).items() if k not in skip)
    return name + "(" + pps(kvs, pp=attr_value_pp, **spec) + ")"


def type_pp(node: Any, **spec: Unpack[PPSpec]) -> str:
    if not isinstance(node, (jax.Array, np.ndarray)):
        return f"{type(node).__name__}"

    shape_dype = node.shape, node.dtype
    return pp(jax.ShapeDtypeStruct(*shape_dype), **spec)


def size_pp(size: int, **spec: Unpack[PPSpec]):
    size_order = int(math.log(size, 1024)) if size > 0 else 0
    text = f"{(size)/(1024**size_order):.2f}{ORDER_KEY[size_order]}"
    return pp(text, **spec)


def tree_repr(
    tree: PyTree,
    *,
    width: int = 80,
    tabwidth: int = 2,
    depth: int | float = float("inf"),
) -> str:
    """Prertty print arbitrary PyTrees `__repr__`

    Args:
        tree: PyTree
        width: max width of the repr string
        tabwidth: tab width of the repr string
        depth: max depth of the repr string

    Example:
        >>> import pytreeclass as pytc
        >>> import jax.numpy as jnp
        >>> tree = {'a' : 1, 'b' : [2, 3], 'c' : {'d' : 4, 'e' : 5} , 'f' : jnp.array([6, 7])}

        >>> print(pytc.tree_repr(tree, depth=0))
        {...}

        >>> print(pytc.tree_repr(tree, depth=1))
        {a:1, b:[...], c:{...}, f:i32[2](μ=6.50, σ=0.50, ∈[6,7])}

        >>> print(pytc.tree_repr(tree, depth=2))
        {a:1, b:[2, 3], c:{d:4, e:5}, f:i32[2](μ=6.50, σ=0.50, ∈[6,7])}
    """
    text = pp(tree, indent=0, kind="REPR", width=width, depth=depth)
    return text.expandtabs(tabwidth)


def tree_str(
    tree: PyTree,
    *,
    width: int = 80,
    tabwidth: int = 2,
    depth: int | float = float("inf"),
) -> str:
    """Prertty print arbitrary PyTrees `__str__`

    Args:
        tree: PyTree
        width: max width of the str string
        tabwidth: tab width of the repr string
        depth: max depth of the repr string
    Example:
        >>> import pytreeclass as pytc
        >>> import jax.numpy as jnp
        >>> tree = {'a' : 1, 'b' : [2, 3], 'c' : {'d' : 4, 'e' : 5} , 'f' : jnp.array([6, 7])}

        >>> print(pytc.tree_str(tree, depth=1))
        {a:1, b:[...], c:{...}, f:[6 7]}

        >>> print(pytc.tree_str(tree, depth=2))
        {a:1, b:[2, 3], c:{d:4, e:5}, f:[6 7]}
    """
    text = pp(tree, indent=0, kind="STR", width=width, depth=depth)
    return text.expandtabs(tabwidth)


def _is_trace_leaf_depth_factory(depth: int | float):
    # generate `is_trace_leaf` function to stop tracing at a certain `depth`
    # in essence, depth is the length of the trace entry
    def is_trace_leaf(trace) -> bool:
        # trace is a tuple of (names, leaves, tracers, aux_data)
        # done like this to ensure 4-tuple unpacking
        keys, _ = trace
        # stop tracing if depth is reached
        return False if depth is None else (depth <= len(keys))

    return is_trace_leaf


def tree_indent(
    tree: Any,
    *,
    depth: int | float = float("inf"),
    is_leaf: IsLeafType = None,
    tabwidth: int | None = 4,
):
    """Returns a string representation of the tree with indentation.

    Args:
        tree: The tree to be printed.
        depth: The maximum depth of the tree to be printed.
        is_leaf: A function that takes a node and returns True if it is a leaf node.
        tabwidth: The number of spaces per indentation level. if `None`
            then tabs are not expanded.

    Example:
        >>> import pytreeclass as pytc
        >>> tree = [1, [2, 3], [4, [5, 6]]]
        >>> print(pytc.tree_indent(tree))
        list
            [0]=1
            [1]:list
                [0]=2
                [1]=3
            [2]:list
                [0]=4
                [1]:list
                    [0]=5
                    [1]=6

    """
    smark = (" \t")[:tabwidth]  # space mark

    def step(node: Node, depth: int = 0) -> str:
        indent = smark * depth

        if (len(node.children)) == 0:
            ppspec = dict(indent=0, kind="REPR", width=80, depth=0)
            text = f"{indent}"
            (key, _), value = node.data
            text += f"{key}=" if key is not None else ""
            text += pp(value, **ppspec)
            return text + "\n"

        (key, type), _ = node.data
        text = f"{indent}"
        text += f"{key}:" if key is not None else ""
        text += f"{type.__name__}\n"

        for child in node:
            text += step(child, depth=depth + 1)
        return text

    root = construct_tree(
        tree,
        is_leaf=is_leaf,
        is_trace_leaf=_is_trace_leaf_depth_factory(depth),
    )
    text = step(root)
    return (text if tabwidth is None else text.expandtabs(tabwidth)).rstrip()


def tree_diagram(
    tree: Any,
    *,
    depth: int | float = float("inf"),
    is_leaf: IsLeafType = None,
    tabwidth: int = 4,
):
    """Pretty print arbitrary PyTrees tree with tree structure diagram.

    Args:
        tree: PyTree
        depth: depth of the tree to print. default is max depth
        is_leaf: function to determine if a node is a leaf. default is None

    Example:
        >>> import pytreeclass as pytc
        >>> class A(pytc.TreeClass):
        ...        x: int = 10
        ...        y: int = (20,30)
        ...        z: int = 40

        >>> class B(pytc.TreeClass):
        ...     a: int = 10
        ...     b: tuple = (20,30, A())

        >>> print(pytc.tree_diagram(B(), depth=0))
        B(...)

        >>> print(pytc.tree_diagram(B(), depth=1))
        B
        ├── .a=10
        └── .b=(...)


        >>> print(pytc.tree_diagram(B(), depth=2))
        B
        ├── .a=10
        └── .b:tuple
            ├── [0]=20
            ├── [1]=30
            └── [2]=A(...)
    """
    vmark = ("│\t")[:tabwidth]  # vertical mark
    lmark = ("└" + "─" * (tabwidth - 2) + (" \t"))[:tabwidth]  # last mark
    cmark = ("├" + "─" * (tabwidth - 2) + (" \t"))[:tabwidth]  # connector mark
    smark = (" \t")[:tabwidth]  # space mark

    def step(
        node: Node,
        depth: int = 0,
        is_last: bool = False,
        is_lasts: tuple[bool, ...] = (),
    ) -> str:
        indent = "".join(smark if is_last else vmark for is_last in is_lasts[:-1])
        branch = (lmark if is_last else cmark) if depth > 0 else ""

        if (child_count := len(node.children)) == 0:
            ppspec = dict(indent=0, kind="REPR", width=80, depth=0)
            (key, _), value = node.data
            text = f"{indent}"
            text += f"{branch}{key}=" if key is not None else ""
            text += pp(value, **ppspec)
            return text + "\n"

        (key, type), _ = node.data

        text = f"{indent}{branch}"
        text += f"{key}:" if key is not None else ""
        text += f"{type.__name__}\n"

        for i, child in enumerate(node.children.values()):
            text += step(
                child,
                depth=depth + 1,
                is_last=(i == child_count - 1),
                is_lasts=is_lasts + (i == child_count - 1,),
            )
        return text

    root = construct_tree(
        tree,
        is_leaf=is_leaf,
        is_trace_leaf=_is_trace_leaf_depth_factory(depth),
    )
    text = step(root, is_last=len(root.children) == 1)
    return (text if tabwidth is None else text.expandtabs(tabwidth)).rstrip()


def tree_mermaid(
    tree: PyTree,
    depth: int | float = float("inf"),
    is_leaf: IsLeafType = None,
    tabwidth: int | None = 4,
) -> str:
    """generate a mermaid diagram syntax for arbitrary PyTrees.

    Args:
        tree: PyTree
        depth: depth of the tree to print. default is max depth
        is_leaf: function to determine if a node is a leaf. default is None
    """

    def step(node: Node, depth: int = 0) -> str:
        if len(node.children) == 0:
            ppspec = dict(indent=0, kind="REPR", width=80, depth=0)
            key, _, value = node.data
            text = f"{key}=" if key is not None else ""
            text += pp(value, **ppspec)
            text = "<b>" + text + "</b>"
            return f'\tid{id(node.parent)} --- id{id(node)}("{text}")\n'

        key, type, _ = node.data
        text = f"{key}:" if key is not None else ""
        text += f"{type.__name__}"
        text = "<b>" + text + "</b>"

        if node.parent is None:
            text = f'\tid{id(node)}("{text}")\n'
        else:
            text = f'\tid{id(node.parent)} --- id{id(node)}("{text}")\n'

        for child in node.children.values():
            text += step(child, depth=depth + 1)
        return text

    root = construct_tree(
        tree,
        is_leaf=is_leaf,
        is_trace_leaf=_is_trace_leaf_depth_factory(depth),
    )
    text = "flowchart LR\n" + step(root)

    return (text.expandtabs(tabwidth) if tabwidth is not None else text).rstrip()


def format_width(string, width=60):
    """strip newline/tab characters if less than max width"""
    children_length = len(string) - string.count("\n") - string.count("\t")
    if children_length > width:
        return string
    return string.replace("\n", "").replace("\t", "")


def _calculate_count(leaf: Any) -> tuple[int, int]:
    if hasattr(leaf, "shape") and hasattr(leaf, "nbytes"):
        return int(np.array(leaf.shape).prod())
    return 1


# table printing


def _hbox(*text) -> str:
    # Create horizontally stacked text boxes
    # Examples:
    #     >>> _hbox("a","b")
    #     ┌─┬─┐
    #     │a│b│
    #     └─┴─┘

    boxes = list(map(_vbox, text))
    boxes = [(box).split("\n") for box in boxes]
    max_col_height = max([len(b) for b in boxes])
    boxes = [b + [" " * len(b[0])] * (max_col_height - len(b)) for b in boxes]
    return "\n".join([_resolve_line(line) for line in zip(*boxes)])


def _vbox(*text) -> str:
    # Create vertically stacked text boxes
    # Example:
    #     >>> _vbox("a","b")
    #     ┌───┐
    #     │a  │
    #     ├───┤
    #     │b  │
    #     └───┘

    #     >>> _vbox("a","","a")
    #     ┌───┐
    #     │a  │
    #     ├───┤
    #     │   │
    #     ├───┤
    #     │a  │
    #     └───┘

    max_width = (
        max(from_iterable([[len(t) for t in item.split("\n")] for item in text])) + 0
    )

    top = f"┌{'─'*max_width}┐"
    line = f"├{'─'*max_width}┤"
    side = [
        "\n".join([f"│{t}{' '*(max_width-len(t))}│" for t in item.split("\n")])
        for item in text
    ]

    btm = f"└{'─'*max_width}┘"

    text = ""

    for i, s in enumerate(side):
        if i == 0:
            text += f"{top}\n{s}\n{line if len(side)>1 else btm}"

        elif i == len(side) - 1:
            text += f"\n{s}\n{btm}"

        else:
            text += f"\n{s}\n{line}"

    return text


def _hstack(*boxes):
    # Create horizontally stacked text boxes
    # Example:
    #     >>> print(_hstack(_hbox("a"),_vbox("b","c")))
    #     ┌─┬─┐
    #     │a│b│
    #     └─┼─┤
    #       │c│
    #       └─┘

    boxes = [(box).split("\n") for box in boxes]
    max_col_height = max([len(b) for b in boxes])
    # expand height of each col before merging
    boxes = [b + [" " * len(b[0])] * (max_col_height - len(b)) for b in boxes]
    text = ""

    _cells = tuple(zip(*boxes))

    for i, line in enumerate(_cells):
        text += _resolve_line(line) + ("\n" if i != (len(_cells) - 1) else "")

    return text


def _resolve_line(cols: list[str]) -> str:
    # Combine columns of single line by merging their borders

    # Args:
    #     cols (Sequence[str,...]): Sequence of single line column string

    # Returns:
    #     str: resolved column string

    # Example:
    #     >>> _resolve_line(['ab','b│','│c'])
    #     'abb│c'

    #     >>> _resolve_line(['ab','b┐','┌c'])
    #     'abb┬c'

    cols = list(map(list, cols))  # convert each col to col of chars
    alpha = ["│", "┌", "┐", "└", "┘", "┤", "├"]

    for index in range(len(cols) - 1):
        if cols[index][-1] == "┐" and cols[index + 1][0] in ["┌", "─"]:
            cols[index][-1] = "┬"
            cols[index + 1].pop(0)

        elif cols[index][-1] == "┘" and cols[index + 1][0] in ["└", "─"]:
            cols[index][-1] = "┴"
            cols[index + 1].pop(0)

        elif cols[index][-1] == "┤" and cols[index + 1][0] in ["├", "─", "└"]:  #
            cols[index][-1] = "┼"
            cols[index + 1].pop(0)

        elif cols[index][-1] in ["┘", "┐", "─"] and cols[index + 1][0] in ["├"]:
            cols[index][-1] = "┼"
            cols[index + 1].pop(0)

        elif cols[index][-1] == " ":
            cols[index].pop()

        elif cols[index][-1] in alpha and cols[index + 1][0] in [*alpha, " "]:
            cols[index + 1].pop(0)

    return "".join(map(lambda x: "".join(x), cols))


def _table(rows: list[list[str]], transpose: bool = False) -> str:
    # Create a table with self aligning rows and cols

    # Args:
    #     rows: list of lists of row values
    #     transpose: transpose the table. i.e. rows become cols and cols become rows

    # Returns:
    #     str: box string

    # Example:
    #     >>> col1 = ['1\n','2']
    #     >>> col2 = ['3','4000']
    #     >>> print(_table([col1,col2]))
    #     ┌─┬────────┐
    #     │1│3       │
    #     │ │        │
    #     ├─┼────────┤
    #     │2│40000000│
    #     └─┴────────┘

    cols = rows if transpose else [list(c) for c in zip(*rows)]

    for i, _cells in enumerate(zip(*cols)):
        max_cell_height = max(map(lambda x: x.count("\n"), _cells))
        for j in range(len(_cells)):
            cols[j][i] += "\n" * (max_cell_height - cols[j][i].count("\n"))

    return _hstack(*(_vbox(*col) for col in cols))


def tree_summary(
    tree: PyTree,
    *,
    depth: int | float = float("inf"),
    is_leaf: IsLeafType = None,
) -> str:
    """Print a summary of an arbitrary PyTree.

    Args:
        tree: a jax registered pytree to summarize.
        depth: max depth to traverse the tree. defaults to maximum depth.
        is_leaf: function to determine if a node is a leaf. defaults to None

    Returns:
        String summary of the tree structure
        - First column: path to the node
        - Second column: type of the node
        - Third column: number of leaves in the node
        - Last row: type of parent, number of leaves of the parent

    Note:
        Array elements are considered as leaves, for example:
        `jnp.array([1,2,3])` has 3 leaves

    Example:
        >>> import pytreeclass as pytc
        >>> print(pytc.tree_summary([1,[2,[3]]]))
        ┌─────────┬────┬─────┐
        │Name     │Type│Count│
        ├─────────┼────┼─────┤
        │[0]      │int │1    │
        ├─────────┼────┼─────┤
        │[1][0]   │int │1    │
        ├─────────┼────┼─────┤
        │[1][1][0]│int │1    │
        ├─────────┼────┼─────┤
        │Σ        │list│3    │
        └─────────┴────┴─────┘
    """
    ROWS = [["Name", "Type", "Count"]]
    COUNT = 0

    # use `unzip2` from `jax.util` to avoid [] leaves
    # based on this issue:
    traces, leaves = unzip2(
        tree_leaves_with_trace(
            tree,
            is_leaf=is_leaf,
            is_trace_leaf=_is_trace_leaf_depth_factory(depth),
        )
    )

    for trace, leaf in zip(traces, leaves):
        count = _calculate_count(leaf)
        COUNT += count

        if trace == ((), ()):
            # avoid printing the leaf trace (which is the root of the tree)
            # twice, once as a leaf and once as the root at the end
            continue

        paths = jtu.keystr(trace[0])
        types = type_pp(leaf, indent=0, kind="STR", width=60, depth=depth)
        counts = f"{count:,}"
        ROWS += [[paths, types, counts]]

    paths = "Σ"
    types = type_pp(tree, indent=0, kind="STR", width=60, depth=depth)
    counts = f"{COUNT:,}"
    ROWS += [[paths, types, counts]]
    return _table(ROWS)


def tree_repr_with_trace(
    tree: PyTree,
    is_leaf: IsLeafType = None,
    transpose: bool = False,
) -> PyTree:
    """
    Return a PyTree with the same structure, but with the leaves replaced
    by a summary of the trace.

    Args:
        tree: pytree to summarize.
        is_leaf: function to determine if a node is a leaf. defaults to None
        transpose: transpose the table. i.e. rows become cols and cols become rows

    Example:
        >>> import pytreeclass as pytc
        >>> class Test(pytc.TreeClass):
        ...    a:int = 1
        ...    b:float = 2.0

        >>> tree = Test()
        >>> print(pytc.tree_repr_with_trace(Test()))  # doctest: +NORMALIZE_WHITESPACE
        Test(
          a=
            ┌─────────┬───┐
            │Value    │1  │
            ├─────────┼───┤
            │Name path│.a │
            ├─────────┼───┤
            │Type path│int│
            └─────────┴───┘,
          b=
            ┌─────────┬─────┐
            │Value    │2.0  │
            ├─────────┼─────┤
            │Name path│.b   │
            ├─────────┼─────┤
            │Type path│float│
            └─────────┴─────┘
        )

        >>> print(pytc.tree_repr_with_trace(Test(), transpose=True)) # doctest: +NORMALIZE_WHITESPACE
        Test(
          a=
            ┌─────┬─────────┬─────────┐
            │Value│Name path│Type path│
            ├─────┼─────────┼─────────┤
            │1    │.a       │int      │
            └─────┴─────────┴─────────┘,
          b=
            ┌─────┬─────────┬─────────┐
            │Value│Name path│Type path│
            ├─────┼─────────┼─────────┤
            │2.0  │.b       │float    │
            └─────┴─────────┴─────────┘
        )

    Note:
        This function can be useful for debugging and raising descriptive errors.
    """

    def leaf_trace_summary(trace, leaf) -> str:
        # this can be useful in debugging and raising descriptive errors

        ROWS = [["Value", tree_repr(leaf)]]

        names = "->".join(str(i) for i in trace[0])
        ROWS += [["Name path", names]]

        types = "->".join(i.__name__ for i in trace[1])
        ROWS += [["Type path", types]]

        # make a pretty table for each leaf
        return "\n\t" + ("\n\t").join(_table(ROWS, transpose=transpose).split("\n"))

    return tree_map_with_trace(leaf_trace_summary, tree, is_leaf=is_leaf)
