from json import load
from os import mkdir, walk
from pathlib import Path
from subprocess import run

from ..function.io import *
from ..function.path import join_path
from ..function.util import get, includes

from .object import *


__all__ = ['ITEMS', 'get_item', 'validify_item', 'get_stack_size']

if not Path(join_path('skyblock', 'data')).is_dir():
    green('Installing assets...')
    mkdir(join_path('skyblock', 'data'))
    run(['git', 'clone', 'https://github.com/peter-hunt/skyblock-data',
         join_path('skyblock', 'data')])


ITEMS = []
for item_type in [*walk(join_path('skyblock', 'data', 'items'))][0][1]:
    for file_name in [
            *walk(join_path('skyblock', 'data', 'items', item_type))][0][2]:
        if not file_name.endswith('.json'):
            continue

        with open(join_path('skyblock', 'data', 'items',
                            item_type, file_name)) as file:
            ITEMS.append(load_item(load(file)))


def get_item(name: str, /, **kwargs) -> ItemType:
    if not includes(ITEMS, name):
        red(f'Item not found: {name!r}')
        exit()
    return get(ITEMS, name, **kwargs)


def get_stack_size(name: str, /) -> int:
    return getattr(get_item(name), 'count', 1)


def validify_item(item: ItemType, /) -> ItemType:
    attrs = {}
    kwargs = {}
    if getattr(item, 'enchantments', {}) != {}:
        attrs['enchantments'] = item.enchantments.copy()
    if getattr(item, 'hot_potato', 0) != 0:
        attrs['hot_potato'] = item.hot_potato
    if getattr(item, 'modifier', None) is not None:
        attrs['modifier'] = item.modifier
    if getattr(item, 'stars', 0) != 0:
        attrs['stars'] = item.stars
    if getattr(item, 'tier', None) is not None:
        kwargs['tier'] = item.tier

    if getattr(item, 'rarity', None) != None:
        if isinstance(item, (Sword, Bow, Armor, Pet)):
            kwargs['rarity'] = item.rarity
        else:
            attrs['rarity'] = item.rarity

    item_copy = get_item(item.name, **kwargs)
    for key, value in attrs.items():
        setattr(item_copy, key, value)

    return item_copy
