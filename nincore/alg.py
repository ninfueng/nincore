import math
from typing import Any, List

__all__ = ['split_n']


def split_n(x: List[Any], n: int) -> List[List[Any]]:
    """Split a list into n-sized chunks. The last chunk may be smaller than n.

    Args:
        x: a list to split
        n: size of chunks

    Returns:
        a list of n-sized lists.
    """
    return [x[n * i : n * (i + 1)] for i in range(math.ceil(len(x) / n))]
