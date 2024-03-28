import math
from typing import Any

__all__ = ['split_n']


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
