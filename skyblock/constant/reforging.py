__all__ = [
    'STAT_ALIASES',
    'ACCESSORY_REFORGES', 'ARMOR_REFORGES', 'BOW_REFORGES', 'MELEE_REFORGES', 'PICKAXE_REFORGES',
    'ACCESSORY_MODIFIERS', 'ARMOR_MODIFIERS', 'BOW_MODIFIERS', 'MELEE_MODIFIERS', 'PICKAXE_MODIFIERS',
    'MODIFIERS', 'REFORGE_COST',
]

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

ACCESSORY_REFORGES = (
    'bizarre', 'itchy', 'ominous', 'pleasant', 'pretty', 'shiny', 'simple',
    'strange', 'vivid', 'godly', 'demonic', 'forceful', 'hurtful', 'keen',
    'strong', 'superior', 'unpleasant', 'zealous',
)

ACCESSORY_MODIFIERS = {
    'bizarre': (
        {'hp': 1, 'str': 1, 'cd': -1, 'int': 6},
        {'hp': 1, 'str': 2, 'cd': -2, 'int': 8},
        {'hp': 1, 'str': 2, 'cd': -2, 'int': 10},
        {'hp': 1, 'str': 3, 'cd': -3, 'int': 14},
        {'hp': 1, 'str': 5, 'cd': -5, 'int': 20},
        {'hp': 2, 'str': 7, 'cd': -7, 'int': 30},
    ),
    'itchy': (
        {'str': 1, 'cd': 3}, {'str': 1, 'cd': 4},
        {'str': 1, 'cd': 5, 'as': 1}, {'str': 2, 'cd': 7, 'as': 1},
        {'str': 3, 'cd': 10, 'as': 1}, {'str': 4, 'cd': 15, 'as': 1},
    ),
    'ominous': (
        {'hp': 1, 'def': 1, 'str': 1, 'cd': 1},
        {'hp': 1, 'def': 1, 'str': 1, 'cd': 1, 'int': 1},
        {'hp': 2, 'def': 1, 'str': 1, 'cd': 1, 'int': 2},
        {'hp': 3, 'def': 2, 'str': 2, 'cd': 1, 'int': 3},
        {'hp': 4, 'def': 3, 'str': 3, 'cd': 1, 'int': 4},
        {'hp': 5, 'def': 5, 'str': 4, 'cd': 1, 'int': 5},
    ),
    'pleasant': (
        {'def': 4}, {'def': 5}, {'def': 7},
        {'def': 10}, {'def': 15}, {'def': 20},
    ),
    'pretty': (
        {'hp': 1, 'int': 3}, {'hp': 1, 'int': 4}, {'hp': 2, 'int': 6, 'as': 1},
        {'hp': 2, 'spd': 1, 'int': 9, 'as': 1},
        {'hp': 3, 'spd': 1, 'int': 13, 'as': 1},
        {'hp': 4, 'spd': 2, 'int': 18, 'as': 1},
    ),
    'shiny': (
        {'hp': 4, 'int': 1}, {'hp': 5, 'int': 2}, {'hp': 7, 'int': 2},
        {'hp': 10, 'int': 3}, {'hp': 15, 'int': 5}, {'hp': 20, 'int': 5},
    ),
    'simple': (
        {'hp': 1, 'def': 1, 'str': 1, 'spd': 1, 'cd': 1, 'int': 1},
        {'hp': 1, 'def': 1, 'str': 1, 'spd': 1, 'cd': 1, 'int': 1},
        {'hp': 1, 'def': 1, 'str': 1, 'spd': 1, 'cd': 1, 'int': 1},
        {'hp': 1, 'def': 1, 'str': 1, 'spd': 1, 'cd': 1, 'int': 1},
        {'hp': 1, 'def': 1, 'str': 1, 'spd': 1, 'cd': 1, 'int': 1},
        {'hp': 1, 'def': 2, 'str': 1, 'spd': 1, 'cd': 1, 'int': 1},
    ),
    'strange': (
        {'str': 2, 'spd': 1, 'cd': 1, 'int': 1, 'as': -1},
        {'def': 3, 'str': 1, 'cd': 1, 'int': -1, 'as': 3},
        {'def': 2, 'str': -1, 'spd': 1, 'int': 2},
        {'def': -1, 'str': 3, 'cd': 1, 'as': 4},
        {'def': 1, 'spd': 3, 'cd': 7, 'int': 8},
        {'def': 1, 'str': 4, 'spd': 3, 'cd': 9, 'int': 11, 'as': 5},
    ),
    'vivid': (
        {'hp': 1, 'spd': 1}, {'hp': 2, 'spd': 2}, {'hp': 3, 'spd': 3},
        {'hp': 4, 'spd': 4}, {'hp': 5, 'spd': 5}, {'hp': 6, 'spd': 6},
    ),
    'godly': (
        {'str': 1, 'cd': 2, 'int': 1}, {'str': 2, 'cd': 2, 'int': 1},
        {'str': 3, 'cd': 3, 'int': 1}, {'str': 5, 'cd': 4, 'int': 2},
        {'str': 7, 'cd': 6, 'int': 4}, {'str': 10, 'cd': 8, 'int': 6},
    ),
    'demonic': (
        {'str': 1, 'int': 5}, {'str': 2, 'int': 7}, {'str': 2, 'int': 9},
        {'str': 3, 'int': 12}, {'str': 5, 'int': 17}, {'str': 7, 'int': 24},
    ),
    'forceful': (
        {'str': 4}, {'str': 5}, {'str': 7},
        {'str': 10}, {'str': 15}, {'str': 20},
    ),
    'hurtful': (
        {'cd': 4}, {'cd': 5}, {'cd': 7},
        {'cd': 10}, {'cd': 15}, {'cd': 20},
    ),
    'keen': (
        {'hp': 1, 'def': 1, 'int': 1}, {'hp': 2, 'def': 2, 'int': 2},
        {'hp': 3, 'def': 3, 'int': 3}, {'hp': 4, 'def': 4, 'int': 4},
        {'hp': 5, 'def': 5, 'int': 5}, {'hp': 7, 'def': 7, 'int': 7},
    ),
    'strong': (
        {'str': 1, 'cd': 1}, {'str': 2, 'cd': 2},
        {'def': 1, 'str': 3, 'cd': 3}, {'def': 2, 'str': 5, 'cd': 5},
        {'def': 3, 'str': 8, 'cd': 8}, {'def': 4, 'str': 12, 'cd': 12},
    ),
    'superior': (
        {'str': 2, 'cd': 2}, {'str': 3, 'cd': 2}, {'str': 4, 'cd': 2},
        {'str': 5, 'cd': 3}, {'str': 7, 'cd': 3}, {'str': 10, 'cd': 5},
    ),
    'unpleasant': (
        {'cc': 1}, {'cc': 1}, {'cc': 1}, {'cc': 2}, {'cc': 2}, {'cc': 3},
    ),
    'zealous': (
        {'str': 1, 'cd': 1, 'int': 1},
        {'str': 2, 'cd': 2, 'int': 2},
        {'str': 2, 'spd': 1, 'cd': 2,  'int': 2},
        {'str': 3, 'spd': 1, 'cd': 3,  'int': 3},
        {'str': 5, 'spd': 1, 'cd': 5,  'int': 5},
        {'str': 7, 'spd': 2, 'cd': 7,  'int': 7},
    ),

    'silky': (
        {'cd': 5}, {'cd': 6}, {'cd': 8}, {'cd': 10}, {'cd': 15}, {'cd': 20},
    ),
    'bloody': (
        {'str': 1, 'spd': 1, 'cd': 3, 'as': 1},
        {'str': 1, 'spd': 1, 'cd': 4, 'as': 1},
        {'str': 1, 'spd': 1, 'cd': 5, 'as': 1},
        {'str': 2, 'spd': 1, 'cd': 6, 'as': 2},
        {'str': 3, 'spd': 1, 'cd': 9, 'as': 2},
        {'str': 4, 'spd': 1, 'cd': 14, 'as': 2},
    ),
    'shaded': (
        {'str': 2, 'cd': 3}, {'str': 3, 'cd': 4},
        {'str': 4, 'cd': 5}, {'str': 5, 'cd': 6},
        {'str': 6, 'cc': 1, 'cd': 9}, {'str': 8, 'cc': 1, 'cd': 14},
    ),
    'sweet': (
        {'hp': 3, 'def': 1, 'spd': 1}, {'hp': 4, 'def': 1, 'spd': 1},
        {'hp': 6, 'def': 2, 'spd': 2}, {'hp': 8, 'def': 3, 'spd': 2},
        {'hp': 12, 'def': 4, 'spd': 3}, {'hp': 16, 'def': 4, 'spd': 4},
    ),
}

ARMOR_REFORGES = (
    'clean', 'fierce', 'heavy', 'light', 'mythic', 'pure', 'smart', 'titanic',
    'wise',
)

ARMOR_MODIFIERS = {
    'clean': (
        {'hp': 5, 'def': 5, 'cc': 2}, {'hp': 7, 'def': 7, 'cc': 4},
        {'hp': 10, 'def': 10, 'cc': 6}, {'hp': 15, 'def': 15, 'cc': 8},
        {'hp': 20, 'def': 20, 'cc': 10}, {'hp': 25, 'def': 25, 'cc': 12},
    ),
    'fierce': (
        {'str': 2, 'cc': 2, 'cd': 4}, {'str': 4, 'cc': 3, 'cd': 7},
        {'str': 6, 'cc': 4, 'cd': 10}, {'str': 8, 'cc': 5, 'cd': 14},
        {'str': 10, 'cc': 6, 'cd': 18}, {'str': 12, 'cc': 8, 'cd': 24},
    ),
    'heavy': (
        {'def': 25, 'spd': -1, 'cd': -1}, {'def': 35, 'spd': -1, 'cd': -2},
        {'def': 50, 'spd': -1, 'cd': -2}, {'def': 65, 'spd': -1, 'cd': -3},
        {'def': 80, 'spd': -1, 'cd': -5}, {'def': 110, 'spd': -1, 'cd': -7},
    ),
    'light': (
        {'hp': 5, 'def': 1, 'spd': 1, 'cc': 1, 'cd': 1, 'as': 1},
        {'hp': 7, 'def': 2, 'spd': 2, 'cc': 1, 'cd': 2, 'as': 2},
        {'hp': 10, 'def': 3, 'spd': 3, 'cc': 2, 'cd': 3, 'as': 3},
        {'hp': 15, 'def': 4, 'spd': 4, 'cc': 2, 'cd': 4, 'as': 4},
        {'hp': 20, 'def': 5, 'spd': 5, 'cc': 3, 'cd': 5, 'as': 5},
        {'hp': 25, 'def': 6, 'spd': 6, 'cc': 3, 'cd': 6, 'as': 6},
    ),
    'mythic': (
        {'hp': 2, 'def': 2, 'str': 2, 'spd': 2, 'cc': 1, 'int': 20},
        {'hp': 4, 'def': 4, 'str': 4, 'spd': 2, 'cc': 2, 'int': 25},
        {'hp': 6, 'def': 6, 'str': 6, 'spd': 2, 'cc': 3, 'int': 30},
        {'hp': 8, 'def': 8, 'str': 8, 'spd': 2, 'cc': 4, 'int': 40},
        {'hp': 10, 'def': 10, 'str': 10, 'spd': 2, 'cc': 5, 'int': 50},
        {'hp': 12, 'def': 12, 'str': 12, 'spd': 2, 'cc': 6, 'int': 60},
    ),
    'pure': (
        {'hp': 2, 'def': 2, 'str': 2, 'spd': 1,
         'cc': 2, 'cd': 2, 'as': 1, 'int': 2},
        {'hp': 3, 'def': 3, 'str': 3, 'spd': 1,
         'cc': 4, 'cd': 3, 'as': 1, 'int': 3},
        {'hp': 4, 'def': 4, 'str': 4, 'spd': 1,
         'cc': 6, 'cd': 4, 'as': 2, 'int': 4},
        {'hp': 6, 'def': 6, 'str': 6, 'spd': 1,
         'cc': 8, 'cd': 6, 'as': 3, 'int': 6},
        {'hp': 8, 'def': 8, 'str': 8, 'spd': 1,
         'cc': 10, 'cd': 8, 'as': 4, 'int': 8},
        {'hp': 10, 'def': 10, 'str': 10, 'spd': 1,
         'cc': 12, 'cd': 8, 'as': 5, 'int': 10},
    ),
    'smart': (
        {'hp': 4, 'def': 4, 'int': 20}, {'hp': 6, 'def': 6, 'int': 40},
        {'hp': 9, 'def': 9, 'int': 60}, {'hp': 12, 'def': 12, 'int': 80},
        {'hp': 15, 'def': 15, 'int': 100}, {'hp': 20, 'def': 20, 'int': 120},
    ),
    'titanic': (
        {'hp': 10, 'def': 10}, {'hp': 15, 'def': 15}, {'hp': 20, 'def': 20},
        {'hp': 25, 'def': 25}, {'hp': 35, 'def': 35}, {'hp': 50, 'def': 50},
    ),
    'wise': (
        {'hp': 6, 'spd': 1, 'int': 25}, {'hp': 8, 'spd': 1, 'int': 50},
        {'hp': 10, 'spd': 1, 'int': 75}, {'hp': 12, 'spd': 2, 'int': 100},
        {'hp': 15, 'spd': 2, 'int': 125}, {'hp': 20, 'spd': 3, 'int': 150},
    ),

    'perfect': (
        {'def': 25}, {'def': 35}, {'def': 50},
        {'def': 65}, {'def': 80}, {'def': 110},
    ),
    'necrotic': (
        {'int': 30}, {'int': 60}, {'int': 90},
        {'int': 120}, {'int': 150}, {'int': 200},
    ),
    'ancient': (
        {'hp': 7, 'def': 7, 'str': 4, 'cc': 3, 'int': 6},
        {'hp': 7, 'def': 7, 'str': 8, 'cc': 5, 'int': 9},
        {'hp': 7, 'def': 7, 'str': 12, 'cc': 7, 'int': 12},
        {'hp': 7, 'def': 7, 'str': 18, 'cc': 9, 'int': 16},
        {'hp': 7, 'def': 7, 'str': 25, 'cc': 12, 'int': 20},
        {'hp': 7, 'def': 7, 'str': 35, 'cc': 15, 'int': 25},
    ),
    'spiked': (
        {'hp': 2, 'def': 2, 'str': 3, 'spd': 1,
         'cc': 2, 'cd': 2, 'as': 1, 'int': 3},
        {'hp': 3, 'def': 3, 'str': 4, 'spd': 1,
         'cc': 4, 'cd': 3, 'as': 1, 'int': 4},
        {'hp': 4, 'def': 4, 'str': 6, 'spd': 1,
         'cc': 6, 'cd': 6, 'as': 2, 'int': 6},
        {'hp': 6, 'def': 6, 'str': 8, 'spd': 1,
         'cc': 8, 'cd': 8, 'as': 3, 'int': 8},
        {'hp': 8, 'def': 8, 'str': 10, 'spd': 1,
         'cc': 10, 'cd': 10, 'as': 4, 'int': 10},
        {'hp': 10, 'def': 10, 'str': 12, 'spd': 1,
         'cc': 12, 'cd': 12, 'as': 5, 'int': 12},
    ),
    'renowned': (
        {'hp': 2, 'def': 2, 'str': 3, 'spd': 1,
         'cc': 2, 'cd': 3, 'as': 1, 'int': 3},
        {'hp': 3, 'def': 3, 'str': 4, 'spd': 1,
         'cc': 4, 'cd': 4, 'as': 1, 'int': 4},
        {'hp': 4, 'def': 4, 'str': 6, 'spd': 1,
         'cc': 6, 'cd': 6, 'as': 2, 'int': 6},
        {'hp': 6, 'def': 6, 'str': 8, 'spd': 1,
         'cc': 8, 'cd': 8, 'as': 3, 'int': 8},
        {'hp': 8, 'def': 8, 'str': 10, 'spd': 1,
         'cc': 10, 'cd': 10, 'as': 4, 'int': 10},
        {'hp': 10, 'def': 10, 'str': 12, 'spd': 1,
         'cc': 12, 'cd': 12, 'as': 5, 'int': 12},
    ),
    'cubic': (
        {'hp': 5, 'str': 3}, {'hp': 7, 'str': 5}, {'hp': 10, 'str': 7},
        {'hp': 15, 'str': 10}, {'hp': 20, 'str': 12}, {'hp': 25, 'str': 15},
    ),
    'warped': (
        {'str': 2, 'spd': 1, 'as': 2}, {'str': 4, 'spd': 1, 'as': 3},
        {'str': 6, 'spd': 2, 'as': 4}, {'str': 7, 'spd': 2, 'as': 5},
        {'str': 10, 'spd': 3, 'as': 6}, {'str': 12, 'spd': 3, 'as': 7},
    ),
    'reinforced': (
        {'def': 25}, {'def': 35}, {'def': 50},
        {'def': 65}, {'def': 80}, {'def': 110},
    ),
    'loving': (
        {'hp': 4, 'def': 4, 'int': 20}, {'hp': 5, 'def': 5, 'int': 40},
        {'hp': 6, 'def': 6, 'int': 60}, {'hp': 8, 'def': 8, 'int': 80},
        {'hp': 10, 'def': 10, 'int': 100}, {'hp': 14, 'def': 14, 'int': 120},
    ),
    'ridiculous': (
        {'hp': 10, 'def': 10, 'cc': 1}, {'hp': 15, 'def': 15, 'cc': 2},
        {'hp': 20, 'def': 20, 'cc': 3}, {'hp': 25, 'def': 25, 'cc': 4},
        {'hp': 35, 'def': 35, 'cc': 5}, {'hp': 50, 'def': 50, 'cc': 6},
    ),
    'giant': (
        {'hp': 50}, {'hp': 60}, {'hp': 80},
        {'hp': 120}, {'hp': 180}, {'hp': 240},
    ),
    'submerged': (
        {'cc': 2, 'scc': 0.5}, {'cc': 4, 'scc': 0.6}, {'cc': 6, 'scc': 0.7},
        {'cc': 8, 'scc': 0.8}, {'cc': 10, 'scc': 0.9}, {'cc': 12, 'scc': 1},
    ),
}

BOW_REFORGES = (
    'deadly', 'fine', 'grand', 'hasty', 'neat',
    'rapid', 'unreal', 'awkward', 'rich',
)

BOW_MODIFIERS = {
    'deadly': (
        {'cc': 10, 'cd': 5}, {'cc': 13, 'cd': 10}, {'cc': 16, 'cd': 18},
        {'cc': 19, 'cd': 32}, {'cc': 22, 'cd': 50}, {'cc': 25, 'cd': 78},
    ),
    'fine': (
        {'str': 3, 'cc': 5, 'cd': 2}, {'str': 7, 'cc': 7, 'cd': 4},
        {'str': 12, 'cc': 9, 'cd': 7}, {'str': 18, 'cc': 12, 'cd': 10},
        {'str': 25, 'cc': 15, 'cd': 15}, {'str': 33, 'cc': 18, 'cd': 20},
    ),
    'grand': (
        {'str': 25}, {'str': 32}, {'str': 40},
        {'str': 50}, {'str': 60}, {'str': 75},
    ),
    'hasty': (
        {'str': 3, 'cc': 20}, {'str': 5, 'cc': 25}, {'str': 7, 'cc': 30},
        {'str': 10, 'cc': 40}, {'str': 15, 'cc': 50}, {'str': 20, 'cc': 75},
    ),
    'neat': (
        {'cc': 10, 'cd': 4, 'int': 3}, {'cc': 12, 'cd': 8, 'int': 6},
        {'cc': 14, 'cd': 14, 'int': 10}, {'cc': 17, 'cd': 20, 'int': 15},
        {'cc': 20, 'cd': 20, 'int': 30}, {'cc': 25, 'cd': 25, 'int': 40},
    ),
    'rapid': (
        {'str': 2, 'cd': 35}, {'str': 3, 'cd': 45}, {'str': 4, 'cd': 55},
        {'str': 7, 'cd': 65}, {'str': 10, 'cd': 75}, {'str': 15, 'cd': 90},
    ),
    'unreal': (
        {'str': 3, 'cc': 8, 'cd': 5}, {'str': 7, 'cc': 9, 'cd': 10},
        {'str': 12, 'cc': 10, 'cd': 18}, {'str': 18, 'cc': 11, 'cd': 32},
        {'str': 25, 'cc': 13, 'cd': 50}, {'str': 34, 'cc': 15, 'cd': 70},
    ),
    'awkward': (
        {'cc': 10, 'cd': 5, 'int': -5}, {'cc': 12, 'cd': 10, 'int': -10},
        {'cc': 15, 'cd': 15, 'int': -18}, {'cc': 20, 'cd': 22, 'int': -32},
        {'cc': 25, 'cd': 30, 'int': -50}, {'cc': 30, 'cd': 35, 'int': -72},
    ),
    'rich': (
        {'str': 2, 'cc': 10, 'cd': 1, 'int': 20},
        {'str': 3, 'cc': 12, 'cd': 2, 'int': 25},
        {'str': 4, 'cc': 14, 'cd': 4, 'int': 30},
        {'str': 7, 'cc': 17, 'cd': 7, 'int': 40},
        {'str': 10, 'cc': 20, 'cd': 10, 'int': 50},
        {'str': 15, 'cc': 25, 'cd': 15, 'int': 60},
    ),

    'precise': (
        {'str': 3, 'cc': 8, 'cd': 5}, {'str': 7, 'cc': 9, 'cd': 10},
        {'str': 12, 'cc': 10, 'cd': 18}, {'str': 18, 'cc': 11, 'cd': 32},
        {'str': 25, 'cc': 13, 'cd': 50}, {'str': 34, 'cc': 15, 'cd': 70},
    ),
    'spiritual': (
        {'str': 4, 'cc': 7, 'cd': 10}, {'str': 8, 'cc': 8, 'cd': 15},
        {'str': 14, 'cc': 9, 'cd': 23}, {'str': 20, 'cc': 10, 'cd': 37},
        {'str': 28, 'cc': 12, 'cd': 55}, {'str': 38, 'cc': 14, 'cd': 75},
    ),
    'headstrong': (
        {'str': 2, 'cc': 10, 'cd': 4}, {'str': 5, 'cc': 11, 'cd': 8},
        {'str': 10, 'cc': 12, 'cd': 16}, {'str': 16, 'cc': 13, 'cd': 18},
        {'str': 23, 'cc': 15, 'cd': 42}, {'str': 33, 'cc': 17, 'cd': 60},
    ),
}

MELEE_REFORGES = (
    'gentle', 'odd', 'fast', 'fair', 'epic',
    'sharp', 'heroic', 'spicy', 'legendary',
)

MELEE_MODIFIERS = {
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

    'dirty': (
        {'str': 2, 'as': 2, 'fer': 2}, {'str': 4, 'as': 3, 'fer': 3},
        {'str': 6, 'as': 5, 'fer': 6}, {'str': 10, 'as': 10, 'fer': 9},
        {'str': 12, 'as': 15, 'fer': 12}, {'str': 15, 'as': 20, 'fer': 15},
    ),
    'fabled': (
        {'str': 30, 'cd': 15}, {'str': 35, 'cd': 20},
        {'str': 40, 'cd': 25}, {'str': 50, 'cd': 32},
        {'str': 60, 'cd': 40}, {'str': 75, 'cd': 50},
    ),
    'suspicious': (
        {'cc': 1, 'cd': 30}, {'cc': 2, 'cd': 40},
        {'cc': 3, 'cd': 50}, {'cc': 5, 'cd': 65},
        {'cc': 7, 'cd': 85}, {'cc': 10, 'cd': 110},
    ),
    'withered': (
        {'str': 60}, {'str': 75}, {'str': 90},
        {'str': 110}, {'str': 135}, {'str': 170},
    ),
}

PICKAXE_REFORGES = (
    'ambered', 'auspicious', 'fleet', 'fruitful', 'magnetic', 'mithraic', 'refined',
)

PICKAXE_MODIFIERS = {
    'ambered': (
        {'min_spd': 25}, {'min_spd': 31}, {'min_spd': 38},
        {'min_spd': 46}, {'min_spd': 55}, {'min_spd': 65},
    ),
    'auspicious': (
        {'min_spd': 7, 'min_ftn': 8}, {'min_spd': 14, 'min_ftn': 8},
        {'min_spd': 23, 'min_ftn': 8}, {'min_spd': 34, 'min_ftn': 8},
        {'min_spd': 45, 'min_ftn': 8}, {'min_spd': 60, 'min_ftn': 8},
    ),
    'fleet': (
        {'min_spd': 9}, {'min_spd': 15}, {'min_spd': 25},
        {'min_spd': 40}, {'min_spd': 55}, {'min_spd': 75},
    ),
    'fruitful': (
        {'def': 3, 'int': 1, 'min_ftn': 3},
        {'def': 4, 'int': 1, 'min_ftn': 3},
        {'def': 5, 'int': 1, 'min_ftn': 3},
        {'def': 7, 'int': 1, 'min_ftn': 3},
        {'def': 9, 'int': 1, 'min_ftn': 3},
        {'def': 12, 'int': 1, 'min_ftn': 3},
    ),
    'magnetic': (
        {'def': 4}, {'def': 5}, {'def': 6},
        {'def': 8}, {'def': 10}, {'def': 14},
    ),
    'mithraic': (
        {'min_spd': 6}, {'min_spd': 12}, {'min_spd': 20},
        {'min_spd': 30}, {'min_spd': 40}, {'min_spd': 70},
    ),
    'refined': (
        {'def': 5}, {'def': 7}, {'def': 9},
        {'def': 13}, {'def': 16}, {'def': 20},
    ),
    'heated': ({}, {}, {}, {}, {}, {}),
}

MODIFIERS = {**ACCESSORY_MODIFIERS, **ARMOR_MODIFIERS,
             **BOW_MODIFIERS, **MELEE_MODIFIERS, **PICKAXE_MODIFIERS}

REFORGE_COST = (250, 500, 1_000, 2_500, 5_000, 10_000)
