from typing import *

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
