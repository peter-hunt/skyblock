from ...object import *


__all__ = ['PICKAXES']

PICKAXES = [
    Pickaxe('wooden_pickaxe', rarity='common',
            breaking_power=1, mining_speed=70, damage=20),
    Pickaxe('golden_pickaxe', rarity='common',
            breaking_power=1, mining_speed=250, damage=15),
    Pickaxe('stone_pickaxe', rarity='common',
            breaking_power=2, mining_speed=110, damage=20),
    Pickaxe('iron_pickaxe', rarity='common',
            breaking_power=3, mining_speed=160, damage=25),
    Pickaxe('diamond_pickaxe', rarity='uncommon',
            breaking_power=4, mining_speed=230, damage=30),

    Pickaxe('rookie_pickaxe', rarity='common',
            breaking_power=2, mining_speed=180, damage=15,
            enchantments={'efficiency': 1}),
    Pickaxe('promising_pickaxe', rarity='uncommon',
            breaking_power=2, mining_speed=190, damage=20),

    Pickaxe('zombie_pickaxe', rarity='common',
            breaking_power=3, mining_speed=290),

    Pickaxe('stonk', rarity='epic',
            breaking_power=1, mining_speed=380,
            enchantments={'efficiency': 6}),

    Pickaxe('fractured_mithril_pickaxe', rarity='uncommon',
            breaking_power=5, mining_speed=200, damage=30),
    Pickaxe('bandaged_mithril_pickaxe', rarity='uncommon',
            breaking_power=5, mining_speed=250, damage=30),
    Pickaxe('mithril_pickaxe', rarity='uncommon',
            breaking_power=5, mining_speed=280, damage=40),
    Pickaxe('refined_mithril_pickaxe', rarity='rare',
            breaking_power=5, mining_speed=300, damage=50),
    Pickaxe('titanium_pickaxe', rarity='rare',
            breaking_power=6, mining_speed=310, damage=60),
    Pickaxe('refined_titanium_pickaxe', rarity='rare',
            breaking_power=6, mining_speed=400, damage=65),

    Drill('mithril_drill_226', rarity='rare',
          breaking_power=5, mining_speed=450, damage=65),
    Drill('mithril_drill_326', rarity='rare',
          breaking_power=6, mining_speed=600, damage=65),
    Drill('titanium_drill_355', rarity='epic',
          breaking_power=7, mining_speed=700, mining_fortune=15, damage=75),
    Drill('titanium_drill_455', rarity='epic',
          breaking_power=8, mining_speed=900, mining_fortune=15, damage=75),
    Drill('titanium_drill_555', rarity='epic',
          breaking_power=9, mining_speed=1_200, mining_fortune=15, damage=75),
]
