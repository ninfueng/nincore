import json
import os
from collections import OrderedDict
from typing import Any, Dict

import numpy as np
import yaml

try:
    import torch

    ENABLE_TORCH = True

except ImportError:
    raise


__all__ = ['AttrDict']


class AttrDict(OrderedDict):
    """Attributed OrderedDict Default (with None).

    Example:
    >>> d = AttrDict()
    >>> d.a
    >>> d = AttrDict(a=3)
    >>> d.a
    3
    >>> d2 = AttrDict(a=1, b={'a': 5, 'b': 6})
    >>> d2.b.a
    5
    """

    __slots__ = ()
    # `OrderedDict.__getitem__` causes `mypy` warnings. Using `dict` instead.
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    # Default, what to replace with unseen keys.
    factory_default = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        for key in self.keys():
            if isinstance(self[key], (OrderedDict, dict)):
                self[key] = AttrDict(self[key])

            elif isinstance(self[key], list):
                for idx, value in enumerate(self[key]):
                    if isinstance(value, dict):
                        self[key][idx] = AttrDict(self[key][idx])

    def __missing__(self, key: str) -> None:
        self[key] = self.factory_default
        return self.factory_default

    def to_json(self, json_dir: str, indent: int = 4) -> None:
        assert isinstance(json_dir, str), f'Should be `str`, your type `{type(json_dir)}`.'
        assert isinstance(indent, int), f'Should be `int`, your type `{type(indent)}`.'
        json_dir = os.path.expanduser(json_dir)

        self._cvt_array_list()
        self._not_exist_makedirs(json_dir)
        with open(json_dir, 'w') as f:
            json.dump(self, f, indent=indent, default=lambda _: None)

    def to_yaml(self, yaml_dir: str) -> None:
        assert isinstance(yaml_dir, str), f'Should be `str`, your type `{type(yaml_dir)}`.'
        yaml_dir = os.path.expanduser(yaml_dir)

        self._cvt_array_list()
        self._not_exist_makedirs(yaml_dir)
        with open(yaml_dir, 'w') as f:
            yaml.dump(self, f)

    def get_dict_repr(self, d: Dict[str, Any], indent: int) -> str:
        s = '{\n'
        for k_, v_ in d.items():
            s += ' ' * indent
            if isinstance(v_, (AttrDict, OrderedDict, dict)):
                indent += 2
                s += self.get_dict_repr(v_, indent)
                indent -= 2
            else:
                s += f'{k_}: {v_},'
            s += '\n'
        s += ' ' * (indent - 2) + '},'
        return s

    def __repr__(self) -> str:
        indent = 2
        s = 'AttrDict{\n'
        for k, v in self.items():
            s += ' ' * 2
            if isinstance(v, (AttrDict, OrderedDict, dict)):
                indent += 2
                s += self.get_dict_repr(v, indent)
                indent -= 2
            else:
                s += f'{k}: {v},'
            s += '\n'
        s += '}'
        return s

    def _not_exist_makedirs(self, dirname: str) -> None:
        dirname = os.path.dirname(dirname)
        os.makedirs(dirname, exist_ok=True)

    def _cvt_array_list(self) -> None:
        """Converts `Tensor` and `np.ndarray` to `list` to save-able formats."""
        for key, value in self.items():
            if isinstance(value, np.ndarray):
                self[key] = value.tolist()
            if ENABLE_TORCH:
                if isinstance(value, torch.Tensor):
                    tmp = value.detach().cpu().numpy()
                    self[key] = tmp.tolist()


if __name__ == '__main__':
    a = AttrDict(
        a=1,
        b=[1, 2],
        c=AttrDict({'d': 3, 'e': AttrDict({'f': 4, 'h': {'k': 5, 'x': 6}}), 'g': 5}),
    )
    print(a)
