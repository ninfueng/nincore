from typing import Any

__all__ = [
    'gstr',
    'ystr',
    'rstr',
    'gprint',
    'yprint',
    'rprint',
    'mgetattr',
    'msetattr',
]


# https://stackoverflow.com/questions/287871/how-do-i-print-colored-text-to-the-terminal
def gstr(s: str) -> str:
    return f'\033[32m{s}\033[0m'


def ystr(s: str) -> str:
    return f'\033[33m{s}\033[0m'


def rstr(s: str) -> str:
    return f'\033[31m{s}\033[0m'


def gprint(s: str) -> None:
    print(gstr(s))


def yprint(s: str) -> None:
    print(ystr(s))


def rprint(s: str) -> None:
    print(rstr(s))


def mgetattr(o: object, attr: str) -> Any:
    """Multi-level `getattr` allows to access recursively attribute.

    Example:
    >>> model = alexnet()
    >>> mgetattr(model, 'features.0.weight')
    """
    assert isinstance(attr, str), f'`attr` should be `str`. Your: {type(attr)}.'
    attrs = attr.split('.')

    rattr = getattr(o, attrs[0])
    for attr in attrs[1:]:
        rattr = getattr(rattr, attr)
    return rattr


def msetattr(o: object, attr: str, value: Any) -> None:
    """Multi-level `setattr` allows to modify recursively attribute.

    Example:
    >>> model = alexnet()
    >>> replace_param = nn.Parameter(torch.zeros_like(model.features[0].weight))
    >>> mgetattr(model, 'features.0.weight', replace_param)
    >>> model.features[0].weight
    """
    assert isinstance(attr, str), f'`attr` should be `str`. Your {type(attr)}.'
    attrs = attr.split('.')

    # a case without `.`.
    if len(attrs) == 1:
        setattr(o, attrs[0], value)
        return None

    rattr = getattr(o, attrs[0])
    for attr in attrs[1:-1]:
        rattr = getattr(rattr, attr)
    setattr(rattr, attrs[-1], value)
