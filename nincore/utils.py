import glob
import logging
import os
import shutil
import sys
import warnings
from pathlib import Path
from typing import Sequence, Union

logger = logging.getLogger(__name__)

__all__ = ["filter_warn", "set_logger", "backup_scripts", "apply_rich", "AvgMeter"]


# https://docs.python.org/3/library/warnings.html
def filter_warn() -> None:
    if not sys.warnoptions:
        warnings.simplefilter("ignore")


def apply_rich() -> None:
    try:
        from rich import pretty, traceback

        pretty.install()
        traceback.install()

    except ImportError:
        raise ImportError("This `apply_rich` function requires the `rich` package.")


def backup_scripts(filetype: Union[str, Sequence], dest: str) -> None:
    """Copy all files with `filetype` to the dest location."""
    os.makedirs(dest, exist_ok=True)
    scripts = []
    if isinstance(filetype, str):
        scripts += glob.glob(os.path.join(os.curdir, f"*{filetype}"))
    elif isinstance(filetype, Sequence):
        # This `Sequence` can be used for the tuple and list.
        for f in filetype:
            scripts += glob.glob(os.path.join(os.curdir, f"*{f}"))
    else:
        raise NotImplementedError(f"Not support filetype: {filetype}.")

    for s in scripts:
        file_name = os.path.basename(s)
        shutil.copy2(os.path.join(s), os.path.join(dest, file_name))


# https://github.com/huggingface/pytorch-image-models/blob/main/timm/utils/metrics.py
class AvgMeter:
    """Computes and stores the average and current value"""

    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0

    def update(self, val: int, n: int = 1) -> None:
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count


def set_logger(
    log_dir: Union[str, Path],
    level: int = logging.INFO,
    stdout: bool = True,
    rm_exist: bool = True,
    with_color: bool = False,
) -> None:
    """Set the logger to log info in terminal and file `log_dir`.
    In general, it is useful to have a logger so that every output to the terminal
    is saved in a permanent file. Here we save it to `model_dir/train.log`.

    Args:
        log_dir: (string) location of log file
        log_level: (string) set log level
        stdout: (bool) whether to print log to stdout
        rm_exist: (bool) remove the old log file before start log or not
        verbose: (bool) if True, verbose some information

    Example:
    >>> set_logger("info.log")
    >>> logger.info("Starting training...")
    """
    assert isinstance(stdout, bool)
    assert level in [0, 10, 20, 30, 40, 50]
    assert isinstance(rm_exist, bool)

    log_dir = Path(log_dir)
    log_dir = log_dir.expanduser()
    parent_dir = log_dir.parent

    if not parent_dir.is_dir():
        parent_dir.mkdir(exist_ok=True)

    if rm_exist and parent_dir.is_file():
        log_dir.unlink()

    logger = logging.getLogger()
    logger.setLevel(level)

    if not logger.handlers:
        file_handler = logging.FileHandler(log_dir)
        file_handler.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(filename)s: %(message)s"))
        logger.addHandler(file_handler)

        if stdout:
            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(filename)s: %(message)s"))
            logger.addHandler(stream_handler)

    if with_color:
        # https://stackoverflow.com/questions/384076/how-can-i-color-python-logging-output
        if sys.stderr.isatty():
            logging.addLevelName(logging.INFO, f"\033[1;32m{logging.getLevelName(logging.INFO)}\033[1;0m")
            logging.addLevelName(
                logging.WARNING,
                f"\033[1;33m{logging.getLevelName(logging.WARNING)}\033[1;0m",
            )
            logging.addLevelName(
                logging.ERROR,
                f"\033[1;31m{logging.getLevelName(logging.ERROR)}\033[1;0m",
            )
            logging.addLevelName(
                logging.CRITICAL,
                f"\041[1;31m{logging.getLevelName(logging.ERROR)}\033[1;0m",
            )
