from os.path import join
from pathlib import Path

from .io import *


__all__ = ['is_dir', 'is_file', 'is_profile']


def is_dir(*names, warn: bool = False):
    """
    Detect if a directory exists in ~/skyblock folder.

    Args:
        *names: Path to the target directory.
        warn: A boolean of whether to warn if the directory doesn't exist.
    """

    if not Path(join(Path.home(), 'skyblock', *names)).is_dir():
        path = join('~', 'skyblock', *names)
        if warn:
            yellow(f'Warning: folder {path} not found.')
        return False
    return True


def is_file(*names, warn: bool = False):
    """
    Detect if a file exists in ~/skyblock folder.

    Args:
        *names: Path to the target file.
        warn: A boolean of whether to warn if the file doesn't exist.
    """

    if not Path(join(Path.home(), 'skyblock', *names)).is_file():
        path = join('~', 'skyblock', *names)
        if warn:
            yellow(f'Warning: file {path} not found.')
        return False
    return True


def is_profile(name: str, /):
    """
    Detect if a profile exists in ~/skyblock folder.

    Args:
        name: Name of the target profile.
    """

    return (is_dir() and is_dir('saves')
            and is_file('saves', f'{name}.json'))
