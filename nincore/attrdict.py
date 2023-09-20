import json
import os
from collections import OrderedDict
from typing import Any

try:
    import tomli_w
except ImportError:
    pass

try:
    import yaml
except ImportError:
    pass

enable_cvt_np = False
enable_cvt_torch = False
try:
    import numpy as np

    enable_cvt_np = True
except ImportError:
    pass

try:
    import torch

    enable_cvt_torch = True
except ImportError:
    pass

__all__ = ["AttrDict"]


# TODO: make __repr__ better


class AttrDict(OrderedDict):
    """Attributed OrderedDict Default (with None).

    Example:
    >>> d = AttrDict()
    >>> d.a
    >>> d = AttrDict(a=3)
    >>> d.a
    3
    >>> d2 = AttrDict(a=1, b={"a": 5, "b": 6})
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
            if isinstance(self[key], dict):
                self[key] = AttrDict(self[key])
            elif isinstance(self[key], list):
                for idx, value in enumerate(self[key]):
                    if isinstance(value, dict):
                        self[key][idx] = AttrDict(self[key][idx])

    def __missing__(self, key: str) -> None:
        self[key] = self.factory_default
        return self.factory_default

    def to_json(self, json_dir: str, indent: int = 4) -> None:
        assert isinstance(json_dir, str), f"Should be `str`, your type `{type(json_dir)}`."
        assert isinstance(indent, int), f"Should be `int`, your type `{type(indent)}`."
        json_dir = os.path.expanduser(json_dir)

        self._cvt_array_list()
        self._not_exist_makedirs(json_dir)
        with open(json_dir, "w") as f:
            json.dump(self, f, indent=indent, default=lambda _: None)

    def to_yaml(self, yaml_dir: str) -> None:
        assert isinstance(yaml_dir, str), f"Should be `str`, your type `{type(yaml_dir)}`."
        yaml_dir = os.path.expanduser(yaml_dir)

        self._cvt_array_list()
        self._not_exist_makedirs(yaml_dir)
        with open(yaml_dir, "w") as f:
            yaml.dump(self, f)

    def to_toml(self, toml_dir: str) -> None:
        assert isinstance(toml_dir, str), f"Should be `str`, your type `{type(toml_dir)}`."
        toml_dir = os.path.expanduser(toml_dir)

        self._cvt_array_list()
        self._not_exist_makedirs(toml_dir)
        with open(toml_dir, "wb") as f:
            tomli_w.dump(self, f)

    def _not_exist_makedirs(self, dirname: str) -> None:
        dirname = os.path.dirname(dirname)
        os.makedirs(dirname, exist_ok=True)

    def _cvt_array_list(self) -> None:
        """Converts `Tensor` and `np.ndarray` to `list` to save-able formats."""
        for key, value in self.items():
            if enable_cvt_torch:
                if isinstance(value, torch.Tensor):
                    tmp = value.detach().cpu().numpy()
                    self[key] = tmp.tolist()
            if enable_cvt_np:
                if isinstance(value, np.ndarray):
                    self[key] = value.tolist()
