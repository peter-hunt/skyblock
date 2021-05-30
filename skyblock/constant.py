__all__ = [
    'CLN',
    'BLACK', 'RED', 'GREEN', 'YELLOW', 'BLUE', 'MAGENTA', 'CYAN', 'WHITE',

    'F_BLACK', 'F_DARK_BLUE', 'F_DARK_GREEN', 'F_DARK_AQUA', 'F_DARK_RED',
    'F_DARK_PURPLE', 'F_GOLD', 'F_GRAY', 'F_DARK_GRAY',
    'F_BLUE', 'F_GREEN', 'F_AQUA', 'F_RED', 'F_LIGHT_PURPLE',
    'F_YELLOW', 'F_WHITE',

    'SPECIAL_NAMES',
    'ROMAN_NUM', 'NUMBER_SCALES', 'EXP_LIMITS', 'SKILL_EXP', 'DUNGEON_EXP',
    'INTEREST_TABLE', 'RARITY_COLORS', 'menu_doc', 'profile_doc',
]

CLN = '\x1b[0m'
BOLD = '\x1b[1m'
BLACK = '\x1b[0;90m'
RED = '\x1b[0;91m'
GREEN = '\x1b[0;92m'
YELLOW = '\x1b[0;93m'
BLUE = '\x1b[0;94m'
MAGENTA = '\x1b[0;95m'
CYAN = '\x1b[0;96m'
WHITE = '\x1b[0;97m'

F_BLACK = '\x1b[0;38;2;0;0;0m'
F_DARK_BLUE = '\x1b[0;38;2;0;0;170m'
F_DARK_GREEN = '\x1b[0;38;2;0;170;0m'
F_DARK_AQUA = '\x1b[0;38;2;0;170;170m'
F_DARK_RED = '\x1b[0;38;2;170;0;0m'
F_DARK_PURPLE = '\x1b[0;38;2;170;0;170m'
F_GOLD = '\x1b[0;38;2;255;170;0m'
F_GRAY = '\x1b[0;38;2;170;170;170m'
F_DARK_GRAY = '\x1b[0;38;2;85;85;85m'
F_BLUE = '\x1b[0;38;2;85;85;255m'
F_GREEN = '\x1b[0;38;2;85;255;85m'
F_AQUA = '\x1b[0;38;2;85;255;255m'
F_RED = '\x1b[0;38;2;255;85;85m'
F_LIGHT_PURPLE = '\x1b[0;38;2;255;85;255m'
F_YELLOW = '\x1b[0;38;2;255;255;85m'
F_WHITE = '\x1b[0;38;2;255;255;255m'

SPECIAL_NAMES = {
    'attack_speed': 'Bonus Attack Speed',
    'builders_house': "Builder's House",
    'necrons_blade': "Necron's Blade",
}

ROMAN_NUM = [
    ('I', 1), ('IV', 4), ('V', 5), ('IX', 9), ('X', 10),
    ('XL', 40), ('L', 50), ('XC', 90), ('C', 100),
    ('CD', 400), ('D', 500), ('CM', 900), ('M', 1000),
]

NUMBER_SCALES = [
    ('', 1), ('K', 10 ** 3), ('M', 10 ** 6), ('B', 10 ** 9), ('T', 10 ** 12),
]

EXP_LIMITS = {
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

INTEREST_TABLE = {
    'starter': [
        # start, end, ratio
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

RARITY_COLORS = {
    'common': f'{BOLD}{F_WHITE}',
    'uncommon': f'{BOLD}{F_GREEN}',
    'rare': f'{BOLD}{F_BLUE}',
    'epic': f'{BOLD}{F_DARK_PURPLE}',
    'legendary': f'{BOLD}{F_GOLD}',
    'mythic': f'{BOLD}{F_LIGHT_PURPLE}',
    'supreme': f'{BOLD}{F_DARK_RED}',
    'special': f'{BOLD}{F_RED}',
    'very_special': f'{BOLD}{F_RED}',
}

menu_doc = """
> help [command]
Show this message or get command description.

> exit
> quit
Exit the menu.

> create
> new
> touch
Create a new profile.

> list
> ls
List all the profile avaliable.

> del <name>
> delete <name>
Delete a profile.

> load <name>
> open <name>
> start <name>
Load a profile and run it.
""".strip()

profile_doc = """
> exit
> quit
Exit to the menu.

> help [command]
Show this message or get command description.

> inv
> inventory
> list
> ls
List all the items in the inventory.

> info <index>
> information <index>
Display detailed informatioon about the item.

> look
Get information about the region.

> money
Display information about your money.

> deposit <coins>
Deposit coins from the purse to the bank.

> withdraw <coins>
Withdraw coins from the bank to the purse.

> goto <location>
Go to a region.

> get <resource> [amount=1] [tool=hand]
Get resources for an amount with chosen tool or hand by default.

> sell <index>
Sell the item.

> merge <from-index> <to-index>
Merge stackable items in the inventory.

> move <index-1> <index-2>
> switch <index-1> <index-2>
Switch items slot in the inventory.

> split <from-index> <to-index> <amount>
Split items to another slot.

> talkto <npc>
Talk to an npc.
""".strip()
