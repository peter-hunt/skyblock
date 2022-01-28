from ...object.mobs import get_mob
from ...object.resources import get_resource

from ..npc import get_npc
from ..object import *


__all__ = ['HUB']

AUCTION_HOUSE = Zone('auction_house', -18, -90)
BANK = Zone(
    'bank', -20, -65,
    npcs=[get_npc('banker')],
)
BAZAAR_ALLEY = Zone(
    'bazaar_alley', -32, -76,
    npcs=[get_npc('adventurer'), get_npc('lumber_merchant')],
)
BLACKSMITH = Zone(
    'blacksmith', -28, -125,
    npcs=[get_npc('blacksmith'), get_npc('smithmonger')],
)
BUILDERS_HOUSE = Zone(
    'builders_house', -50, -36,
    npcs=[get_npc('builder')],
)
COAL_MINE = Zone(
    'coal_mine', -20, -160, portal='gold',
    resources=[get_resource('stone'), get_resource('coal_ore')],
)
COLOSSEUM = Zone('colosseum', -58, -58)
COMMUNITY_CENTER = Zone(
    'community_center', 0, -100,
    npcs=[get_npc('elizabeth')],
)
CRYPT = Zone(
    'crypt', -120, -100,
    mobs=[get_mob('crypt_ghoul'), get_mob('golden_ghoul')],
)
FARM = Zone(
    'farm', 41, -137, portal='barn', fishable=True,
    resources=[get_resource('wheat')],
)
FARMHOUSE = Zone(
    'farmhouse', 23, -80,
    npcs=[get_npc('anita'), get_npc('farm_merchant'), get_npc('jacob')],
)
FASHION_SHOP = Zone(
    'fashion_shop', 27, -44,
    npcs=[get_npc('seymour'), get_npc('taylor')],
)
FLOWER_HOUSE = Zone(
    'flower_house', -7, -25,
    resources=[get_resource('dandelion'), get_resource('poppy')],
)
FOREST = Zone(
    'forest', -95, -40, portal='park',
    resources=[get_resource('oak_log')],
)
GRAVEYARD = Zone(
    'graveyard', -99, -54, portal='spider',
    npcs=[get_npc('pat')],
    mobs=[get_mob('zombie', level=1), get_mob('zombie_villager')],
)
HIGH_LEVEL = Zone(
    'high_level', 0, 150,
    mobs=[get_mob('skeleton', level=6)],
)
HUB_CASTLE = Zone(
    'castle', -280, -60,
    npcs=[get_npc('lonely_philosopher')],
    mobs=[get_mob('wolf'), get_mob('old_wolf')],
)
LIBRARY = Zone(
    'library', 37, -111,
    npcs=[get_npc('librarian')],
)
MOUNTAIN = Zone('mountain', 0, 0, fishable=True)
PETS_BUILDING = Zone(
    'pets_building', 24, -90,
    npcs=[get_npc('bea')],
)
POTION_SHOP = Zone(
    'potion_shop', 41, -63,
    resources=[get_resource('nether_wart')],
    npcs=[get_npc('alchemist')],
)
RUINS = Zone(
    'ruins', -250, -80, fishable=True,
    mobs=[get_mob('wolf'), get_mob('old_wolf')],
)
TAVERN = Zone('tavern', -85, -69)
VILLAGE = Zone(
    'village', -3, -85, fishable=True,
    npcs=[get_npc('andrew'), get_npc('armorsmith'), get_npc('duke'),
          get_npc('fish_merchant'), get_npc('jack'), get_npc('jamie'),
          get_npc('liam'), get_npc('mine_merchant'), get_npc('oringo'),
          get_npc('rosetta'), get_npc('ryu'), get_npc('weaponsmith')],
)
WILDERNESS = Zone('wilderness', 75, -11, fishable=True)
WIZARD_TOWER = Zone('wizard_tower', 40, 70)


HUB_JOINTS = [
    AUCTION_HOUSE, BANK, BAZAAR_ALLEY, BLACKSMITH, BUILDERS_HOUSE, COAL_MINE,
    COLOSSEUM, COMMUNITY_CENTER, FARM, FARMHOUSE, FASHION_SHOP, FLOWER_HOUSE, FOREST,
    GRAVEYARD, HIGH_LEVEL, HUB_CASTLE, CRYPT, LIBRARY, MOUNTAIN, PETS_BUILDING,
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
    (CRYPT, FOREST),
    (CRYPT, GRAVEYARD),
    (FARM, PETS_BUILDING),
    (FARM, VILLAGE),
    (FARMHOUSE, VILLAGE),
    (FASHION_SHOP, VILLAGE),
    (FLOWER_HOUSE, VILLAGE),
    (FOREST, GRAVEYARD),
    (FOREST, HIGH_LEVEL),
    (FOREST, MOUNTAIN),
    (FOREST, RUINS),
    (FOREST, TAVERN),
    (FOREST, VILLAGE),
    (HIGH_LEVEL, MOUNTAIN),
    (HIGH_LEVEL, RUINS),
    (HIGH_LEVEL, WILDERNESS),
    (HIGH_LEVEL, WIZARD_TOWER),
    (HUB_CASTLE, RUINS),
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

HUB = Island('hub', 'village', HUB_JOINTS, HUB_CONNS, HUB_DISTS)
