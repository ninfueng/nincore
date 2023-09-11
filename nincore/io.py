import json
import os
import pickle
import re
from typing import Any, Dict

import yaml

__all__ = [
    "save_json",
    "load_json",
    "load_yaml",
    "save_yaml",
    "load_pt",
    "save_pt",
]


def load_json(json_dir: str) -> Dict[str, Any]:
    """Load a toml file as a `dict`."""
    assert isinstance(json_dir, str)
    json_dir = os.path.expanduser(json_dir)
    with open(json_dir, "r") as f:
        dict_ = json.load(f)
    return dict_


def save_json(dict_: Dict[str, Any], json_file: str, indent: int = 4) -> None:
    """Save a `dict` as a json file."""
    assert isinstance(json_file, str)
    json_file = os.path.expanduser(json_file)
    dirname = os.path.dirname(json_file)
    os.makedirs(dirname, exist_ok=True)
    with open(json_file, "w") as f:
        # Avoid objects which can not be serializable.
        json.dump(dict_, f, indent=indent, default=lambda _: "<not serializable>")


def load_yaml(yaml_dir: str) -> Dict[str, Any]:
    """Load a yaml file to `dict`.

    Example:
    >>> load_yaml('./config.yaml')
    """
    assert isinstance(yaml_dir, str)
    yaml_dir = os.path.expanduser(yaml_dir)
    # https://stackoverflow.com/questions/30458977/yaml-loads-5e-6-as-string-and-not-a-number
    loader = yaml.SafeLoader
    loader.add_implicit_resolver(
        "tag:yaml.org,2002:float",
        re.compile(
            """^(?:
         [-+]?(?:[0-9][0-9_]*)\\.[0-9_]*(?:[eE][-+]?[0-9]+)?
        |[-+]?(?:[0-9][0-9_]*)(?:[eE][-+]?[0-9]+)
        |\\.[0-9_]+(?:[eE][-+][0-9]+)?
        |[-+]?[0-9][0-9_]*(?::[0-5]?[0-9])+\\.[0-9_]*
        |[-+]?\\.(?:inf|Inf|INF)
        |\\.(?:nan|NaN|NAN))$""",
            re.X,
        ),
        list("-+0123456789."),
    )

    with open(yaml_dir, "r") as f:
        data = yaml.load(f, Loader=loader)
    return data


# https://stackabuse.com/reading-and-writing-yaml-to-a-file-in-python/
def save_yaml(dict_: Dict[str, Any], save_dir: str) -> None:
    """Save a `dict` to a yaml file.

    Example:
    >>> dict_ = load_yaml('./config.yaml')
    >>> dump_yaml(dict_, './config2.yaml')
    """
    assert isinstance(save_dir, str)
    save_dir = os.path.expanduser(save_dir)
    dirname = os.path.dirname(save_dir)
    os.makedirs(dirname, exist_ok=True)

    with open(save_dir, "w") as f:
        yaml.dump(dict_, f)


def load_pt(pickle_dir: str) -> Any:
    assert isinstance(pickle_dir, str)
    pickle_dir = os.path.expanduser(pickle_dir)
    with open(pickle_dir, "rb") as f:
        return pickle.load(f)


def save_pt(obj: Any, save_dir: str) -> None:
    """Save a object to pickle file."""
    assert isinstance(save_dir, str)
    save_dir = os.path.expanduser(save_dir)
    with open(save_dir, "wb") as p:
        pickle.dump(obj, p, protocol=pickle.HIGHEST_PROTOCOL)


try:
    import tomli

    def load_toml(toml_dir: str) -> Dict[str, Any]:
        """Load a toml file as a `dict`."""
        assert isinstance(toml_dir, str)
        toml_dir = os.path.expanduser(toml_dir)
        with open(toml_dir, "rb") as f:
            dict_ = tomli.load(f)
        return dict_

    __all__ += ["load_toml"]

except ImportError:
    pass

try:
    import tomli_w

    def save_toml(dict_: Dict[str, Any], toml_file: str) -> None:
        """Save a `dict` as a toml file."""

        assert isinstance(toml_file, str)
        toml_file = os.path.expanduser(toml_file)
        dirname = os.path.dirname(toml_file)
        os.makedirs(dirname, exist_ok=True)
        with open(toml_file, "wb") as f:
            tomli_w.dump(dict_, f)

    __all__ += ["save_toml"]

except ImportError:
    pass
