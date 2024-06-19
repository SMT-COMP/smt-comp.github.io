from dataclasses import dataclass
import polars as pl
from rich.table import Table
import rich
from typing import *
from smtcomp import defs

U = TypeVar("U")
V = TypeVar("V")
W1 = TypeVar("W1")
W2 = TypeVar("W2")


def filter_map(f: Callable[[U], V | None], i: Iterable[U]) -> Iterable[V]:
    i2 = map(f, i)
    i3: Iterable[V | None] = filter(lambda x: x is not None, i2)
    return cast(Iterable[V], i3)


def map_none3(f: Callable[[U], V | None]) -> Callable[[Tuple[W1, W2, U]], Tuple[W1, W2, V] | None]:
    def g(x: Tuple[W1, W2, U]) -> Tuple[W1, W2, V] | None:
        y = f(x[2])
        if y is None:
            return None
        else:
            return (x[0], x[1], y)

    return g


def add_columns(dst: pl.LazyFrame, from_: pl.LazyFrame, on: list[str], defaults: Dict[str, Any]) -> pl.LazyFrame:
    dst_cols = set(dst.columns)
    from_cols = set(from_.columns)
    on_cols = set(on)
    assert on_cols.issubset(dst_cols)
    assert on_cols.issubset(from_cols)
    assert dst_cols.isdisjoint(from_cols.difference(on_cols))
    assert from_cols.difference(on_cols) == defaults.keys()
    fill_nulls = [pl.col(k).fill_null(value=v) for k, v in defaults.items()]
    return dst.join(from_, how="left", on=on, coalesce=True).with_columns(*fill_nulls)


def intersect(dst: pl.LazyFrame, from_: pl.LazyFrame, on: list[str]) -> pl.LazyFrame:
    """
    All the possible matches in the two given tables
    """
    dst_cols = set(dst.columns)
    from_cols = set(from_.columns)
    on_cols = set(on)
    assert on_cols.issubset(dst_cols)
    assert on_cols.issubset(from_cols)
    assert dst_cols.isdisjoint(from_cols.difference(on_cols))
    return dst.join(from_, how="inner", on=on, coalesce=True)


def filter_with(a: pl.LazyFrame, b: pl.LazyFrame, on: list[str]) -> pl.LazyFrame:
    return a.join(b, how="semi", on=on)


@dataclass
class Col:
    name: str
    header: str
    footer: str | Callable[[pl.DataFrame], str] | None = None
    justify: Literal["default", "left", "center", "right", "full"] = "right"
    style: str | None = None
    no_wrap: bool = False
    custom: Callable[[Any], str] = str


def rich_print_pl(title: str, df: pl.DataFrame, *cols: Col) -> None:
    """Print DataFrame of integers"""

    table = Table(title="Statistics on the benchmark selection for single query")

    for col in cols:
        table.add_column(col.header, justify=col.justify, style=col.style, no_wrap=col.no_wrap)

    for d in df.to_dicts():
        l = list(map(lambda col: col.custom(d[col.name]), cols))
        table.add_row(*l)

    table.add_section()

    def compute_footer(col: Col) -> str:
        if isinstance(col.footer, str):
            return col.footer
        elif col.footer is None:
            return str(df[col.name].sum())
        else:
            return col.footer(df)

    l = list(map(compute_footer, cols))
    table.add_row(*l)

    rich.print(table)
