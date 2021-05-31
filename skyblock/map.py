from decimal import Decimal
from dataclasses import dataclass, field
from math import dist, inf
from typing import Dict, List, Optional, Tuple

from .function.item import get_item
from .function.util import display_name
from .item.object import Item, Resource


__all__ = [
    'Npc', 'Region', 'Island',
    'HUB_ISLAND', 'path_find',
]


@dataclass
class Npc:
    name: str
    init_dialog: Optional[List[str]] = None
    dialog: Optional[List[List[str]]] = None
    trades: Optional[List[Tuple[int, Item]]] = None  # price, item
    claim_item: Optional[Item] = None  # price, item, amount

    def __repr__(self):
        return display_name(self.name)


@dataclass(order=True)
class Region:
    name: str
    x: int
    z: int
    npcs: List[Npc] = field(default_factory=list)
    resources: List[Resource] = field(default_factory=list)

    def __repr__(self):
        return display_name(self.name)

    def __hash__(self):
        return hash(self.name)


def calc_dist(region_1: Region, region_2: Region) -> Decimal:
    return round(Decimal(
        dist((region_1.x, region_1.z), (region_2.x, region_2.z))
    ), 2)


def add_dist(region_1: Region, region_2: Region, DISTS: Dict) -> None:
    DISTS[tuple(sorted((region_1, region_2)))] = calc_dist(region_1, region_2)


def path_find(start_region: Region, end_region: Region,
              conns: List, dists: Dict) -> Tuple[List, Decimal]:
    paths = []
    for conn in conns:
        if start_region in conn:
            other_region = conn[0] if conn[1] == start_region else conn[1]
            if other_region == end_region:
                return [start_region, end_region], calc_dist(start_region, end_region)
            paths.append(  # tuple([*places], accum_dist, heuri_dist)
                (
                    [start_region, other_region],
                    dists[tuple(conn)],
                    calc_dist(other_region, end_region),
                )
            )
    paths = sorted(paths, key=lambda group: group[1] + group[2])
    best_found = False
    best_path = None
    best_dist = inf
    while True:
        first, *paths = paths
        first_end = first[0][-1]
        for conn in conns:
            if first_end in conn:
                other_region = conn[0] if conn[1] == first_end else conn[1]
                if other_region in first[0]:
                    continue
                path = (
                    first[0] + [other_region],
                    first[1] + dists[tuple(conn)],
                    calc_dist(other_region, end_region),
                )
                slower = False
                for other_path in paths:
                    if other_region == other_path[0][-1]:
                        if path[1] >= other_path[1]:
                            slower = True
                            break
                if slower:
                    continue
                else:
                    if other_region == end_region:
                        if best_found and path[1] >= best_dist:
                            continue
                        best_found = True
                        best_path = path[0]
                        best_dist = path[1]
                        continue
                    elif best_found:
                        if path[1] + path[2] >= best_dist:
                            continue
                    paths = [other_path for other_path in paths
                             if other_region != other_path[0][-1]]
                    paths.append(path)

        paths = sorted(paths, key=lambda group: group[1] + group[2])
        if len(paths) == 0 and best_found == True:
            return best_path, best_dist


@dataclass
class Island:
    name: str
    spawn: str
    regions: List[Region]
    conns: List[Tuple[Region, Region]]
    dists: Dict[Tuple[Region, Region], Decimal]

    def __repr__(self):
        return display_name(self.name)


AUCTION_HOUSE = Region('auction_house', -18, -90)
BANK = Region('bank', -20, -65)
BAZAAR_ALLEY = Region('bazaar_alley', -32, -76)
BLACKSMITH = Region('blacksmith', -28, -125)
BUILDERS_HOUSE = Region('builders_house', -50, -36)
COAL_MINE = Region(
    'coal_mine', -20, -160,
    resources=[get_item('stone'), get_item('coal_ore')],
)
COLOSSEUM = Region('colosseum', -58, -58)
COMMUNITY_CENTER = Region('community_center', 0, -100)
FARM = Region('farm', 41, -137)
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
    resources=[get_item('oak')],
)
GRAVEYARD = Region('graveyard', -99, -54)
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

# for conn in sorted(tuple(sorted(_conn)) for _conn in HUB_CONNS):
#     print(f'    ({conn[0].name.upper()}, {conn[1].name.upper()}),')

HUB_DISTS = {}

for conn in HUB_CONNS:
    add_dist(*conn, HUB_DISTS)

HUB_ISLAND = Island('hub', 'village', HUB_JOINTS, HUB_CONNS, HUB_DISTS)
ISLANDS = [
    HUB_ISLAND,
]
