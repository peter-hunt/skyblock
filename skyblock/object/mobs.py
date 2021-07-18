from json import load
from os import walk
from typing import Optional

from ..function.io import *
from ..function.path import join_path
from ..function.util import get, includes

from .object import *


__all__ = ['MOBS', 'get_mob']

MOBS = []
for file_name in [*walk(join_path('skyblock', 'data', 'mobs'))][0][2]:
    if not file_name.endswith('.json'):
        continue

    print(file_name)
    with open(join_path('skyblock', 'data', 'mobs', file_name)) as file:
        MOBS.append(Mob.from_obj(load(file)))


def get_mob(name: str, /, *, warn=True, **kwargs) -> Optional[ItemType]:
    if not includes(MOBS, name):
        if warn:
            red(f'Mob not found: {name!r}')
        return
    return get(MOBS, name, **kwargs)
