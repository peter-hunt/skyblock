from ..item.item import get_item
from ..item.mob import get_mob
from ..item.object import Item
from ..item.resource import get_resource

from .object import Island, Npc, Region, add_dist

__all__ = ['ISLANDS']


AUCTION_HOUSE = Region('auction_house', -18, -90)
BANK = Region('bank', -20, -65)
BAZAAR_ALLEY = Region(
    'bazaar_alley', -32, -76,
    npcs=[
        Npc('adventurer',
            init_dialog=[
                ("I've seen it all - every island"
                 " from here to the edge of the world!"),
                ("Over the years I've acquired"
                 " a variety of Talismans and Artifacts."),
                'For a price, you can have it all!',
                'Talk to me again to open the Adventurer Shop!',
            ],
            trades=[
                (8, Item('rotten_flesh')),
                (8, Item('bone')),
                (10, Item('string')),
                (14, Item('slime_ball')),
                (10, Item('gunpowder')),
            ]),
        Npc('lumber_merchant',
            init_dialog=[
                'Buy and sell wood and axes with me!',
                'Talk to me again to open the Lumberjack Shop!',
            ],
            trades=[
                (5, Item('oak_wood')),
                (5, Item('birch_wood')),
                (5, Item('spruce_wood')),
                (5, Item('dark_oak_wood')),
                (5, Item('acacia_wood')),
                (5, Item('jungle_wood')),
                (12, Item('rookie_axe')),
                (35, Item('promising_axe')),
                (100, Item('sweet_axe')),
                (100, Item('efficient_axe')),
            ]),
    ],
)
BLACKSMITH = Region('blacksmith', -28, -125)
BUILDERS_HOUSE = Region(
    'builders_house', -50, -36,
    npcs=[
        Npc('builder',
            init_dialog=[
                'If you build, they will come!',
                'Talk to me again to open the Builder Shop!',
            ],
            trades=[
                (22, Item('gravel')),
                (69, Item('obsidian')),
                (1, Item('cobblestone')),
                (1, Item('sand')),
            ]),
    ]
)
COAL_MINE = Region(
    'coal_mine', -20, -160,
    resources=[get_resource('stone'), get_resource('coal_ore')],
    portal='gold',
)
COLOSSEUM = Region('colosseum', -58, -58)
COMMUNITY_CENTER = Region('community_center', 0, -100)
FARM = Region(
    'farm', 41, -137,
    resources=[get_resource('wheat')],
    portal='barn',
)
FARMHOUSE = Region(
    'farmhouse', 23, -80,
    npcs=[
        Npc('farm_merchant',
            init_dialog=[
                'You can buy and sell harvested crops with me!',
                'Wheat, carrots, potatoes, and melon are my specialties!',
                'Talk to me again to open the Farmer Shop!',
            ],
            trades=[
                (7/3, Item('wheat')),
                (7/3, Item('carrot')),
                (7/3, Item('potato')),
                (8, Item('pumpkin')),
                (2, Item('melon')),
                (12, Item('red_mushroom')),
                (12, Item('brown_mushroom')),
                (5, Item('cocoa_beans')),
                (5, Item('sugar_cane')),
                (4, Item('sand')),
                (10, get_item('rookie_hoe')),
            ]),
        Npc('jacob',
            dialog=[[
                'Howdy!',
                'I organize farming contests once every few days!',
                'You need Farming X to participate! :)',
            ]]),
        Npc('anita'),
    ],
)
FASHION_SHOP = Region('fashion_shop', 27, -44)
FLOWER_HOUSE = Region('flower_house', -7, -25)
FOREST = Region(
    'forest', -95, -40,
    resources=[get_resource('oak')],
    portal='park',
)
GRAVEYARD = Region(
    'graveyard', -99, -54,
    mobs=[get_mob('zombie', level=1)],
    portal='spider',
)
HIGH_LEVEL = Region('high_level', 0, 150)
HUB_CRYPTS = Region('hub_crypts', -120, -100)
LIBRARY = Region('library', 37, -111)
MOUNTAIN = Region('mountain', 0, 0)
PETS_BUILDING = Region('pets_building', 24, -90)
POTION_SHOP = Region('potion_shop', 41, -63)
RUINS = Region('ruins', -250, -80)
TAVERN = Region('tavern', -85, -69)
VILLAGE = Region(
    'village', -3, -85,
    npcs=[
        Npc('armorsmith',
            init_dialog=[
                'A great warrior is nothing without their armor!',
                'Talk to me again to open the Armorsmith Shop!',
            ],
            trades=[
                (8, get_item('leather_helmet')),
                (14, get_item('leather_chestplate')),
                (16, get_item('leather_leggings')),
                (10, get_item('leather_boots')),
                (15, get_item('iron_helmet')),
                (20, get_item('iron_chestplate')),
                (30, get_item('iron_leggings')),
                (20, get_item('iron_boots')),
                (350, get_item('diamond_helmet',
                               enchantments={'growth': 1})),
                (440, get_item('diamond_chestplate',
                               enchantments={'growth': 1})),
                (400, get_item('diamond_leggings',
                               enchantments={'growth': 1})),
                (320, get_item('diamond_boots',
                               enchantments={'growth': 1})),
            ]),
        Npc('mine_merchant',
            init_dialog=[
                'My specialties are ores, stone, and mining equipment.',
                'Talk to me again to open the Miner Shop!',
            ],
            trades=[
                (4, Item('coal')),
                (5.5, Item('iron_ingot')),
                (6, Item('gold_ingot')),
                (12, get_item('rookie_pickaxe')),
                (35, get_item('promising_pickaxe')),
                (6, Item('gravel')),
                (3, Item('cobblestone')),
            ]),
        Npc('weaponsmith',
            init_dialog=[
                ("You'll need some strong weapons to survive out in the wild! "
                 "Lucky for you, I've got some!"),
                'Talk to me again to open the Weaponsmith Shop!',
            ],
            trades=[
                (100, get_item('undead_sword')),
                (150, get_item('end_sword')),
                (100, get_item('spider_sword')),
                (60, get_item('diamond_sword')),
                (25, get_item('bow')),
                (10/3, Item('arrow')),
                (250, get_item('wither_bow')),
            ]),
    ],
)
WILDERNESS = Region('wilderness', 75, -11)
WIZARD_TOWER = Region('wizard_tower', 40, 70)


HUB_JOINTS = [
    AUCTION_HOUSE, BANK, BAZAAR_ALLEY, BLACKSMITH, BUILDERS_HOUSE, COAL_MINE,
    COMMUNITY_CENTER, FARM, FARMHOUSE, FASHION_SHOP, FLOWER_HOUSE, FOREST,
    GRAVEYARD, HIGH_LEVEL, HUB_CRYPTS, LIBRARY, MOUNTAIN, PETS_BUILDING,
    POTION_SHOP, RUINS, TAVERN, VILLAGE, WILDERNESS, WIZARD_TOWER,
]

HUB_CONNS = [
    (AUCTION_HOUSE, BAZAAR_ALLEY),
    (AUCTION_HOUSE, LIBRARY),
    (AUCTION_HOUSE, VILLAGE),
    (BANK, BAZAAR_ALLEY),
    (BANK, BUILDERS_HOUSE),
    (BANK, FLOWER_HOUSE),
    (BANK, VILLAGE),
    (BAZAAR_ALLEY, BUILDERS_HOUSE),
    (BAZAAR_ALLEY, FOREST),
    (BAZAAR_ALLEY, VILLAGE),
    (BLACKSMITH, COAL_MINE),
    (BLACKSMITH, LIBRARY),
    (BLACKSMITH, VILLAGE),
    (BUILDERS_HOUSE, VILLAGE),
    (COAL_MINE, FARM),
    (COAL_MINE, GRAVEYARD),
    (COAL_MINE, VILLAGE),
    (COLOSSEUM, FARM),
    (COLOSSEUM, WILDERNESS),
    (COMMUNITY_CENTER, VILLAGE),
    (FARM, PETS_BUILDING),
    (FARM, VILLAGE),
    (FARMHOUSE, VILLAGE),
    (FASHION_SHOP, VILLAGE),
    (FLOWER_HOUSE, VILLAGE),
    (FOREST, GRAVEYARD),
    (FOREST, HIGH_LEVEL),
    (FOREST, HUB_CRYPTS),
    (FOREST, MOUNTAIN),
    (FOREST, RUINS),
    (FOREST, TAVERN),
    (FOREST, VILLAGE),
    (GRAVEYARD, HUB_CRYPTS),
    (HIGH_LEVEL, MOUNTAIN),
    (HIGH_LEVEL, RUINS),
    (HIGH_LEVEL, WILDERNESS),
    (HIGH_LEVEL, WIZARD_TOWER),
    (LIBRARY, VILLAGE),
    (MOUNTAIN, RUINS),
    (MOUNTAIN, VILLAGE),
    (MOUNTAIN, WILDERNESS),
    (MOUNTAIN, WIZARD_TOWER),
    (PETS_BUILDING, VILLAGE),
    (POTION_SHOP, VILLAGE),
    (TAVERN, VILLAGE),
    (WILDERNESS, WIZARD_TOWER),
]

HUB_DISTS = {}

for conn in HUB_CONNS:
    add_dist(*conn, HUB_DISTS)

HUB_ISLAND = Island('hub', 'village', HUB_JOINTS, HUB_CONNS, HUB_DISTS)


GOLD_GATE = Region(
    'gold_gate', 0, -300,
    npcs=[
        Npc('gold_forger',
            init_dialog=[
                'I love goooold!',
                'Talk to me again to open the Gold Forger Shop!',
            ],
            trades=[
                (5.5, Item('gold_ingot')),
                (10, get_item('golden_helmet')),
                (16, get_item('golden_chestplate')),
                (14, get_item('golden_leggings')),
                (9, get_item('golden_boots')),
                (80, get_item('fancy_sword')),
            ]),
        Npc('iron_forger',
            init_dialog=[
                "For my wares, you'll have to pay the iron price!",
                'Seriously though, I accept Coins',
                'Talk to me again to open the Iron Forger Shop!',
            ],
            trades=[
                (60, get_item('iron_pickaxe')),
                (5, Item('iron_ingot')),
                (50, get_item('chainmail_helmet')),
                (100, get_item('chainmail_chestplate')),
                (75, get_item('chainmail_leggings')),
                (100, get_item('chainmail_boots')),
            ]),
    ],
    portal='hub',
)
GOLD_MINE = Region(
    'gold_mine', 0, -360,
    resources=[get_resource('stone'), get_resource('coal_ore'),
               get_resource('iron_ore'), get_resource('gold_ore')],
    portal='deep',
)

GOLD_JOINTS = [GOLD_GATE, GOLD_MINE]
GOLD_CONNS = [
    (GOLD_GATE, GOLD_MINE),
]

GOLD_DISTS = {}

for conn in GOLD_CONNS:
    add_dist(*conn, GOLD_DISTS)

GOLD_MINE = Island(
    'gold', 'gold_gate', GOLD_JOINTS, GOLD_CONNS, GOLD_DISTS,
    skill_req=('mining', 1),
)


DEEP_ENTRENCE = Region(
    'deep_entrence', 0, 90,
    portal='gold',
)
GUNPOWDER_MINES = Region(
    'gunpowder_mines', 5, 20,
    resources=[get_resource('stone'), get_resource('coal_ore'),
               get_resource('iron_ore'), get_resource('gold_ore')],
    mobs=[get_mob('sneaky_creeper')],
)
LAPIS_QUARRY = Region(
    'lapis_quarry', -30, -35,
    resources=[get_resource('stone'), get_resource('lapis_ore')],
    mobs=[get_mob('lapis_zombie')],
)
PIGMANS_DEN = Region(
    'pigmans_den', -10, 70,
    resources=[get_resource('stone'), get_resource('redstone_ore')],
    mobs=[get_mob('redstone_pigman')],
)
SLIMEHILL = Region(
    'slilmehill', 20, -10,
    resources=[get_resource('stone'), get_resource('emerald_ore')],
    mobs=[get_mob('small_emerald_slime'),
          get_mob('medium_emerald_slime'),
          get_mob('large_emerald_slime')],
)
DIAMOND_RESERVE = Region(
    'diamond_reserve', -35, 15,
    resources=[get_resource('stone'), get_resource('diamond_ore')],
    mobs=[get_mob('diamond_zombie'),
          get_mob('diamond_skeleton')],
)
OBSIDIAN_SANCTUARY = Region(
    'obsidian_sanctuary', -10, 70,
    resources=[get_resource('stone'), get_resource('diamond_ore'),
               get_resource('diamond_block'), get_resource('obsidian')],
    mobs=[get_mob('enchanted_diamond_zombie'),
          get_mob('enchanted_diamond_skeleton')],
)
LIFT = Region(
    'lift', 50, 0,
    npcs=[
        Npc('life_operator',
            init_dialog=[
                'Hey Feller!',
                'I control this lift here behind me.',
                ("Once you've explored an area"
                 " I can give you a safe ride back there."),
                ("Be careful not to fall down the shaft though,"
                 " it's a long fall!"),
                'Good luck on your adventures.',
            ])
    ]
)

DEEP_JOINTS = [
    DEEP_ENTRENCE, DIAMOND_RESERVE, GUNPOWDER_MINES, LAPIS_QUARRY, LIFT,
    OBSIDIAN_SANCTUARY, PIGMANS_DEN, SLIMEHILL,
]
DEEP_CONNS = [
    (DIAMOND_RESERVE, LIFT),
    (DIAMOND_RESERVE, OBSIDIAN_SANCTUARY),
    (DIAMOND_RESERVE, SLIMEHILL),
    (DEEP_ENTRENCE, GUNPOWDER_MINES),
    (GUNPOWDER_MINES, LAPIS_QUARRY),
    (GUNPOWDER_MINES, LIFT),
    (LAPIS_QUARRY, PIGMANS_DEN),
    (LAPIS_QUARRY, LIFT),
    (LIFT, OBSIDIAN_SANCTUARY),
    (LIFT, PIGMANS_DEN),
    (LIFT, SLIMEHILL),
    (PIGMANS_DEN, SLIMEHILL),
]

DEEP_DISTS = {}

for conn in DEEP_CONNS:
    add_dist(*conn, DEEP_DISTS)

DEEP_CAVERNS = Island(
    'deep', 'deep_entrence', DEEP_JOINTS, DEEP_CONNS, DEEP_DISTS,
    skill_req=('mining', 5),
)


BIRCH_PARK = Region(
    'birch_park', -300, -20,
    resources=[get_resource('birch')],
    portal='hub',
)
SPRUCE_WOOD = Region(
    'spruce_wood', -325, 0,
    resources=[get_resource('spruce')],
    npcs=[
        Npc('melancholic_viking',
            init_dialog=[
                "For my wares, you'll have to pay the iron price!",
                'Seriously though, I accept Coins',
                'Talk to me again to open the Iron Forger Shop!',
            ],
            trades=[
                (130_000, get_item('raider_axe')),
            ]),
    ],
    skill_req=('foraging', 2),
)
DARK_THICKET = Region(
    'dark_thicket', -330, -45,
    resources=[get_resource('dark_oak')],
    skill_req=('foraging', 3),
)
SAVANNA_WOODLAND = Region(
    'savanna_woodland', -350, -15,
    resources=[get_resource('acacia')],
    npcs=[
        Npc('master_tactician_funk',
            trades=[
                (35_000, get_item('tacticians_sword')),
            ]),
    ],
    skill_req=('foraging', 4),
)
JUNGLE_ISLAND = Region(
    'jungle_island', -55, -60,
    resources=[get_resource('jungle')],
    skill_req=('foraging', 5),
)

PARK_JOINTS = [
    BIRCH_PARK, SPRUCE_WOOD, DARK_THICKET, SAVANNA_WOODLAND, JUNGLE_ISLAND,
]
PARK_CONNS = [
    (BIRCH_PARK, SPRUCE_WOOD),
    (DARK_THICKET, SAVANNA_WOODLAND),
    (DARK_THICKET, SPRUCE_WOOD),
    (JUNGLE_ISLAND, SAVANNA_WOODLAND),
]

PARK_DISTS = {}

for conn in PARK_CONNS:
    add_dist(*conn, PARK_DISTS)

PARK_ISLAND = Island(
    'park', 'birch', PARK_JOINTS, PARK_CONNS, PARK_DISTS,
    skill_req=('foraging', 1),
)


POTATO_FIELD = Region(
    'potato_field', 150, -245,
    resources=[
        get_resource('carrot'),
        get_resource('potato'),
    ],
)
PUMPKIN_FIELD = Region(
    'pumpkin_field', 190, -225,
    resources=[
        get_resource('melon'),
        get_resource('pumpkin'),
    ],
)
WHEAT_FIELD = Region(
    'wheat_field', 105, -220,
    resources=[get_resource('wheat')],
    portal='hub',
)

BARN_JOINTS = [POTATO_FIELD, PUMPKIN_FIELD, WHEAT_FIELD]
BARN_CONNS = [
    (POTATO_FIELD, WHEAT_FIELD),
    (POTATO_FIELD, PUMPKIN_FIELD),
    (PUMPKIN_FIELD, WHEAT_FIELD),
]

BARN_DISTS = {}

for conn in BARN_CONNS:
    add_dist(*conn, BARN_DISTS)

BARN_ISLAND = Island(
    'barn', 'wheat_field', BARN_JOINTS, BARN_CONNS, BARN_DISTS,
    skill_req=('farming', 1),
)


SPIDERS_PATH = Region(
    'spiders_path', -315, -240,
    portal='hub',
)
SPIDER_TOWER = Region('spider_tower', -365, -220)
FOSSIL = Region('fossil', -340, -255)

SPIDER_JOINTS = [SPIDERS_PATH, SPIDER_TOWER, FOSSIL]
SPIDER_CONNS = [
    (FOSSIL, SPIDERS_PATH),
    (SPIDER_TOWER, SPIDERS_PATH),
]

SPIDER_DISTS = {}

for conn in SPIDER_CONNS:
    add_dist(*conn, SPIDER_DISTS)

SPIDERS_DEN = Island(
    'spider', 'spiders_path', SPIDER_JOINTS, SPIDER_CONNS, SPIDER_DISTS,
    skill_req=('combat', 1),
)


ISLANDS = [
    HUB_ISLAND,
    GOLD_MINE,
    DEEP_CAVERNS,
    PARK_ISLAND,
    BARN_ISLAND,
    SPIDERS_DEN,
]

# for conn in sorted(tuple(sorted(_conn)) for _conn in HUB_CONNS):
#     print(f'    ({conn[0].name.upper()}, {conn[1].name.upper()}),')
