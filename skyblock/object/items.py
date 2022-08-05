from json import load
from os import walk
from pathlib import Path

from ..function.file import load_folder
from ..function.io import *
from ..function.util import get, includes, includes_id
from ..path import join_path

from .abilities import ABILITIES
from .object import *


__all__ = ['ITEMS', 'get_item', 'get_stack_size']

if not Path(join_path('skyblock', 'data', 'items')).is_dir():
    raise FileNotFoundError(
        'Required data not found.\nRestart skyblock to fix it automatically.'
    )

ITEMS = load_folder(join_path('skyblock', 'data', 'items'), load_item)
ITEMS = sorted(ITEMS, key=lambda item: item.name)


def get_item(name: str, /, **kwargs) -> ItemType:
    if not includes(ITEMS, name):
        red(f'Item not found: {name!r}')
    return get(ITEMS, name, **kwargs)


def get_stack_size(name: str, /) -> int:
    return getattr(get_item(name), 'count', 1)


for item in ITEMS:
    for ability in getattr(item, 'abilities', []):
        if not includes_id(ABILITIES, ability):
            yellow(f'Invalid item ability: {ability!r} of item {item.name!r}')
