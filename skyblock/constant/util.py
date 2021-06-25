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
    'barn': 'The Barn',
    'birch': 'Birch Park',
    'builders_house': "Builder's House",
    'veins': 'Cliffside Veins',
    'counter_strike': 'Counter-Strike',
    'crypt': 'Hub Crypts',
    'dark_thicket': 'Dark Thicket',
    'deep': 'Deep Caverns',
    'dragons_nest': "Dragon's Nest",
    'end': 'The End',
    'far': 'Far Reserve',
    'first_strike': 'First-Strike',
    'forge': 'The Forge',
    'giants_sword': "Giant's Sword",
    'goblins': 'Goblin Burrows',
    'gold': 'Gold Mine',
    'jakes_house': "Jake's House",
    'jungle': 'Jungle Island',
    'miners_outfit_helmet': "Miner's Outfit Helmet",
    'miners_outfit_chestplate': "Miner's Outfit Chestplate",
    'miners_outfit_leggings': "Miner's Outfit Leggings",
    'miners_outfit_boots': "Miner's Outfit Boots",
    'mines': 'Dwarven Mines',
    'mist': 'The Mist',
    'necrons_blade': "Necron's Blade",
    'palace': 'Royal Palace',
    'park': 'The Park',
    'pigmans_den': "Pigman's Den",
    'pray_rngesus': 'Pray RNGesus',
    'savanna': 'Savanna Woodland',
    'skeletons_helmet': "Skeleton's Helmet",
    'spider': "Spider's Den",
    'spiders_boots': "Spider's Boots",
    'springs': 'Lava Springs',
    'spruce': 'Spruce Wood',
    'ramparts': "Rampart's Quarry",
    'ranchers_boots': "Rancher's Boots",
    'rngesus': 'RNGesus',
    'royal': 'Royal Mines',
    'runaans_bow': "Runaan's Bow",
    'tacticians_sword': "Tactician's Sword",
    'tightly_tied_hay_bale': 'Tightly-Tied Hay Bale',
    'triple_strike': 'Triple-Strike',
    'upper': 'Upper Mines',
    'zombies_heart': "Zombie's Heart",
}

# ignored word by capitalization
IGNORED_WORDS = ('from', 'of', 'the', 'to')
