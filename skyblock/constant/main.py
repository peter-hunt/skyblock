"""
Contains constants of many categories.
"""

from typing import List

__all__ = [
    'ARMOR_PARTS', 'DUNGEON_EXP', 'INTEREST_TABLE', 'SELL_PRICE',
    'SKILL_EXP', 'SKILL_LIMITS',
]


# names of armor parts used by iterating and displaying
ARMOR_PARTS = ['helmet', 'chestplate', 'leggings', 'boots']

# dungeon level exp requirements
DUNGEON_EXP = [
    (0, 0, 0),
    (1, 50, 50),
    (2, 75, 125),
    (3, 110, 235),
    (4, 160, 395),
    (5, 230, 625),
    (6, 330, 955),
    (7, 470, 1425),
    (8, 670, 2095),
    (9, 950, 3045),
    (10, 1340, 4385),
    (11, 1890, 6275),
    (12, 2665, 8940),
    (13, 3760, 12700),
    (14, 5260, 17960),
    (15, 7380, 25340),
    (16, 10300, 35640),
    (17, 14400, 50040),
    (18, 20000, 70040),
    (19, 27600, 97640),
    (20, 38000, 135640),
    (21, 52500, 188140),
    (22, 71500, 259640),
    (23, 97000, 356640),
    (24, 132000, 488640),
    (25, 180000, 668640),
    (26, 243000, 911640),
    (27, 328000, 1239640),
    (28, 445000, 1684640),
    (29, 600000, 2284640),
    (30, 800000, 3084640),
    (31, 1065000, 4149640),
    (32, 1410000, 5559640),
    (33, 1900000, 7459640),
    (34, 2500000, 9959640),
    (35, 3300000, 13259640),
    (36, 4300000, 17559640),
    (37, 5600000, 23159640),
    (38, 7200000, 30359640),
    (39, 9200000, 39559640),
    (40, 12000000, 51559640),
    (41, 15000000, 66559640),
    (42, 19000000, 85559640),
    (43, 24000000, 109559640),
    (44, 30000000, 139559640),
    (45, 38000000, 177559640),
    (46, 48000000, 225559640),
    (47, 60000000, 285559640),
    (48, 75000000, 360559640),
    (49, 93000000, 453559640),
    (50, 116250000, 569809640),
]

# balance interest table
INTEREST_TABLE = {
    'starter': [
        (0, 10_000_000, 0.02),
        (10_000_000, 15_000_000, 0.01),
    ],
    'gold': [
        (0, 10_000_000, 0.02),
        (10_000_000, 20_000_000, 0.01),
    ],
    'deluxe': [
        (0, 10_000_000, 0.02),
        (10_000_000, 20_000_000, 0.01),
        (20_000_000, 30_000_000, 0.005),
    ],
    'super_deluxe': [
        (0, 10_000_000, 0.02),
        (10_000_000, 20_000_000, 0.01),
        (20_000_000, 30_000_000, 0.005),
        (30_000_000, 50_000_000, 0.002),
    ],
    'premier': [
        (0, 10_000_000, 0.02),
        (10_000_000, 20_000_000, 0.01),
        (20_000_000, 30_000_000, 0.005),
        (30_000_000, 50_000_000, 0.002),
        (50_000_000, 160_000_000, 0.001),
    ],
}


def appender(ls: List[int]):
    def func(diff):
        ls.append(ls[-1] + diff)
    return func


FC, FU, FR, FE, FL = 1, 2, 4, 8, 16


def append_exp(dod: int, fls: int):
    if fls & FC:
        common.append(common[-1] + dod)
    if fls & FU:
        uncommon.append(uncommon[-1] + dod)
    if fls & FR:
        rare.append(rare[-1] + dod)
    if fls & FE:
        epic.append(epic[-1] + dod)
    if fls & FL:
        legendary.append(legendary[-1] + dod)


common, uncommon, rare, epic, legendary = (
    [0, 100], [0, 175], [0, 275], [0, 440], [0, 660])

append_exp(15, FU)
append_exp(25, FR)
for i in range(3):
    append_exp(10, FC)
for i in range(4):
    append_exp(15, FC)
for i in range(3):
    append_exp(20, FC | FU)
for i in range(2):
    append_exp(25, FC | FU)
for dod in range(30, 90, 10):
    for i in range(2):
        append_exp(dod, FC | FU | FR)
for dod in range(50, 90, 10):
    for i in range(2):
        append_exp(dod, FE)
for dod in range(70, 90, 10):
    for i in range(2):
        append_exp(dod, FL)
for dod in range(90, 210, 10):
    append_exp(dod, FC | FU | FR | FE | FL)
for dod in range(220, 320, 20):
    append_exp(dod, FC | FU | FR | FE | FL)
for dod in range(350, 550, 50):
    append_exp(dod, FC | FU | FR | FE | FL)
for dod in range(600, 2100, 100):
    append_exp(dod, FC | FU | FR | FE | FL)
for dod in range(2200, 5200, 200):
    append_exp(dod, FC | FU | FR | FE | FL)
for dod in range(5500, 10500, 500):
    append_exp(dod, FC | FU | FR | FE | FL)
for dod in range(11000, 21000, 1000):
    append_exp(dod, FC | FU | FR | FE | FL)
for dod in range(22000, 28000, 2000):
    append_exp(dod, FC)
for dod in range(22000, 32000, 2000):
    append_exp(dod, FU | FR | FE | FL)
for dod in range(35000, 55000, 5000):
    append_exp(dod, FU)
for dod in range(35000, 80000, 5000):
    append_exp(dod, FR)
for dod in range(35000, 105000, 5000):
    append_exp(dod, FE | FL)
for dod in range(110000, 150000, 10000):
    append_exp(dod, FL)

# derivative of culumative pet exp requirements for each level
PET_EXP_DIFF = [
    common, uncommon, rare, epic, legendary,
]

# items sell price at npc
SELL_PRICE = {
    'wheat': 1,
    'carrot': 1,
    'potato': 1,
    'pumpkin': 4,
    'melon': 0.5,
    'seeds': 0.5,
    'mushroom': 4,
    'cocoa': 3,
    'cactus': 1,
    'feather': 3,
    'leather': 3,
    'beef': 4,
    'porkchop': 5,
    'chicken': 4,
    'egg': 3,
    'mutton': 5,
    'wool': 2,
    'rabbit': 4,
    'rabbit_foot': 5,
    'rabbit_hide': 5,
    'nether_wart': 3,

    'sugar': 2,
    'paper': 2,
    'book': 12,
    'hay_bale': 9,
    'golden_carrot': 9,
    'glistering_melon': 3.5,
    'mushroom_block': 4,

    'enchanted_hay_bale': 1_300,
    'tightly_tied_hay_bale': 187_200,
    'enchanted_carrot': 160,
    'enchanted_golden_carrot': 20_608,
    'enchanted_potato': 160,
    'enchanted_baked_potato': 25_600,
    'enchanted_pumpkin': 640,
    'polished_pumpkin': 102_400,
    'enchanted_melon': 160,
    'enchanted_glistering_melon': 1_024,
    'enchanted_melon_block': 25_600,
    'enchanted_mushroom': 640,
    'enchanted_mushroom_block': 2_300,
    'enchanted_cocoa': 480,
    'enchanted_cookie': 61_472,
    'enchanted_cactus_green': 160,
    'enchanted_cactus': 25_600,
    'enchanted_sugar': 320,
    'enchanted_paper': 384,
    'enchanted_bookshelf': 2_700,
    'enchanted_sugar_cane': 512_000,
    'enchanted_feather': 480,
    'enchanted_beef': 640,
    'enchanted_leather': 1_700,
    'enchanted_pork': 800,
    'enchanted_grilled_pork': 128_000,
    'enchanted_chicken': 640,
    'enchanted_egg': 432,
    'enchanted_cake': 2_700,
    'enchanted_mutton': 800,
    'enchanted_cooked_mutton': 128_000,
    'enchanted_rabbit': 640,
    'enchanted_foot': 800,
    'enchanted_hide': 2_880,
    'enchanted_nether_wart': 480,
    'mutant_nether_wart': 76_800,

    'cobblestone': 1,
    'coal': 2,
    'iron': 3,
    'gold': 4,
    'redstone': 1,
    'lapis': 4,
    'diamond': 8,
    'emerald': 6,
    'obsidian': 9,
    'glowstone': 2,
    'gravel': 3,
    'ice': 0.5,
    'netherrack': 1,
    'sand': 2,
    'end_stone': 2,
    'mithril': 10,
    'starfall': 15,
    'titanium': 20,
    'sorrow': 13,
    'plasma': 20_000,

    'enchanted_cobblestone': 160,
    'enchanted_coal': 320,
    'enchanted_coal_block': 51_200,
    'enchanted_iron': 480,
    'enchanted_iron_block': 76_800,
    'enchanted_gold': 640,
    'enchanted_gold_block': 102_400,
    'enchanted_diamond': 1_280,
    'enchanted_diamond_block': 204_800,
    'enchanted_lapis': 160,
    'enchanted_lapis_block': 25_600,
    'enchanted_emerald': 960,
    'enchanted_emerald_block': 153_600,
    'enchanted_redstone': 160,
    'enchanted_redstone_block': 25_600,
    'enchanted_quartz': 640,
    'enchanted_quartz_block': 102_400,
    'enchanted_obsidian': 1_920,
    'enchanted_glowstone': 320,
    'enchanted_glowstone_block': 61_000,
    'enchanted_redstone_lamp': 30_720,
    'enchanted_flint': 640,
    'enchanted_ice': 80,
    'enchanted_packed_ice': 12_800,
    'enchanted_netherrack': 160,
    'enchanted_sand': 320,
    'enchanted_end_stone': 320,
    'enchanted_mithril': 1_600,
    'enchanted_titanium': 3_200,

    'treasurite': 5_000,

    'refined_diamond': 4_096,
    'refined_mithril': 256_000,
    'refined_titanium': 51_200,
    'fuel_tank': 51_000,
    'bejeweled_handle': 100,

    'rotten_flesh': 2,
    'bone': 2,
    'string': 3,
    'spider_eye': 3,
    'gunpowder': 4,
    'ender_pearl': 7,
    'ghast_tear': 16,
    'slime_ball': 5,
    'blaze_rod': 9,
    'magma_cream': 9,

    'enchanted_rotten_flesh': 320,
    'zombies_heart': 123_000,
    'enchanted_bone': 320,
    'enchanted_bone_block': 51_200,
    'enchanted_string': 576,
    'enchanted_spider_eye': 480,
    'enchanted_fermented_spider_eye': 31_000,
    'enchanted_gunpowder': 640,
    'enchanted_firework_rocket': 41_000,
    'enchanted_ender_pearl': 140,
    'enchanted_eye_of_ender': 3_520,
    'absolute_ender_pearl': 11_200,
    'enchanted_ghast_tear': 80,
    'enchanted_slime_ball': 800,
    'enchanted_slime_block': 128_000,
    'enchanted_blaze_powder': 1_440,
    'enchanted_blaze_rod': 230_400,
    'enchanted_magma_cream': 1_280,

    'oak_wood': 2,
    'birch_wood': 2,
    'spruce_wood': 2,
    'dark_oak_wood': 2,
    'acacia_wood': 2,
    'jungle_wood': 2,

    'blaze_powder': 4,

    'enchanted_ender_pearl': 140,
    'enchanted_eye_of_ender': 3_520,

    'rookie_axe': 6,
    'sweet_axe': 25,
    'efficient_axe': 25,

    'lapis_helmet': 1_000,
    'lapis_chestplate': 1_000,
    'lapis_leggings': 1_000,
    'lapis_boots': 1_000,

    'ender_helmet': 10_000,
    'ender_chestplate': 10_000,
    'ender_leggings': 10_000,
    'ender_boots': 10_000,

    'flaming_sword': 20,
}

# other level exp requirements
SKILL_EXP = [
    (0, 0, 0, 0),
    (1, 50, 50, 25),
    (2, 125, 175, 50),
    (3, 200, 375, 100),
    (4, 300, 675, 200),
    (5, 500, 1_175, 300),
    (6, 750, 1_925, 400),
    (7, 1_000, 2_925, 500),
    (8, 1_500, 4_425, 600),
    (9, 2_000, 6_425, 700),
    (10, 3_500, 9_925, 800),
    (11, 5_000, 14_925, 900),
    (12, 7_500, 22_425, 1_000),
    (13, 10_000, 32_425, 1_100),
    (14, 15_000, 47_425, 1_200),
    (15, 20_000, 67_425, 1_300),
    (16, 30_000, 97_425, 1_400),
    (17, 50_000, 147_425, 1_500),
    (18, 75_000, 222_425, 1_600),
    (19, 100_000, 322_425, 1_800),
    (20, 200_000, 522_425, 2_000),
    (21, 300_000, 822_425, 2_200),
    (22, 400_000, 1_222_425, 2_400),
    (23, 500_000, 1_722_425, 2_600),
    (24, 600_000, 2_322_425, 2_800),
    (25, 700_000, 3_022_425, 3_000),
    (26, 800_000, 3_822_425, 3_500),
    (27, 900_000, 4_722_425, 4_000),
    (28, 1_000_000, 5_722_425, 5_000),
    (29, 1_100_000, 6_822_425, 6_000),
    (30, 1_200_000, 8_022_425, 7_500),
    (31, 1_300_000, 9_322_425, 10_000),
    (32, 1_400_000, 10_722_425, 12_500),
    (33, 1_500_000, 12_222_425, 15_000),
    (34, 1_600_000, 13_822_425, 17_500),
    (35, 1_700_000, 15_522_425, 20_000),
    (36, 1_800_000, 17_322_425, 25_000),
    (37, 1_900_000, 19_222_425, 30_000),
    (38, 2_000_000, 21_222_425, 35_000),
    (39, 2_100_000, 23_322_425, 40_000),
    (40, 2_200_000, 25_522_425, 45_000),
    (41, 2_300_000, 27_822_425, 50_000),
    (42, 2_400_000, 30_222_425, 60_000),
    (43, 2_500_000, 32_722_425, 70_000),
    (44, 2_600_000, 35_322_425, 80_000),
    (45, 2_750_000, 38_072_425, 90_000),
    (46, 2_900_000, 40_972_425, 100_000),
    (47, 3_100_000, 44_072_425, 125_000),
    (48, 3_400_000, 47_472_425, 150_000),
    (49, 3_700_000, 51_172_425, 175_000),
    (50, 4_000_000, 55_172_425, 200_000),
    (51, 4_300_000, 59_472_425, 250_000),
    (52, 4_600_000, 64_072_425, 300_000),
    (53, 4_900_000, 68_972_425, 350_000),
    (54, 5_200_000, 74_172_425, 400_000),
    (55, 5_500_000, 79_672_425, 450_000),
    (56, 5_800_000, 85_472_425, 500_000),
    (57, 6_100_000, 91_572_425, 600_000),
    (58, 6_400_000, 97_972_425, 700_000),
    (59, 6_700_000, 104_672_425, 800_000),
    (60, 7_000_000, 111_672_425, 1_000_000),
]

# maximum levels for each skill
SKILL_LIMITS = {
    'farming': 60,
    'mining': 60,
    'combat': 60,
    'foraging': 60,
    'fishing': 50,
    'enchanting': 60,
    'alchemy': 50,
    'taming': 50,
    'dungeoneering': 50,
}
