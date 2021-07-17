from typing import List

from ..constant.enchanting import *
from ..object.object import *


__all__ = ['get_enchantments']


def get_enchantments(item) -> List[str]:
    if isinstance(item, Armor):
        table = ARMOR_ENCHS
    elif isinstance(item, Axe):
        table = AXE_ENCHS
    elif isinstance(item, Bow):
        table = BOW_ENCHS
    elif isinstance(item, (Drill, Pickaxe)):
        table = PICKAXE_ENCHS
    elif isinstance(item, FishingRod):
        table = FISHING_ROD_ENCHS
        if item.damage != 0:
            table += SWORD_ENCHS
    elif isinstance(item, Hoe):
        table = HOE_ENCHS
    elif isinstance(item, Sword):
        table = SWORD_ENCHS
    else:
        table = []
    return table
