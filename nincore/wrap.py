import cProfile
import os
import time
from pstats import SortKey, Stats
from typing import Any, Callable

__all__ = [
    'wrap_time',
    'wrap_identity',
    'WrapWithIdentity',
    'wrap_profile',
]


def wrap_time(fn: Callable[..., Any]) -> Callable[..., Any]:
    """Wrapper and print the run time of `fn`."""
    t0 = time.perf_counter()

    def wrapped(*args: Any, **kwargs: Any) -> Any:
        return fn(*args, **kwargs)

    diff = time.perf_counter() - t0
    print(f'Run `{fn=}` for {diff} seconds.')
    return wrapped


def wrap_identity(fn: Callable[..., Any]) -> Callable[..., Any]:
    """Same as identity wrapper used for a placeholder."""

    def wrapped(*args: Any, **kwargs: Any) -> Any:
        return fn(*args, **kwargs)

    return wrapped


def wrap_profile(fn: Callable[..., Any]) -> Callable[..., Any]:
    def wrapped(*args: Any, **kwargs: Any) -> Any:
        with cProfile.Profile() as p:
            results = fn(*args, **kwargs)

        stats = Stats(p)
        stats.sort_stats(SortKey.CUMULATIVE)
        stats.print_stats()

        profile_file = os.path.expanduser('./profile.pstat')
        stats.dump_stats(profile_file)
        return results

    return wrapped


class WrapWithIdentity:
    """Using for"""

    def __enter__(self, *_: Any, **__: Any) -> None:
        return

    def __exit__(self, *_: Any, **__: Any) -> None:
        return


if __name__ == '__main__':

    @wrap_profile
    def test_profile():
        print('hello world')

    test_profile()
