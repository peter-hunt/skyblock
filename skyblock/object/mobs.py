from json import load
from os import walk
from pathlib import Path

from .._lib import _open
from ..function.file import load_folder
from ..function.io import red
from ..function.util import get, includes
from ..path import join_path

from .object import *


__all__ = ['MOBS', 'get_mob']

if not Path(join_path('skyblock', 'data', 'mobs')).is_dir():
    raise FileNotFoundError(
        'Required data not found.\nRestart skyblock to fix it automatically.'
    )

MOBS = load_folder(join_path('skyblock', 'data', 'mobs'), Mob.from_obj)
MOBS = sorted(MOBS, key=lambda mob: (mob.name, mob.level))


def get_mob(name: str, /, *, warn=True, **kwargs) -> ItemType | None:
    if includes(MOBS, name):
        return get(MOBS, name, **kwargs)
    elif warn:
        red(f'Mob not found: {name!r}')
