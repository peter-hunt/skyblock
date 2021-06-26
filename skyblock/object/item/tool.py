from ..object import Axe, Hoe, Pickaxe, Drill


__all__ = ['TOOLS']

TOOLS = [
    Axe('wooden_axe', rarity='common', tool_speed=2),
    Axe('stone_axe', rarity='common', tool_speed=4),
    Axe('golden_axe', rarity='common', tool_speed=12),
    Axe('iron_axe', rarity='common', tool_speed=6),
    Axe('diamond_axe', rarity='uncommon', tool_speed=8),

    Axe('rookie_axe', rarity='common', tool_speed=4,
        enchantments={'efficiency': 1}),
    Axe('promising_axe', rarity='uncommon', tool_speed=6),
    Axe('sweet_axe', rarity='uncommon', tool_speed=6),
    Axe('efficient_axe', rarity='uncommon', tool_speed=6),

    Axe('jungle_axe', rarity='uncommon', tool_speed=2,
        abilities=['jungle_axe']),
    Axe('treecapitator', rarity='epic', tool_speed=12,
        abilities=['treecapitator']),

    Hoe('wooden_hoe', rarity='common'),
    Hoe('golden_hoe', rarity='common'),
    Hoe('stone_hoe', rarity='common'),
    Hoe('iron_hoe', rarity='common'),
    Hoe('diamond_hoe', rarity='uncommon'),

    Hoe('rookie_hoe', rarity='common'),

    Pickaxe('wooden_pickaxe', rarity='common',
            breaking_power=1, mining_speed=70),
    Pickaxe('golden_pickaxe', rarity='common',
            breaking_power=1, mining_speed=250),
    Pickaxe('stone_pickaxe', rarity='common',
            breaking_power=2, mining_speed=110),
    Pickaxe('iron_pickaxe', rarity='common',
            breaking_power=3, mining_speed=160),
    Pickaxe('diamond_pickaxe', rarity='uncommon',
            breaking_power=4, mining_speed=230),

    Pickaxe('rookie_pickaxe', rarity='common',
            breaking_power=2, mining_speed=180,
            enchantments={'efficiency': 1}),
    Pickaxe('promising_pickaxe', rarity='uncommon',
            breaking_power=2, mining_speed=190),

    Pickaxe('zombie_pickaxe', rarity='common',
            breaking_power=3, mining_speed=290),

    Pickaxe('stonk', rarity='epic',
            breaking_power=1, mining_speed=380,
            enchantments={'efficiency': 6}),

    Pickaxe('fractured_mithril_pickaxe', rarity='uncommon',
            breaking_power=5, mining_speed=200),
    Pickaxe('bandaged_mithril_pickaxe', rarity='uncommon',
            breaking_power=5, mining_speed=250),
    Pickaxe('mithril_pickaxe', rarity='uncommon',
            breaking_power=5, mining_speed=280),
    Pickaxe('refined_mithril_pickaxe', rarity='rare',
            breaking_power=5, mining_speed=300),
    Pickaxe('titanium_pickaxe', rarity='rare',
            breaking_power=6, mining_speed=310),
    Pickaxe('refined_titanium_pickaxe', rarity='rare',
            breaking_power=6, mining_speed=400),

    Drill('mithril_drill_226', rarity='rare',
          breaking_power=5, mining_speed=450),
    Drill('mithril_drill_326', rarity='rare',
          breaking_power=6, mining_speed=600),
    Drill('titanium_drill_355', rarity='epic',
          breaking_power=7, mining_speed=700, mining_fortune=15),
    Drill('titanium_drill_455', rarity='epic',
          breaking_power=8, mining_speed=900, mining_fortune=15),
    Drill('titanium_drill_555', rarity='epic',
          breaking_power=9, mining_speed=1_200, mining_fortune=15)]
