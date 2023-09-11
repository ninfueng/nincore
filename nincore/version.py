"""Version related functions."""
import types

from packaging.version import Version, parse

__all__ = [
    "parse_module",
    "is_newer_equal",
    "is_newer",
    "is_older_equal",
    "is_older",
    "is_equal",
]


def parse_module(module: types.ModuleType) -> Version:
    """Parse version from given module.

    Example:
    >>> import torch
    >>> parse_module(torch)
    1.12.1+cu113
    """
    version = getattr(module, "__version__")
    version = parse(version)
    return version


def is_newer(module: types.ModuleType, version: str) -> bool:
    """Return True if `module.__version__` is newer than `version`.

    Example:
    >>> import torch
    >>> is_newer(torch, "0.0.0")
    True
    """
    module_version = parse_module(module)
    version = parse(version)
    return module_version > version


def is_newer_equal(module: types.ModuleType, version: str) -> bool:
    """Return True if `module.__version__` is newer or equal than `version`.

    Example:
    >>> import torch
    >>> is_newer_equal(torch, "0.0.0")
    True
    """
    module_version = parse_module(module)
    version = parse(version)
    return module_version >= version


def is_older(module: types.ModuleType, version: str) -> bool:
    """Return True if `module.__version__` is newer or equal than `version`."""
    module_version = parse_module(module)
    version = parse(version)
    return module_version < version


def is_older_equal(module: types.ModuleType, version: str) -> bool:
    """Return True if `module.__version__` is newer than `version`."""
    module_version = parse_module(module)
    version = parse(version)
    return module_version <= version


def is_equal(module: types.ModuleType, version: str) -> bool:
    """Return True if `module.__version__` is newer than `version`."""
    module_version = parse_module(module)
    version = parse(version)
    return module_version == version


if __name__ == "__main__":
    import numpy as np
    import packaging

    version = parse_module(np)

    print(version)
    packaging.version.parse(np.__version__)
    print(version)

    res = version == np.__version__
