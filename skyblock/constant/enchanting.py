"""
Constant about enchantments, and enchanting information.
"""

__all__ = [
    'ULTIMATE_ENCHS', 'CONFLICTS', 'ENCHS', 'ENCH_LVLS', 'ENCH_REQUIREMENTS',
    'SWORD_ENCHS', 'BOW_ENCHS', 'ARMOR_ENCHS',
    'AXE_ENCHS', 'HOE_ENCHS', 'PICKAXE_ENCHS', 'FISHING_ROD_ENCHS',
]

# list of ultimate enchantments
ULTIMATE_ENCHS = [
    'bank',
    # 'chimera',
    # 'combo',
    'last_stand',
    'no_pain_no_gain',
    'one_for_all',
    'soul_eater',
    'ultimate_jerry',
]

# groups of enchantements which cannot be applied to a single item
CONFLICTS = [
    ('bane_of_arthropods', 'sharpness', 'smite'),
    ('execute', 'prosecute'),
    ('first_strike', 'triple_strike'),
    ('giant_killer', 'titan_killer'),
    ('life_steal', 'mana_steal', 'syphon'),
    ('thunderbolt', 'thunderlord'),

    # ('rejuvenate', 'respite'),
    ('blast_protection', 'fire_protection',
     'projectile_protection', 'protection'),
]

# enchantments and level costs enchanting at the table
ENCHS = [
    # name, maximum, weight, bias
    ('bane_of_arthropods', 5, 5, 5),
    # ('cleave', 5, 10, 0),
    ('critical', 5, 10, 0),
    ('cubism', 5, 10, 0),
    ('ender_slayer', 5, (10, 20, 25, 30, 40)),
    ('execute', 5, (20, 25, 30, 40, 50)),
    ('experience', 3, 15, 0),
    ('fire_aspect', 2, 15, 0),
    ('first_strike', 4, (20, 30, 40, 75)),
    ('giant_killer', 5, 10, 0),
    ('impaling', 3, 10, 20),
    ('knockback', 2, 15, 0),
    # ('lethality', 5, (20, 25, 30, 40, 50)),
    ('life_steal', 3, 5, 15),
    ('looting', 3, 15, 0),
    ('luck', 5, 10, 0),
    ('procecute', 5, (20, 25, 30, 40, 50)),
    ('scavenger', 3, 10, 0),
    ('sharpness', 5, 5, 5),
    ('smite', 5, 5, 5),
    ('syphon', 3, 5, 15),
    ('titan_killer', 5, 10, 0),
    ('thunderbolt', 5, (20, 25, 30, 40, 50)),
    ('thunderlord', 5, (20, 25, 30, 40, 50)),
    ('triple_strike', 4, (20, 30, 40, 75)),
    ('vampirism', 5, (20, 25, 30, 40, 50)),
    ('venomous', 5, (20, 25, 30, 40, 50)),

    ('chance', 3, 15, 0),
    # ('dragon_tracer', 5, 10, 0),
    ('flame', 1, 25, 0),
    ('infinite_quiver', 5, 5, 5),
    ('piercing', 1, 30, 0),
    ('power', 5, 10, 0),
    ('punch', 2, 30, 0),
    # ('snipe', 3, 5, 15),

    ('blast_protection', 5, 5, 5),
    ('fire_protection', 5, 5, 5),
    ('growth', 5, 10, 0),
    ('respiration', 3, 10, 0),
    ('thorns', 3, 15, 0),
    ('projectile_protection', 5, 5, 5),
    ('protection', 5, 5, 5),

    ('efficiency', 5, 5, 5),
    ('fortune', 3, 15, 0),
    ('harvesting', 5, 5, 0),

    ('angler', 5, 10, 0),
    ('blessing', 5, 10, 0),
    ('caster', 5, (20, 25, 30, 40, 50)),
    ('frail', 5, (20, 25, 30, 40, 50)),
    ('luck_of_the_sea', 5, 5, 5),
    ('lure', 5, 5, 5),
    ('magnet', 5, (20, 25, 30, 40, 50)),
    ('spiked_hook', 5, 10, 0),
]

ENCHS = sorted(ENCHS, key=lambda pair: pair[0])

ENCH_LVLS = {
    'bane_of_arthropods': 5,
    'cleave': 5,
    'critical': 5,
    'cubism': 5,
    'dragon_hunter': 5,
    'ender_slayer': 5,
    'execute': 5,
    'experience': 3,
    'fire_aspect': 2,
    'first_strike': 4,
    'giant_killer': 5,
    'impaling': 3,
    'knockback': 2,
    'lethality': 5,
    'life_steal': 3,
    'looting': 3,
    'luck': 5,
    'mana_steal': 3,
    'prosecute': 5,
    'scavenger': 3,
    'sharpness': 5,
    'smite': 5,
    'syphon': 3,
    'thunderbolt': 5,
    'thunderlord': 5,
    'titan_killer': 4,
    'triple_strike': 4,
    'vampirism': 5,
    'venomous': 5,
    'vicious': 3,

    'chance': 3,
    'dragon_tracer': 5,
    'flame': 1,
    'infinite_quiver': 5,
    'piercing': 1,
    'overload': 5,
    'power': 5,
    'punch': 2,
    # 'snipe': 3,

    'big_brain': 5,
    'blast_protection': 5,
    'counter_strike': 5,
    'counter_strike': 5,
    'fire_protection': 5,
    'growth': 5,
    'projectile_protection': 5,
    'protection': 5,
    'rejuvenate': 5,
    'respite': 5,
    'thorns': 3,
    'true_protection': 0,
    'smarty_pants': 5,
    'sugar_rush': 0,

    'efficiency': 5,
    'fortune': 3,
    'harvesting': 5,

    'angler': 5,
    'blessing': 5,
    'caster': 5,
    'expertise': 10,
    'frail': 5,
    'luck_of_the_sea': 5,
    'lure': 5,
    'magnet': 5,
}

# enchanting skill level requirements for certain enchantments
ENCH_REQUIREMENTS = [
    ('scavenger', 1),
    ('infinite_quiver', 2),
    ('harvesting', 2),
    ('luck', 3),
    ('cubism', 3),
    ('cleave', 4),
    ('angler', 4),
    ('life_steal', 5),
    ('growth', 5),
    # ('snipe', 6),
    ('sugar_rush', 7),
    ('giant_killer', 8),
    ('dragon_tracer', 8),
    ('blessing', 9),
    ('critical', 9),
    ('first_strike', 10),
    ('rejuvenate', 10),
    ('ender_slayer', 11),
    ('chance', 11),
    ('impaling', 12),
    ('magnet', 13),
    ('lethality', 14),
    ('frail', 14),
    ('execute', 14),
    ('thunderlord', 14),
    ('syphon', 15),
    ('caster', 15),
    ('true_protection', 15),
    ('vampirism', 15),
    ('dragon_hunter', 16),
    ('bank', 16),
    ('piercing', 17),
    ('venomous', 17),
    ('spiked_hook', 18),
    ('ultimate_jerry', 18),
    ('triple_strike', 19),
    ('thunderbolt', 20),
    ('ultimate_wise', 20),
    ('big_brain', 21),
    ('smarty_pants', 21),
    ('counter_strike', 22),
    ('respite', 23),
    ('combo', 24),
    ('prosecute', 25),
    ('vicious', 26),
    ('wisdom', 27),
    ('titan_killer', 28),
    ('no_pain_no_gain', 29),
    ('last_stand', 30),
    ('chimera', 31),
    ('rend', 32),
    ('overload', 33),  # more information needed
    ('legion', 34),
    ('swarm', 35),
    ('soul_eater', 36),
]

# list of sword enchantments (used by enchanting table)
SWORD_ENCHS = [
    'bane_of_arthropods',
    # 'cleave',
    'critical',
    'cubism',
    'ender_slayer',
    'execute',
    'experience',
    'fire_aspect',
    'first_strike',
    'giant_killer',
    'impaling',
    'lethality',
    # 'lethality',
    'life_steal',
    'looting',
    'luck',
    'procecute',
    'scavenger',
    'sharpness',
    'smite',
    'syphon',
    'titan_killer',
    'thunderbolt',
    'thunderlord',
    'triple_strike',
    'vampirism',
    'venomous',

    # 'chimera',
    # 'combo',
    'one_for_all',
    'soul_eater',
    'ultimate_jerry',
]

# list of bow enchantments (used by enchanting table)
BOW_ENCHS = [
    'chance',
    'cubism',
    # 'dragon_tracer',
    'flame',
    'impaling',
    'infinite_quiver',
    'piercing',
    # 'overload',
    'power',
    'punch',
    # 'snipe',
]

# list of armor enchantments (used by enchanting table)
ARMOR_ENCHS = [
    'big_brain',
    'blast_protection',
    'counter_strike',
    'fire_protection',
    'growth',
    'projectile_protection',
    'protection',
    'rejuvenate',
    'respite',
    'thorns',
    'true_protection',
    'smarty_pants',
    'sugar_rush',

    'last_stand',
    'no_pain_no_gain',
]

# list of axe enchantments (used by enchanting table)
AXE_ENCHS = [
    'efficiency',
]

# list of hoe enchantments (used by enchanting table)
HOE_ENCHS = [
    # 'cultivating',
    'experience',
    'harvesting',
]

# list of pickaxe enchantments (used by enchanting table)
PICKAXE_ENCHS = [
    # 'compact',
    'efficiency',
    'experience',
]

# list of fishing rod enchantments (used by enchanting table)
FISHING_ROD_ENCHS = [
    'angler',
    'blessing',
    'caster',
    'expertise',
    'frail',
    'looting',
    'luck_of_the_sea',
    'lure',
    'magnet',
    'spiked_hook',
]
