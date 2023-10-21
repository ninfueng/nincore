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

    factory_default = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        for k, v in self.items():
            if isinstance(v, (dict, OrderedDict, AttrDict)):
                # Recursively convert to `AttrDict`.
                self[k] = AttrDict(v)
            elif isinstance(v, (tuple, list)):
                for idx, value in enumerate(v):
                    if isinstance(value, (dict, OrderedDict, AttrDict)):
                        self[k][idx] = AttrDict(v[idx])

    def __setattr__(self, key: str, value: Any) -> None:
        self.__setitem__(key, value)

    def __delattr__(self, key: str) -> None:
        self.__delitem__(key)

    def __getattr__(self, key: str) -> Any:
        return self.__getitem__(key)

    def __missing__(self, key: str) -> None:
        """Default is `None`, what to replace with unseen keys."""
        self[key] = self.factory_default
        return self.factory_default

    def __repr__(self) -> str:
        indent = 2
        s = 'AttrDict{\n'
        for k, v in self.items():
            s += ' ' * 2
            if isinstance(v, (dict, OrderedDict, AttrDict)):
                s += f'{k}: '
                if len(v) == 0:
                    s += '{},'
                else:
                    indent += 4
                    s += self._get_dict_repr(v, indent)
                    indent -= 4
            else:
                s += f'{k}: {v},'
            s += '\n'
        s += '}'
        return s

    def _get_dict_repr(self, d: Dict[str, Any], indent: int) -> str:
        s = '{\n'
        for k, v in d.items():
            s += ' ' * indent
            if isinstance(v, (dict, OrderedDict, AttrDict)):
                indent += 2
                s += self._get_dict_repr(v, indent)
                indent -= 2
            else:
                s += f'{k}: {v},'
            s += '\n'
        s += ' ' * (indent - 2) + '},'
        return s

    def to_json(self, json_dir: str, indent: int = 4) -> None:
        assert isinstance(json_dir, str), f'Should be `str`, Your `{type(json_dir)}`.'
        assert isinstance(indent, int), f'Should be `int`, Your `{type(indent)}`.'
        json_dir = os.path.expanduser(json_dir)

        self._cvt_array_list()
        self._if_not_exist_makedirs(json_dir)
        with open(json_dir, 'w') as f:
            json.dump(self, f, indent=indent, default=lambda _: None)

    def to_yaml(self, yaml_dir: str) -> None:
        assert isinstance(yaml_dir, str), f'Should be `str`, Your `{type(yaml_dir)}`.'
        yaml_dir = os.path.expanduser(yaml_dir)

        self._cvt_array_list()
        self._if_not_exist_makedirs(yaml_dir)
        with open(yaml_dir, 'w') as f:
            yaml.dump(self, f)

    def _if_not_exist_makedirs(self, dirname: str) -> None:
        dirname = os.path.dirname(dirname)
        if dirname == '' or dirname == '.':
            return
        os.makedirs(dirname, exist_ok=True)

    def _cvt_array_list(self) -> None:
        """Converts `Tensor` and `np.ndarray` to `list` to save-able formats."""
        for k, v in self.items():
            if isinstance(v, np.ndarray):
                self[k] = v.tolist()
            elif isinstance(v, (dict, OrderedDict, AttrDict)):
                if isinstance(v, AttrDict):
                    self[k]._cvt_array_list()
                else:
                    self[k] = AttrDict(v)
                    self[k]._cvt_array_list()
            if ENABLE_TORCH:
                if isinstance(v, torch.Tensor):
                    self[k] = v.detach().cpu().numpy().tolist()


if __name__ == '__main__':
    a = AttrDict(
        a=1,
        b=[1, 2],
        c=AttrDict({'d': 3, 'e': AttrDict({'f': 4, 'h': {'h': 5, 'j': 6}}), 'g': 5}),
        k={},
        l=[],
        m=np.array([1, 2, 3]),
        n=np.array([[1, 2, 3], [4, 5, 6]]),
        o={'p': np.array([1, 2, 3]), 'q': np.array([[1, 2, 3], [4, 5, 6]])},
    )
    print(a)
    a.test = 5
    print(a)
    print(a.test2)
