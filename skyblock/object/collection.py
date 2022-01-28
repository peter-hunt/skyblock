from json import load
from os import walk
from pathlib import Path
from typing import Optional

from .._lib import _open
from ..function.io import red
from ..path import join_path

from .object import *


__all__ = ['COLLECTIONS', 'is_collection', 'get_collection', 'calc_coll_level']

if not Path(join_path('skyblock', 'data', 'collections')).is_dir():
    raise FileNotFoundError(
        'Required data not found.\nRestart skyblock to fix it automatically.'
    )

COLLECTIONS = []
for category in [*walk(join_path('skyblock', 'data', 'collections'))][0][1]:
    for file_name in [*walk(join_path('skyblock', 'data',
                                      'collections', category))][0][2]:
        if not file_name.endswith('.json'):
            continue

        with _open(join_path('skyblock', 'data', 'collections',
                             category, file_name)) as file:
            COLLECTIONS.append(Collection.load(load(file)))
COLLECTIONS = sorted(COLLECTIONS, key=lambda collection: collection.name)


def is_collection(name: str) -> bool:
    for collection in COLLECTIONS:
        if collection.name == name:
            return True

    return False


def get_collection(name: str) -> Optional[Collection]:
    for collection in COLLECTIONS:
        if collection.name == name:
            return collection

    red(f'Collection not found: {name!r}')


def calc_coll_level(name: str, amount: int) -> Optional[int]:
    if (collection := get_collection(name)) is None:
        return

    for lvl, (lvl_amount, _) in enumerate(collection):
        if amount < lvl_amount:
            return lvl

    return lvl + 1
