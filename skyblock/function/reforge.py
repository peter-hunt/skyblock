from typing import Dict

from ..constant import STAT_ALIASES, REFORGES

from .io import red


__all__ = ['get_reforge']


def get_reforge(name: str, rarity: str, /) -> Dict[str, int]:
    if name is None:
        return {}
    elif name not in REFORGES:
        red(f'Invalid reforge: {name}')
        return

    bonuses = REFORGES[name]
    if rarity == 'mythic':
        rarity = 'l'

    result = {}
    for key, value in bonuses['curel'.index(rarity[0])].items():
        result[STAT_ALIASES[key]] = value
    return result
