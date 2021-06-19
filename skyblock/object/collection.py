from typing import Optional

from ..function.io import red

from .object import Collection
from .recipe import get_recipe

__all__ = ['COLLECTIONS', 'is_collection', 'get_collection', 'calc_coll_lvl']


COLLECTIONS = [
    Collection(
        'wheat', 'farming',
        [
            (50, 5),
            (100, 10),
            (250, (get_recipe('farm_suit_helmet'),
                   get_recipe('farm_suit_chestplate'),
                   get_recipe('farm_suit_leggings'),
                   get_recipe('farm_suit_boots'))),
            (500, 50),
            (1_000, 100),
            (2_500, 250),
            (10_000, get_recipe('hay_to_enchanted')),
            (15_000, 1_500),
            (25_000, (get_recipe('farm_helmet'),
                      get_recipe('farm_chestplate'),
                      get_recipe('farm_leggings'),
                      get_recipe('farm_boots'))),
            (50_000, 5_000),
            (100_000, get_recipe('hay_to_tighted')),
        ],
    ),
    Collection(
        'carrot', 'farming',
        [
            (100, 10),
            (250, 25),
            (500, 50),
            (1_700, 170),
            (5_000, 500),
            (10_000, 1_000),
            (25_000, 2_500),
            (50_000, 5_000),
            (100_000, 10_000),
        ],
    ),
    Collection(
        'potato', 'farming',
        [
            (100, 10),
            (250, 25),
            (500, 50),
            (1_700, 170),
            (5_000, 500),
            (10_000, 1_000),
            (25_000, 2_500),
            (50_000, 5_000),
            (100_000, 10_000),
        ],
    ),
    Collection(
        'pumpkin', 'farming',
        [
            (40, 4),
            (100, 10),
            (250, 25),
            (1_000, 100),
            (2_500, 250),
            (5_000, 500),
            (10_000, 1_000),
            (25_000, 2_500),
            (50_000, 5_000),
            (100_000, 10_000),
            (250_000, 25_000),
        ],
    ),
    Collection(
        'melon', 'farming',
        [
            (250, 25),
            (500, 50),
            (1_200, 120),
            (5_000, 500),
            (15_500, 1_550),
            (25_000, 2_500),
            (50_000, 5_000),
            (100_000, 10_000),
            (250_000, 25_000),
        ],
    ),
    Collection(
        'seeds', 'farming',
        [
            (50, 5),
            (100, 10),
            (250, 25),
            (1_000, 100),
            (2_500, 250),
            (5_000, 500),
        ],
    ),
    Collection(
        'mushroom', 'farming',
        [
            (50, 5),
            (100, 10),
            (250, 25),
            (1_000, 100),
            (2_500, 250),
            (5_000, 500),
            (10_000, 1_000),
            (25_000, 2_500),
            (50_000, 5_000),
        ],
    ),
    Collection(
        'cocoa_beans', 'farming',
        [
            (75, 7.5),
            (200, 20),
            (500, 50),
            (2_000, 200),
            (5_000, 500),
            (10_000, 1_000),
            (20_000, 2_000),
            (50_000, 5_000),
            (100_000, 10_000),
        ],
    ),
    Collection(
        'cactus', 'farming',
        [
            (100, 10),
            (250, 25),
            (500, 50),
            (1_000, 100),
            (2_500, 250),
            (5_000, 500),
            (10_000, 1_000),
            (25_000, 2_500),
            (50_000, 5_000),
        ],
    ),
    Collection(
        'sugar_cane', 'farming',
        [
            (100, 10),
            (250, 25),
            (500, 50),
            (1_000, 100),
            (2_500, 250),
            (5_000, 500),
            (10_000, 1_000),
            (25_000, 2_500),
            (50_000, 5_000),
        ],
    ),
]


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
