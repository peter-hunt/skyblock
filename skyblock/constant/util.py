from typing import Tuple, Union

__all__ = [
    'Amount', 'Number', 'NUMBER_SCALES', 'ROMAN_NUM',
    'SPECIAL_NAMES', 'IGNORED_WORDS',
]

Amount = Union[Tuple[int, int], int]
Number = Union[float, int]

NUMBER_SCALES = [
    ('', 1), ('K', 10 ** 3), ('M', 10 ** 6), ('B', 10 ** 9), ('T', 10 ** 12),
]

ROMAN_NUM = [
    ('I', 1), ('IV', 4), ('V', 5), ('IX', 9), ('X', 10),
    ('XL', 40), ('L', 50), ('XC', 90), ('C', 100),
    ('CD', 400), ('D', 500), ('CM', 900), ('M', 1000),
]

SPECIAL_NAMES = {
    'attack_speed': 'Bonus Attack Speed',
    'barn': 'The Barn',
    'birch': 'Birch Park',
    'builders_house': "Builder's House",
    'counter_strike': 'Counter-Strike',
    'crypt': 'Hub Crypts',
    'dark_thicket': 'Dark Thicket',
    'deep': 'Deep Caverns',
    'dragons_nest': "Dragon's Nest",
    'end': 'The End',
    'first_strike': 'First-Strike',
    'gold': 'Gold Mine',
    'jungle': 'Jungle Island',
    'necrons_blade': "Necron's Blade",
    'park': 'The Park',
    'pigmans_den': "Pigman's Den",
    'pray_rngesus': 'Pray RNGesus',
    'savanna': 'Savanna Woodland',
    'spider': "Spider's Den",
    'spruce': 'Spruce Wood',
    'ranchers_boots': "Rancher's Boots",
    'rngesus': 'RNGesus',
    'runaans_bow': "Runaan's Bow",
    'tacticians_sword': "Tactician's Sword",
    'tightly_tied_hay_bale': 'Tightly-Tied Hay Bale',
    'triple_strike': 'Triple-Strike',
}

IGNORED_WORDS = ('from', 'of', 'the', 'to')
