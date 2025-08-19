import math
from typing import Any, Sequence

__all__ = ['split_n', 'is_incremental']


def is_incremental(x: Sequence[Any]) -> bool:
    """whether a sequence x in incremental format or x[0] < x[1] < x[2] < ...

    Example:
    >>> is_incremental([1, 2, 3, 4])
    True
    >>> is_incremental([1, 2, 1, 4])
    False
    """
    return all(x[i] < x[i + 1] for i in range(len(x) - 1))


def split_n(x: list[Any], n: int) -> list[list[Any]]:
    """Split a list into n-sized chunks. The last chunk may be smaller than n.

    Args:
        x: a list to split
        n: size of chunks

    Returns:
        a list of n-sized lists.

    Example:
    >>> split_n([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 3)
    [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10]]
    """
    return [x[n * i : n * (i + 1)] for i in range(math.ceil(len(x) / n))]
