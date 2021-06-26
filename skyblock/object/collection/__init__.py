from typing import Optional

from ...function.io import red

from ..object import Collection

from .combat import COMBAT_COLLECTIONS
from .farming import FARMING_COLLECTIONS
from .foraging import FORAGING_COLLECTIONS
from .mining import MINING_COLLECTIONS


__all__ = ['COLLECTIONS', 'is_collection', 'get_collection', 'calc_coll_lvl']

COLLECTIONS = (FARMING_COLLECTIONS + MINING_COLLECTIONS
               + COMBAT_COLLECTIONS + FORAGING_COLLECTIONS)


def is_collection(name: str) -> bool:
    for collection in COLLECTIONS:
        if collection.name == name:
            return True
    else:
        return False


def get_collection(name: str) -> Optional[Collection]:
    for collection in COLLECTIONS:
        if collection.name == name:
            return collection
    else:
        red(f'Unknown collection: {name!r}')


def calc_coll_lvl(name: str, amount: int) -> Optional[int]:
    if (collection := get_collection(name)) is None:
        return

    for lvl, (lvl_amount, _) in enumerate(collection):
        if amount < lvl_amount:
            return lvl
    else:
        return lvl + 1
