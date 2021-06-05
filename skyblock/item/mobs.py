from typing import Any

from .items import get_item
from .object import ItemType, Mob

__all__ = ['MOBS', 'get_mob']


MOBS = [
    Mob('enderman', level=42, health=4_500, damage=500,
        coins=10, combat_xp=40.8, xp_orb=8,
        drops=[
            (get_item('ender_pearl'), (1, 3), 'common', 1),
            (get_item('enchanted_ender_pearl'), 1, 'rare', 0.01),
            (get_item('enderman_pet', rarity='common'), 1, 'legendary', 0.0005),
            (get_item('enderman_pet', rarity='uncommon'), 1, 'legendary', 0.0002),
            (get_item('enderman_pet', rarity='rare'), 1, 'legendary', 0.0001),
        ]),
    Mob('enderman', level=45, health=6_000, damage=600,
        coins=12, combat_xp=40.8, xp_orb=9,
        drops=[
            (get_item('ender_pearl'), (1, 3), 'common', 1),
            (get_item('enchanted_ender_pearl'), 1, 'rare', 0.01),
            (get_item('enderman_pet', rarity='uncommon'), 1, 'legendary', 0.0005),
            (get_item('enderman_pet', rarity='rare'), 1, 'legendary', 0.0002),
            (get_item('enderman_pet', rarity='epic'), 1, 'legendary', 0.0001),
        ]),
    Mob('enderman', level=50, health=9_000, damage=700,
        coins=15, combat_xp=40.8, xp_orb=10,
        drops=[
            (get_item('ender_pearl'), (1, 2), 'common', 1),
            (get_item('enchanted_ender_pearl'), 1, 'rare', 0.01),
            (get_item('enderman_pet', rarity='rare'), 1, 'legendary', 0.001),
            (get_item('enderman_pet', rarity='epic'), 1, 'legendary', 0.0001),
            (get_item('enderman_pet', rarity='legendary'),
             1, 'legendary', 0.000006),
        ]),
]


def get_mob(name: str, default: Any = None, **kwargs) -> ItemType:
    for mob in MOBS:
        if mob.name == name:
            for kwarg in kwargs:
                if getattr(mob, kwarg, None) != kwargs[kwarg]:
                    break
            else:
                return mob.copy()
    return default.copy() if hasattr(default, 'copy') else default
