from pathlib import Path

from ..constant.util import Number
from ..function.file import load_folder
from ..function.io import *
from ..function.util import get, includes
from ..path import join_path

from .items import *
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


for mob in MOBS:
    for drop in mob.drops:
        pointer = drop[0]
        if isinstance(pointer, Number):
            continue

        pointer = pointer.copy()
        name = pointer['name']
        if not includes(ITEMS, name):
            yellow(f'Item not found: {name!r} in mob drop {mob.name!r}')
            continue
        del pointer['name']
        if get(ITEMS, name, **pointer) is None:
            yellow(f'Invalid item: {name!r} in mob drop {mob.name!r}')
