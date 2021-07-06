from ...object import Axe


__all__ = ['AXES']

AXES = [
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
]
