from typing import Dict, Optional

from ..constant import STAT_ALIASES, MODIFIERS

from .io import red


__all__ = ['get_modifier']


def get_modifier(name: Optional[str], rarity: str, /) -> Dict[str, int]:
    """
    Get modifier bonus from the item.

    Args:
        name: Name of the modifier.
        rarity: Rarity of the item.

    Returns:
        A dict of stat boost by the modifier.
    """

    if name is None:
        return {}
    elif name not in MODIFIERS:
        red(f'Modifier not found: {name}')
        return

    bonuses = MODIFIERS[name]
    rarity = rarity[0]
    if rarity in {'m', 's', 'v'}:
        rarity = 'l'

    result = {}
    for key, value in bonuses['curel'.index(rarity[0])].items():
        result[STAT_ALIASES[key]] = value
    return result
