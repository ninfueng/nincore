import collections.abc
from itertools import repeat
from typing import Any, Callable, Tuple

__all__ = [
    "to_ntuple",
    "to_1tuple",
    "to_2tuple",
    "to_3tuple",
    "to_4tuple",
]


# https://github.com/huggingface/pytorch-image-models/blob/main/timm/layers/helpers.py
def _ntuple(n: Any) -> Callable[..., Tuple[Any, ...]]:
    def parse(x: Any) -> Tuple[Any, ...]:
        if isinstance(x, collections.abc.Iterable) and not isinstance(x, str):
            return tuple(x)
        return tuple(repeat(x, n))

    return parse


to_1tuple = _ntuple(1)
to_2tuple = _ntuple(2)
to_3tuple = _ntuple(3)
to_4tuple = _ntuple(4)
to_ntuple = _ntuple
