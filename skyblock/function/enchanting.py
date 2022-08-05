from ..constant.enchanting import *


__all__ = ['get_enchantments']


def get_enchantments(item) -> list[str]:
    cls = item.__class__.__name__
    if cls == 'Armor':
        table = ARMOR_ENCHS
    elif cls == 'Axe':
        table = AXE_ENCHS
    elif cls == 'Bow':
        table = BOW_ENCHS
    elif cls in {'Drill', 'Pickaxe'}:
        table = PICKAXE_ENCHS
    elif cls == 'FishingRod':
        table = FISHING_ROD_ENCHS
        if item.damage != 0:
            table += SWORD_ENCHS
    elif cls == 'Hoe':
        table = HOE_ENCHS
    elif cls == 'Sword':
        table = SWORD_ENCHS
    else:
        table = []

    return table
