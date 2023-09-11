from typing import Any

__all__ = [
    "gstr",
    "ystr",
    "rstr",
    "gprint",
    "yprint",
    "rprint",
    "multi_getattr",
    "multi_setattr",
]


# https://stackoverflow.com/questions/287871/how-do-i-print-colored-text-to-the-terminal
def gstr(s: str) -> str:
    return f"\033[32m{s}\033[0m"


def ystr(s: str) -> str:
    return f"\033[33m{s}\033[0m"


def rstr(s: str) -> str:
    return f"\033[31m{s}\033[0m"


def gprint(s: str) -> None:
    print(gstr(s))


def yprint(s: str) -> None:
    print(ystr(s))


def rprint(s: str) -> None:
    print(rstr(s))


def multi_getattr(obj: object, multiattr: str) -> Any:
    """Multi-level `getattr` allows for accessing multi-level.

    Example:
    >>> model = alexnet()
    >>> multi_getattr(model, "features.0.weight")
    """
    assert isinstance(multiattr, str)
    attrs = multiattr.split(".")
    recur_attr = getattr(obj, attrs[0])
    for attr in attrs[1:]:
        recur_attr = getattr(recur_attr, attr)
    return recur_attr


def multi_setattr(obj: object, multiattr: str, value: Any) -> None:
    """Multi-level `setattr` allows for accessing multi-level.

    Example:
    >>> model = alexnet()
    >>> replace_param = nn.Parameter(torch.zeros_like(model.features[0].weight))
    >>> multi_setattr(model, "features.0.weight", replace_param)
    >>> model.features[0].weight
    """
    assert isinstance(multiattr, str)
    attrs = multiattr.split(".")
    # Fixes when `multiattr` without `.`.
    if len(attrs) == 1:
        setattr(obj, attrs[0], value)
        return
    recur_attr = getattr(obj, attrs[0])
    for attr in attrs[1:-1]:
        recur_attr = getattr(recur_attr, attr)
    setattr(recur_attr, attrs[-1], value)
