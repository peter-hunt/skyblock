from json import load
from os import walk
from pathlib import Path

from .._lib import _open
from ..function.io import *
from ..function.util import get, includes
from ..path import join_path

from .object import *


__all__ = ['ITEMS', 'get_item', 'get_stack_size']

if not Path(join_path('skyblock', 'data', 'items')).is_dir():
    raise FileNotFoundError(
        'Required data not found.\nRestart skyblock to fix it automatically.'
    )

ITEMS = []
for item_type in [*walk(join_path('skyblock', 'data', 'items'))][0][1]:
    for file_name in [
            *walk(join_path('skyblock', 'data', 'items', item_type))][0][2]:
        if not file_name.endswith('.json'):
            continue

        with _open(join_path('skyblock', 'data', 'items',
                             item_type, file_name)) as file:
            ITEMS.append(load_item(load(file)))
ITEMS = sorted(ITEMS, key=lambda item: item.name)


def get_item(name: str, /, **kwargs) -> ItemType:
    if not includes(ITEMS, name):
        red(f'Item not found: {name!r}')
        exit()
    return get(ITEMS, name, **kwargs)


def get_stack_size(name: str, /) -> int:
    return getattr(get_item(name), 'count', 1)
