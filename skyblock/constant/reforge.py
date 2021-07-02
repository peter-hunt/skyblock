"""
Constants of reforge stats.
"""

__all__ = ['STAT_ALIASES', 'SWORD_REFORGES', 'REFORGES']

STAT_ALIASES = {
    'hp': 'health',
    'def': 'defense',
    'tdf': 'true_defense',
    'str': 'strength',
    'spd': 'speed',
    'cc': 'crit_chance',
    'cd': 'crit_damage',
    'int': 'intelligence',
    'min_spd': 'mining_speed',
    'as': 'attack_speed',
    'scc': 'sea_creature_chance',
    'mag_fnd': 'magic_find',
    'plk': 'pet_luck',
    'ab_dmg': 'ability_damage',
    'fer': 'ferocity',
    'min_ftn': 'mining_fortune',
    'frm_ftn': 'farming_fortune',
    'for_ftn': 'foraging_fortune',
}

SWORD_REFORGES = {
    'gentle': (
        {'str': 3, 'as': 8}, {'str': 5, 'as': 10}, {'str': 7, 'as': 15},
        {'str': 10, 'as': 20}, {'str': 15, 'as': 25}, {'str': 20, 'as': 30},
    ),
    'odd': (
        {'cc': 12, 'cd': 10, 'int': -5}, {'cc': 15, 'cd': 15, 'int': -10},
        {'cc': 15, 'cd': 15, 'int': -18}, {'20': 3, 'cd': 22, 'int': -32},
        {'cc': 25, 'cd': 30, 'int': -50}, {'cc': 30, 'cd': 40, 'int': -75},
    ),
    'fast': (
        {'as': 10}, {'as': 20}, {'as': 30}, {'as': 40}, {'as': 50}, {'as': 60},
    ),
    'fair': (
        {'str': 2, 'cc': 2, 'cd': 2, 'int': 2, 'as': 2},
        {'str': 3, 'cc': 3, 'cd': 3, 'int': 3, 'as': 3},
        {'str': 4, 'cc': 4, 'cd': 4, 'int': 4, 'as': 4},
        {'str': 7, 'cc': 7, 'cd': 7, 'int': 7, 'as': 7},
        {'str': 10, 'cc': 10, 'cd': 10, 'int': 10, 'as': 10},
        {'str': 12, 'cc': 12, 'cd': 12, 'int': 12, 'as': 12},
    ),
    'epic': (
        {'str': 15, 'cd': 10, 'as': 1}, {'str': 20, 'cd': 15, 'as': 2},
        {'str': 25, 'cd': 20, 'as': 4}, {'str': 32, 'cd': 27, 'as': 7},
        {'str': 40, 'cd': 35, 'as': 10}, {'str': 50, 'cd': 45, 'as': 15},
    ),
    'sharp': (
        {'cc': 10, 'cd': 20}, {'cc': 12, 'cd': 30}, {'cc': 14, 'cd': 40},
        {'cc': 17, 'cd': 55}, {'cc': 20, 'cd': 75}, {'cc': 25, 'cd': 90},
    ),
    'heroic': (
        {'str': 15, 'int': 40, 'as': 1}, {'str': 20, 'int': 50, 'as': 2},
        {'str': 25, 'int': 65, 'as': 2}, {'str': 32, 'int': 80, 'as': 3},
        {'str': 40, 'int': 100, 'as': 5}, {'str': 50, 'int': 125, 'as': 7},
    ),
    'spicy': (
        {'str': 2, 'cc': 1, 'cd': 25, 'as': 1},
        {'str': 3, 'cc': 1, 'cd': 35, 'as': 2},
        {'str': 4, 'cc': 1, 'cd': 45, 'as': 4},
        {'str': 7, 'cc': 1, 'cd': 60, 'as': 7},
        {'str': 10, 'cc': 1, 'cd': 80, 'as': 10},
        {'str': 12, 'cc': 1, 'cd': 100, 'as': 15},
    ),
    'legendary': (
        {'str': 3, 'cc': 5, 'cd': 5, 'int': 5, 'as': 2},
        {'str': 7, 'cc': 7, 'cd': 7, 'int': 8, 'as': 3},
        {'str': 12, 'cc': 9, 'cd': 9, 'int': 12, 'as': 5},
        {'str': 18, 'cc': 12, 'cd': 12, 'int': 18, 'as': 7},
        {'str': 25, 'cc': 15, 'cd': 15, 'int': 25, 'as': 10},
        {'str': 32, 'cc': 18, 'cd': 18, 'int': 35, 'as': 15},
    ),
}

REFORGES = {**SWORD_REFORGES}
