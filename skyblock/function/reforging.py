from typing import Dict

from ..constant import STAT_ALIASES, MODIFIERS

from .io import red


__all__ = ['get_modifier']


def get_modifier(name: str, rarity: str, /) -> Dict[str, int]:
    if name is None:
        return {}
    elif name not in MODIFIERS:
        red(f'Invalid modifier: {name}')
        return

    bonuses = MODIFIERS[name]
    if rarity == 'mythic':
        rarity = 'l'

    result = {}
    for key, value in bonuses['curel'.index(rarity[0])].items():
        result[STAT_ALIASES[key]] = value
    return result
