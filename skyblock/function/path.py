from os.path import join
from pathlib import Path

from .io import *


__all__ = ['is_dir', 'is_file', 'is_profile']


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


def is_profile(name: str, /):
    return is_dir() and is_dir('saves') and is_file('saves', f'{name}.json')
