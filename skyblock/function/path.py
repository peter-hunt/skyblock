from os.path import join
from pathlib import Path

from .io import yellow

__all__ = ['is_dir', 'is_file']


def is_dir(*names, warn: bool = False):
    if not Path(join(Path.home(), 'skyblock', *names)).is_dir():
        path = join('~', 'skyblock', *names)
        if warn:
            yellow(f'Warning: folder {path} not found.')
        return False
    return True


def is_file(*names, warn: bool = False):
    if not Path(join(Path.home(), 'skyblock', *names)).is_file():
        path = join('~', 'skyblock', *names)
        if warn:
            yellow(f'Warning: file {path} not found.')
        return False
    return True
