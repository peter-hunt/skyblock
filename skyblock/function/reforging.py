from typing import Dict, Optional

from ..constant.enchanting import ENCH_LVLS
from ..constant.reforging import STAT_ALIASES, MODIFIERS
from ..constant.util import Ench

from .io import *


__all__ = ['combine_ench', 'get_modifier']


def combine_ench(ench_1: Ench, ench_2: Ench, /) -> Ench:
    names = {*ench_1, *ench_2}
    result = {}

    for name in names:
        if name in ench_1 and name in ench_2:
            if ench_1[name] == ench_2[name]:
                if ench_1[name] < ENCH_LVLS[name]:
                    result[name] = ench_1[name] + 1
                else:
                    result[name] = ench_1[name]
            else:
                result[name] = max(ench_1[name], ench_2[name])
        elif name in ench_1:
            result[name] = ench_1[name]
        else:
            result[name] = ench_2[name]

    return result


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
