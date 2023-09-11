"""Version related functions."""
import types

import pkg_resources as pkg
from pkg_resources.extern import packaging

__all__ = [
    "parse_version",
    "is_newer_equal",
    "is_newer",
    "is_older_equal",
    "is_older",
    "is_equal",
]


def parse_version(module: types.ModuleType) -> packaging.version.Version:
    """Parse version from given module.

    Example:
    >>> import torch
    >>> parse_version(torch)
    1.12.1+cu113
    """
    version = getattr(module, "__version__")
    version = pkg.parse_version(version)
    return version


def is_newer(module: types.ModuleType, version: str) -> bool:
    """Return True if `module.__version__` is newer than `version`.

    Example:
    >>> import torch
    >>> is_newer(torch, "0.0.0")
    True
    """
    module_version = parse_version(module)
    version = pkg.parse_version(version)
    return module_version > version


def is_newer_equal(module: types.ModuleType, version: str) -> bool:
    """Return True if `module.__version__` is newer or equal than `version`.

    Example:
    >>> import torch
    >>> is_newer_equal(torch, "0.0.0")
    True
    """
    module_version = parse_version(module)
    version = pkg.parse_version(version)
    return module_version >= version


def is_older(module: types.ModuleType, version: str) -> bool:
    """Return True if `module.__version__` is newer or equal than `version`."""
    module_version = parse_version(module)
    version = pkg.parse_version(version)
    return module_version < version


def is_older_equal(module: types.ModuleType, version: str) -> bool:
    """Return True if `module.__version__` is newer than `version`."""
    module_version = parse_version(module)
    version = pkg.parse_version(version)
    return module_version <= version


def is_equal(module: types.ModuleType, version: str) -> bool:
    """Return True if `module.__version__` is newer than `version`."""
    module_version = parse_version(module)
    version = pkg.parse_version(version)
    return module_version == version
