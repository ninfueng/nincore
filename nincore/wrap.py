import time
from typing import Any, Callable

__all__ = [
    "wrap_time",
    "wrap_identity",
    "WrapWithIdentity",
]


def wrap_time(fn: Callable[..., Any]) -> Callable[..., Any]:
    """Wrapper and print the run time of `fn`."""
    t0 = time.perf_counter()

    def wrapped(*args: Any, **kwargs: Any) -> Any:
        return fn(*args, **kwargs)

    diff = time.perf_counter() - t0
    print(f"Run `{fn=}` for {diff} seconds.")
    return wrapped


def wrap_identity(fn: Callable[..., Any]) -> Callable[..., Any]:
    """Same as identity wrapper used for a placeholder."""

    def wrapped(*args: Any, **kwargs: Any) -> Any:
        return fn(*args, **kwargs)

    return wrapped


class WrapWithIdentity:
    """Using for"""

    def __enter__(self, *_: Any, **__: Any) -> None:
        return

    def __exit__(self, *_: Any, **__: Any) -> None:
        return
