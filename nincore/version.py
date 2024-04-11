"""Version related functions."""

from types import ModuleType

from packaging.version import Version, parse

__all__ = [
    'parse_module_ver',
    'is_newer_equal_ver',
    'is_newer_ver',
    'is_older_equal_ver',
    'is_older_ver',
    'is_same_ver',
]


def parse_module_ver(module: ModuleType) -> Version:
    """Parse version from given module.

    Example:
    >>> import torch
    >>> parse_module_ver(torch)
    1.12.1+cu113
    """
    version = getattr(module, '__version__')
    version = parse(version)
    return version


def is_newer_ver(module: ModuleType, version: str) -> bool:
    """Return True if `module.__version__` is newer than `version`.

    Example:
    >>> import torch
    >>> is_newer_ver(torch, '0.0.0')
    True
    """
    module_version = parse_module_ver(module)
    version = parse(version)
    return module_version > version


def is_newer_equal_ver(module: ModuleType, version: str) -> bool:
    """Return True if `module.__version__` is newer or equal than `version`.

    Example:
    >>> import torch
    >>> is_newer_equal_ver(torch, '0.0.0')
    True
    """
    module_version = parse_module_ver(module)
    version = parse(version)
    return module_version >= version


def is_older_ver(module: ModuleType, version: str) -> bool:
    """Return True if `module.__version__` is newer or equal than `version`."""
    module_version = parse_module_ver(module)
    version = parse(version)
    return module_version < version


def is_older_equal_ver(module: ModuleType, version: str) -> bool:
    """Return True if `module.__version__` is newer than `version`."""
    module_version = parse_module_ver(module)
    version = parse(version)
    return module_version <= version


def is_same_ver(module: ModuleType, version: str) -> bool:
    """Return True if `module.__version__` is newer than `version`."""
    module_version = parse_module_ver(module)
    version = parse(version)
    return module_version == version


if __name__ == '__main__':
    import numpy as np
    import packaging

    version = parse_module_ver(np)
    print(version)
    packaging.version.parse(np.__version__)
    print(version)
    res = version == np.__version__
