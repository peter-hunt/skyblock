from json import load
from os import walk
from pathlib import Path
from typing import Optional

from ..function.io import *
from ..function.util import get, includes
from ..path import join_path

from .object import *


__all__ = ['MOBS', 'get_mob']

if not Path(join_path('skyblock', 'data', 'mobs')).is_dir():
    raise FileNotFoundError(
        'Required data not found.\n'
        'Restart skyblock to fix it automatically.'
    )

MOBS = []
for file_name in [*walk(join_path('skyblock', 'data', 'mobs'))][0][2]:
    if not file_name.endswith('.json'):
        continue

    with open(join_path('skyblock', 'data', 'mobs', file_name)) as file:
        MOBS.append(Mob.from_obj(load(file)))
MOBS = sorted(MOBS, key=lambda mob: (mob.name, mob.level))


def get_mob(name: str, /, *, warn=True, **kwargs) -> Optional[ItemType]:
    if not includes(MOBS, name):
        if warn:
            red(f'Mob not found: {name!r}')
        return
    return get(MOBS, name, **kwargs)
