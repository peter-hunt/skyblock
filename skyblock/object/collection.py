from pathlib import Path

from ..function.file import load_folder
from ..function.io import *
from ..path import join_path

from .object import *


__all__ = ['COLLECTIONS', 'is_collection', 'get_collection', 'calc_coll_level']

if not Path(join_path('skyblock', 'data', 'collections')).is_dir():
    raise FileNotFoundError(
        'Required data not found.\nRestart skyblock to fix it automatically.'
    )

COLLECTIONS = load_folder(join_path('skyblock', 'data', 'collections'), Collection.load)
COLLECTIONS = sorted(COLLECTIONS, key=lambda collection: collection.name)


def is_collection(name: str) -> bool:
    for collection in COLLECTIONS:
        if collection.name == name:
            return True

    return False


def get_collection(name: str) -> Collection | None:
    for collection in COLLECTIONS:
        if collection.name == name:
            return collection

    red(f'Collection not found: {name!r}')


def calc_coll_level(name: str, amount: int) -> int | None:
    if (collection := get_collection(name)) is None:
        return

    for lvl, (lvl_amount, _) in enumerate(collection):
        if amount < lvl_amount:
            return lvl

    return lvl + 1
