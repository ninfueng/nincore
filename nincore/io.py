import json
import os
import pickle
import re
from typing import Any, Dict

import yaml

__all__ = [
    'save_json',
    'load_json',
    'load_yaml',
    'save_yaml',
    'load_pt',
    'save_pt',
]


def load_json(json_dir: str) -> Dict[str, Any]:
    """Load a toml file as a `dict`."""
    assert isinstance(json_dir, str), f'`json_dir` is not `str`, Your: {type(json_dir)}'
    json_dir = os.path.expanduser(json_dir)
    with open(json_dir) as f:
        dict_ = json.load(f)
    return dict_


def save_json(dict_: Dict[str, Any], json_dir: str, indent: int = 4) -> None:
    """Save a `dict` as a json file."""
    assert isinstance(json_dir, str), f'`json_dir` is not `str`, Your: {type(json_dir)}'
    json_dir = os.path.expanduser(json_dir)
    dirname = os.path.dirname(json_dir)
    os.makedirs(dirname, exist_ok=True)
    with open(json_dir, 'w') as f:
        # Avoid objects which can not be serializable.
        json.dump(dict_, f, indent=indent, default=lambda _: '<not serializable>')


def load_yaml(yaml_dir: str) -> Dict[str, Any]:
    """Load a yaml file to `dict`.

    Example:
    >>> load_yaml('./config.yaml')
    """
    assert isinstance(yaml_dir, str), f'`yaml_dir` is not `str`, Your: {type(yaml_dir)}'
    yaml_dir = os.path.expanduser(yaml_dir)
    # https://stackoverflow.com/questions/30458977/yaml-loads-5e-6-as-string-and-not-a-number
    loader = yaml.SafeLoader
    loader.add_implicit_resolver(
        'tag:yaml.org,2002:float',
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
        list('-+0123456789.'),
    )

    with open(yaml_dir) as f:
        data = yaml.load(f, Loader=loader)
    return data


# https://stackabuse.com/reading-and-writing-yaml-to-a-file-in-python/
def save_yaml(dict_: Dict[str, Any], yaml_dir: str) -> None:
    """Save a `dict` to a yaml file.

    Example:
    >>> dict_ = load_yaml('./config.yaml')
    >>> dump_yaml(dict_, './config2.yaml')
    """
    assert isinstance(yaml_dir, str), f'`yaml_dir` is not `str`, Your: {type(yaml_dir)}'
    yaml_dir = os.path.expanduser(yaml_dir)
    dirname = os.path.dirname(yaml_dir)
    os.makedirs(dirname, exist_ok=True)
    with open(yaml_dir, 'w') as f:
        yaml.dump(dict_, f)


def load_pt(pt_dir: str) -> Any:
    assert isinstance(pt_dir, str), f'`pt_dir` is not `str`, Your: {type(pt_dir)}'
    pt_dir = os.path.expanduser(pt_dir)
    with open(pt_dir, 'rb') as f:
        return pickle.load(f)


def save_pt(obj: Any, pt_dir: str) -> None:
    """Save a object to pickle file."""
    assert isinstance(pt_dir, str), f'`pt_dir` is not `str`, Your: {type(pt_dir)}'
    pt_dir = os.path.expanduser(pt_dir)
    with open(pt_dir, 'wb') as p:
        pickle.dump(obj, p, protocol=pickle.HIGHEST_PROTOCOL)


try:
    import tomli

    def load_toml(toml_dir: str) -> Dict[str, Any]:
        """Load a toml file as a `dict`."""
        assert isinstance(toml_dir, str)
        toml_dir = os.path.expanduser(toml_dir)
        with open(toml_dir, 'rb') as f:
            dict_ = tomli.load(f)
        return dict_

    __all__ += ['load_toml']

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
        with open(toml_file, 'wb') as f:
            tomli_w.dump(dict_, f)

    __all__ += ['save_toml']

except ImportError:
    pass
