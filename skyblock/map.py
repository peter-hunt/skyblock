from decimal import Decimal
from dataclasses import dataclass
from math import dist, inf
from typing import Dict, List, Tuple, Union
from pprint import pprint


__all__ = [
    'HUB_ISLAND',
    'VILLAGE', 'COMMUNITY_CENTER', 'FOREST', 'WASTELAND',
    'COAL_MINE', 'FARM', 'RUINS', 'WILDERNESS',
    'get', 'includes', 'path_find',
]


@dataclass(order=True)
class Region:
    name: str
    x: int
    z: int

    def __repr__(self):
        return self.name.replace('_', ' ')

    def __hash__(self):
        return hash(self.name)


def calc_dist(region_1: Region, region_2: Region) -> Decimal:
    return round(Decimal(
        dist(
            (region_1.x, region_1.z), (region_2.x, region_2.z),
        )
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
class Map:
    name: str
    spawn: str
    regions: List[Region]
    conns: List[Tuple[Region, Region]]
    dists: Dict[Tuple[Region, Region], Decimal]

    def __repr__(self):
        return self.name.replace('_', ' ')


def get(ls: List[Union[Region, Map]], name: str, default=None):
    for item in ls:
        if item.name == name:
            return item
    return default


def includes(ls: List[Union[Region, Map]], name: str):
    for item in ls:
        if item.name == name:
            return True
    return False


VILLAGE = Region('village', 0, 0)
COMMUNITY_CENTER = Region('community_center', -20, 10)
FOREST = Region('forest', 0, -50)
WASTELAND = Region('wasteland', -50, -40)
COAL_MINE = Region('coal_mine', -60, -10)
FARM = Region('farm', -50, 40)
RUINS = Region('ruins', 60, -90)
WILDERNESS = Region('wilderness', 80, 80)

HUB_JOINTS = [
    VILLAGE, COMMUNITY_CENTER, FOREST, WASTELAND,
    COAL_MINE, FARM, RUINS, WILDERNESS,
]

HUB_CONNS = [
    (COAL_MINE, FARM),
    (COAL_MINE, VILLAGE),
    (COAL_MINE, WASTELAND),
    (COMMUNITY_CENTER, VILLAGE),
    (FARM, VILLAGE),
    (FARM, WILDERNESS),
    (FOREST, RUINS),
    (FOREST, VILLAGE),
    (FOREST, WASTELAND),
    (RUINS, VILLAGE),
    (VILLAGE, WASTELAND),
    (VILLAGE, WILDERNESS),
]

HUB_DISTS = {}

for conn in HUB_CONNS:
    add_dist(*conn, HUB_DISTS)

HUB_ISLAND = Map('hub', 'village', HUB_JOINTS, HUB_CONNS, HUB_DISTS)
ISLANDS = [
    HUB_ISLAND,
]
