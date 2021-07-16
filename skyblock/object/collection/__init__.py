from typing import Optional

from ...function.io import *

from ..object import *

from .combat import COMBAT_COLLECTIONS as COMBAT
from .farming import FARMING_COLLECTIONS as FARMING
from .fishing import FISHING_COLLECTIONS as FISHING
from .foraging import FORAGING_COLLECTIONS as FORAGING
from .mining import MINING_COLLECTIONS as MINING


__all__ = ['COLLECTIONS', 'is_collection', 'get_collection', 'calc_coll_level']

COLLECTIONS = COMBAT + FARMING + FISHING + FORAGING + MINING


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
        red(f'Collection not found: {name!r}')


def calc_coll_level(name: str, amount: int) -> Optional[int]:
    if (collection := get_collection(name)) is None:
        return

    for lvl, (lvl_amount, _) in enumerate(collection):
        if amount < lvl_amount:
            return lvl
    else:
        return lvl + 1
