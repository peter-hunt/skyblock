from .colors import *


__all__ = [
    'Amount', 'Ench', 'ItemPointer', 'Number', 'NUMBER_SCALES', 'ROMAN_NUM',
    'SPECIAL_ZONES', 'SPECIAL_NAMES', 'SPECIAL_ALTER', 'IGNORED_WORDS', 'UPGRADE_ATTRS',
    'PLUS_RARITY', 'MINUS_RARITY',
]

Amount = list[int] | tuple[int, int] | int | float
Ench = dict[str, int]
ItemPointer = dict[str, any]
Number = float | int

NUMBER_SCALES = [
    ('', 1), ('k', 10 ** 3), ('m', 10 ** 6), ('b', 10 ** 9), ('t', 10 ** 12),
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

    'crimson': 'Crimson Isle',
    'ashfang_ruins': 'Ruins of Ashfang',
    'burning': 'Burning Desert',
    'dukedom': 'The Dukedom',
    'fields': 'Crimson Fields',
    'magma': 'Magma Chamber',
    'mystic': 'Mystic Marsh',
    'odgers_hut': "Odger's Hut",
    'skull': 'Forgotten Skull',
    'smoldering': 'Smoldering Tomb',
    'volcano': 'Blazing Volcano',
    'wasteland': 'The Wasteland',

    'end': 'The End',
    'drag': "Dragon's Nest",
    'void': 'Void Sepulture',

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
    'divans_alloy': "Divan's Alloy",
    'ender_artifact_upgrader': 'Exceedingly Rare Ender Artifact Upgrader',

    'millenia_old_blaze_ashes': 'Millenia-Old Blaze Ashes',
    'netherrack_looking_sunshade': 'Netherrack-Looking Sunshade',

    'diamantes_handle': "Diamante's Handle",
    'lasrs_eye': "L.A.S.R.'s Eye",
    'bigfoots_lasso': "Bigfoot's Lasso",

    # weapon
    'sinseeker_scythe': f'{DARK_RED}Sin{DARK_PURPLE}seeker Scythe',

    # gemstones
    'rough_ruby_gemstone': '❤ Rough Ruby Gemstone',
    'rough_amber_gemstone': '⸕ Rough Amber Gemstone',
    'rough_sapphire_gemstone': '✎ Rough Sapphire Gemstone',
    'rough_jade_gemstone': '☘ Rough Jade Gemstone',
    'rough_amethyst_gemstone': '❈ Rough Amethyst Gemstone',
    'rough_topaz_gemstone': '✧ Rough Topaz Gemstone',
    'rough_jasper_gemstone': '❁ Rough Jasper Gemstone',
    'rough_opal_gemstone': '❂ Rough Opal Gemstone',

    'flawed_ruby_gemstone': '❤ Flawed Ruby Gemstone',
    'flawed_amber_gemstone': '⸕ Flawed Amber Gemstone',
    'flawed_sapphire_gemstone': '✎ Flawed Sapphire Gemstone',
    'flawed_jade_gemstone': '☘ Flawed Jade Gemstone',
    'flawed_amethyst_gemstone': '❈ Flawed Amethyst Gemstone',
    'flawed_topaz_gemstone': '✧ Flawed Topaz Gemstone',
    'flawed_jasper_gemstone': '❁ Flawed Jasper Gemstone',
    'flawed_opal_gemstone': '❂ Flawed Opal Gemstone',

    'fine_ruby_gemstone': '❤ Fine Ruby Gemstone',
    'fine_amber_gemstone': '⸕ Fine Amber Gemstone',
    'fine_sapphire_gemstone': '✎ Fine Sapphire Gemstone',
    'fine_jade_gemstone': '☘ Fine Jade Gemstone',
    'fine_amethyst_gemstone': '❈ Fine Amethyst Gemstone',
    'fine_topaz_gemstone': '✧ Fine Topaz Gemstone',
    'fine_jasper_gemstone': '❁ Fine Jasper Gemstone',
    'fine_opal_gemstone': '❂ Fine Opal Gemstone',

    'flawless_ruby_gemstone': '❤ Flawless Ruby Gemstone',
    'flawless_amber_gemstone': '⸕ Flawless Amber Gemstone',
    'flawless_sapphire_gemstone': '✎ Flawless Sapphire Gemstone',
    'flawless_jade_gemstone': '☘ Flawless Jade Gemstone',
    'flawless_amethyst_gemstone': '❈ Flawless Amethyst Gemstone',
    'flawless_topaz_gemstone': '✧ Flawless Topaz Gemstone',
    'flawless_jasper_gemstone': '❁ Flawless Jasper Gemstone',
    'flawless_opal_gemstone': '❂ Flawless Opal Gemstone',

    'perfect_ruby_gemstone': '❤ Perfect Ruby Gemstone',
    'perfect_amber_gemstone': '⸕ Perfect Amber Gemstone',
    'perfect_sapphire_gemstone': '✎ Perfect Sapphire Gemstone',
    'perfect_jade_gemstone': '☘ Perfect Jade Gemstone',
    'perfect_amethyst_gemstone': '❈ Perfect Amethyst Gemstone',
    'perfect_topaz_gemstone': '✧ Perfect Topaz Gemstone',
    'perfect_jasper_gemstone': '❁ Perfect Jasper Gemstone',
    'perfect_opal_gemstone': '❂ Perfect Opal Gemstone',

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
    'necrons_handle': "Necron's Handle",
    'necrons_blade': "Necron's Blade (Unrefined)",
    'tacticians_sword': "Tactician's Sword",

    # mob
    'millenia_aged_blaze': 'Millenia-Aged Blaze',

    # armor pieces
    'rosettas_helmet': "Rosetta's Helmet",
    'rosettas_chestplate': "Rosetta's Chestplate",
    'rosettas_leggings': "Rosetta's Leggings",
    'rosettas_boots': "Rosetta's Boots",

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

    'divan_helmet': 'Helmet of Divan',
    'divan_chestplate': 'Chestplate of Divan',
    'divan_leggings': 'Leggings of Divan',
    'divan_boots': 'Boots of Divan',

    'pack_helmet': 'Helmet of the Pack',
    'pack_chestplate': 'Chestplate of the Pack',
    'pack_leggings': 'Leggings of the Pack',
    'pack_boots': 'Boots of the Pack',

    # tools
    'mithril_drill_226': 'Mithril Drill SX-R226',
    'mithril_drill_326': 'Mithril Drill SX-R326',
    'titanium_drill_355': 'Titanium Drill DR-X355',
    'titanium_drill_455': 'Titanium Drill DR-X455',
    'titanium_drill_555': 'Titanium Drill DR-X555',
    'divans_drill': "Divan's Drill",

    'ruby_drill_15': 'Ruby Drill TX-15',
    'gemstone_drill_522': 'Gemstone Drill LT-522',
    'topaz_drill_12': 'Topaz Drill KGR-12',
    'jasper_drill_10': 'Jasper Drill X',

    'farmers_rod': "Farmer's Rod",

    # reforge stones
    'necromancers_brooch': "Necromancer's Brooch",

    # rarity
    'rngesus': 'RNGesus',
    'pray_rngesus': 'Pray RNGesus',
    'rngesus_incarnate': 'RNGesus Incarnate',
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

IGNORED_WORDS = ('and', 'from', 'of', 'the', 'to')

UPGRADE_ATTRS = {
    'dye', 'enchantments', 'exp', 'floor_obtained', 'hot_potato',
    'kill_count', 'modifier', 'recombobulated', 'stars',
    'compact_count', 'cultivating_count', 'expertise_count',
}

PLUS_RARITY = {
    'common': 'uncommon',
    'uncommon': 'rare',
    'rare': 'epic',
    'epic': 'legendary',
    'legendary': 'mythic',
    'mythic': 'divine',
    'divine': 'special',
    'special': 'very_special',
    'very_special': 'very_special',
}

MINUS_RARITY = {
    'common': 'common',
    'uncommon': 'common',
    'rare': 'uncommon',
    'epic': 'rare',
    'legendary': 'epic',
    'mythic': 'legendary',
    'divine': 'mythic',
    'special': 'divine',
    'very_special': 'special',
}
