"""
Constants used by displaying.
"""

from typing import Tuple, Union

__all__ = [
    'Amount', 'Number', 'NUMBER_SCALES', 'ROMAN_NUM',
    'SPECIAL_NAMES', 'IGNORED_WORDS',
]

# util type notation classes
Amount = Union[Tuple[int, int], int]
Number = Union[float, int]

# used to display numbers in short
NUMBER_SCALES = [
    ('', 1), ('K', 10 ** 3), ('M', 10 ** 6), ('B', 10 ** 9), ('T', 10 ** 12),
]

# used to display numbers in roman numeral
ROMAN_NUM = [
    ('I', 1), ('IV', 4), ('V', 5), ('IX', 9), ('X', 10),
    ('XL', 40), ('L', 50), ('XC', 90), ('C', 100),
    ('CD', 400), ('D', 500), ('CM', 900), ('M', 1000),
]

# names with special translation from id to displayed name
SPECIAL_NAMES = {
    'attack_speed': 'Bonus Attack Speed',

    'counter_strike': 'Counter-Strike',
    'first_strike': 'First-Strike',
    'triple_strike': 'Triple-Strike',

    'builders_house': "Builder's House",
    'castle': 'Hub Castle',
    'crypt': 'Hub Crypts',

    'skeletons_helmet': "Skeleton's Helmet",
    'spiders_boots': "Spider's Boots",
    'ranchers_boots': "Rancher's Boots",
    'tightly_tied_hay_bale': 'Tightly-Tied Hay Bale',
    'runaans_bow': "Runaan's Bow",
    'zombies_heart': "Zombie's Heart",

    'barn': 'The Barn',

    'desert': 'Mushroom Desert',
    'jakes_house': "Jake's House",

    'gold': 'Gold Mine',

    'deep': 'Deep Caverns',
    'pigmans_den': "Pigman's Den",

    'spider': "Spider's Den",
    'nest': 'Top of Nest',

    'end': 'The End',
    'drag': "Dragon's Nest",

    'park': 'The Park',
    'birch': 'Birch Park',
    'dark': 'Dark Thicket',
    'jungle': 'Jungle Island',
    'savanna': 'Savanna Woodland',
    'spruce': 'Spruce Wood',

    'mines': 'Dwarven Mines',
    'veins': 'Cliffside Veins',
    'far': 'Far Reserve',
    'forge': 'The Forge',
    'goblins': 'Goblin Burrows',
    'mist': 'The Mist',
    'palace': 'Royal Palace',
    'ramparts': "Rampart's Quarry",
    'royal': 'Royal Mines',
    'springs': 'Lava Springs',
    'upper': 'Upper Mines',

    'giants_sword': "Giant's Sword",
    'necrons_blade': "Necron's Blade",
    'tacticians_sword': "Tactician's Sword",

    'miners_outfit_helmet': "Miner's Outfit Helmet",
    'miners_outfit_chestplate': "Miner's Outfit Chestplate",
    'miners_outfit_leggings': "Miner's Outfit Leggings",
    'miners_outfit_boots': "Miner's Outfit Boots",

    'growth_helmet': 'Helmet of Growth',
    'growth_chestplate': "Chestplate of Growth",
    'growth_leggings': "Leggings of Growth",
    'growth_boots': "Boots of Growth",

    'mithril_drill_226': 'Mithril Drill SX-R226',
    'mithril_drill_326': 'Mithril Drill SX-R326',
    'titanium_drill_355': 'Titanium Drill DR-X355',
    'titanium_drill_455': 'Titanium Drill DR-X455',
    'titanium_drill_555': 'Titanium Drill DR-X555',

    'pray_rngesus': 'Pray RNGesus',
    'rngesus': 'RNGesus',
}

# words ignored by capitalization
IGNORED_WORDS = ('from', 'of', 'the', 'to')
