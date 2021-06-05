from ..item.mob import get_mob
from ..item.object import Item
from ..item.resource import get_resource

from .object import Island, Npc, Region, add_dist

__all__ = ['ISLANDS']


AUCTION_HOUSE = Region('auction_house', -18, -90)
BANK = Region('bank', -20, -65)
BAZAAR_ALLEY = Region('bazaar_alley', -32, -76)
BLACKSMITH = Region('blacksmith', -28, -125)
BUILDERS_HOUSE = Region('builders_house', -50, -36)
COAL_MINE = Region(
    'coal_mine', -20, -160,
    resources=[get_resource('stone'), get_resource('coal_ore')],
    portal='gold',
)
COLOSSEUM = Region('colosseum', -58, -58)
COMMUNITY_CENTER = Region('community_center', 0, -100)
FARM = Region(
    'farm', 41, -137,
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
                # (10, get_item('rookie_hoe')),
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
VILLAGE = Region('village', -3, -85)
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
    portal='hub',
)
GOLD_MINE = Region(
    'gold_mine', 0, -360,
    resources=[get_resource('stone'), get_resource('coal_ore'),
               get_resource('iron_ore'), get_resource('gold_ore')],
    # portal='deep',
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


BIRCH_PARK = Region(
    'birch_park', -300, -20,
    resources=[get_resource('birch')],
    portal='hub',
)
SPRUCE_WOOD = Region(
    'spruce_wood', -325, 0,
    resources=[get_resource('spruce')],
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


PUMPKIN_FIELD = Region('pumpkin_field', 190, -225)
WHEAT_FIELD = Region(
    'wheat_field', 105, -220,
    portal='hub',
)

BARN_JOINTS = [PUMPKIN_FIELD, WHEAT_FIELD]
BARN_CONNS = [
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
    PARK_ISLAND,
    BARN_ISLAND,
    SPIDERS_DEN,
]

# for conn in sorted(tuple(sorted(_conn)) for _conn in HUB_CONNS):
#     print(f'    ({conn[0].name.upper()}, {conn[1].name.upper()}),')
