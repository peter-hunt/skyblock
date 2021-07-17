from typing import Dict, Tuple, Union


__all__ = [
    'Amount', 'Ench', 'Number', 'NUMBER_SCALES', 'ROMAN_NUM',
    'SPECIAL_ZONES', 'SPECIAL_NAMES', 'SPECIAL_ALTER', 'IGNORED_WORDS',
]

Amount = Union[Tuple[int, int], int]
Ench = Dict[str, int]
Number = Union[float, int]

NUMBER_SCALES = [
    ('', 1), ('K', 10 ** 3), ('M', 10 ** 6), ('B', 10 ** 9), ('T', 10 ** 12),
]

ROMAN_NUM = [
    ('I', 1), ('IV', 4), ('V', 5), ('IX', 9), ('X', 10),
    ('XL', 40), ('L', 50), ('XC', 90), ('C', 100),
    ('CD', 400), ('D', 500), ('CM', 900), ('M', 1000),
]

SPECIAL_ZONES = {
    'builders_house': "Builder's House",
    'castle': 'Hub Castle',
    'crypt': 'Hub Crypts',

    'barn': 'The Barn',

    'desert': 'Mushroom Desert',
    'jakes_house': "Jake's House",

    'gold': 'Gold Mine',

    'deep': 'Deep Caverns',
    'pigmans_den': "Pigman's Den",

    'spider': "Spider's Den",
    'nest': 'Top of Nest',

    'nether': 'Blazing Fortress',
    'magma': 'Magma Fields',

    'end': 'The End',
    'drag': "Dragon's Nest",

    'park': 'The Park',
    'howl': 'Howling Cave',
    'birch': 'Birch Park',
    'spruce': 'Spruce Wood',
    'dark': 'Dark Thicket',
    'savanna': 'Savanna Woodland',
    'jungle': 'Jungle Island',

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
}

# names with special translation from id to displayed name
SPECIAL_NAMES = {
    # items
    'tightly_tied_hay_bale': 'Tightly-Tied Hay Bale',

    # npcs
    'oringo': 'Oringo the Traveling Zookeeper',

    # stats
    'ehp': 'EHP',
    'attack_speed': 'Bonus Attack Speed',

    # enchantments
    'counter_strike': 'Counter-Strike',
    'first_strike': 'First-Strike',
    'triple_strike': 'Triple-Strike',

    # weapon
    'runaans_bow': "Runaan's Bow",

    'giants_sword': "Giant's Sword",
    'necrons_blade': "Necron's Blade",
    'tacticians_sword': "Tactician's Sword",

    # armor pieces
    'skeletons_helmet': "Skeleton's Helmet",
    'spiders_boots': "Spider's Boots",
    'ranchers_boots': "Rancher's Boots",
    'zombies_heart': "Zombie's Heart",

    'miners_outfit_armor': "Miner's Outfit Armor",
    'miners_outfit_helmet': "Miner's Outfit Helmet",
    'miners_outfit_chestplate': "Miner's Outfit Chestplate",
    'miners_outfit_leggings': "Miner's Outfit Leggings",
    'miners_outfit_boots': "Miner's Outfit Boots",

    'growth_armor': 'Armor of Growth',
    'growth_helmet': 'Helmet of Growth',
    'growth_chestplate': "Chestplate of Growth",
    'growth_leggings': "Leggings of Growth",
    'growth_boots': "Boots of Growth",

    'fairys_fedora': "Fairy's Fedora",
    'fairys_polo': "Fairy's Polo",
    'fairys_trousers': "Fairy's Trousers",
    'fairys_galoshes': "Fairy's Galoshes",

    'emperors_skull': "Emperor's Skull",

    'divers_armor': "Diver's Armor",
    'divers_mask': "Diver's Mask",
    'divers_shirt': "Diver's Shirt",
    'divers_trunks': "Diver's Trunks",
    'divers_boots': "Diver's Boots",

    'goldors_helmet': "Goldor's Helmet",
    'goldors_chestplate': "Goldor's Chestplate",
    'goldors_leggings': "Goldor's Leggings",
    'goldors_boots': "Goldor's Boots",

    'storms_helmet': "Storm's Helmet",
    'storms_chestplate': "Storm's Chestplate",
    'storms_leggings': "Storm's Leggings",
    'storms_boots': "Storm's Boots",

    'necrons_helmet': "Necron's Helmet",
    'necrons_chestplate': "Necron's Chestplate",
    'necrons_leggings': "Necron's Leggings",
    'necrons_boots': "Necron's Boots",

    'maxors_helmet': "Maxor's Helmet",
    'maxors_chestplate': "Maxor's Chestplate",
    'maxors_leggings': "Maxor's Leggings",
    'maxors_boots': "Maxor's Boots",

    'titans_helmet': "Titan's Helmet",
    'titans_chestplate': "Titan's Chestplate",
    'titans_leggings': "Titan's Leggings",
    'titans_boots': "Titan's Boots",

    # tools
    'mithril_drill_226': 'Mithril Drill SX-R226',
    'mithril_drill_326': 'Mithril Drill SX-R326',
    'titanium_drill_355': 'Titanium Drill DR-X355',
    'titanium_drill_455': 'Titanium Drill DR-X455',
    'titanium_drill_555': 'Titanium Drill DR-X555',

    'farmers_rod': "Farmer's Rod",

    # reforge stones
    'necromancers_brooch': "Necromancer's Brooch",

    # rarity
    'pray_rngesus': 'Pray RNGesus',
}

SPECIAL_ALTER = {
    'Wise Wise Dragon': 'Very Wise',
    'Strong Strong Dragon': 'Very Strong',
    'Superior Superior Dragon': 'Highly Superior',
    'Heavy Heavy': 'Extremely Heavy',
    'Heavy Super Heavy': 'Thicc Super Heavy',
    'Perfect Perfect': 'Absolutely Perfect',
    'Refined Refined': 'Even more Refined',
}

IGNORED_WORDS = ('from', 'of', 'the', 'to')
