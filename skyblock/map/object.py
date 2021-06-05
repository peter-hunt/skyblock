from decimal import Decimal
from dataclasses import dataclass, field
from math import dist, inf
from typing import Dict, List, Optional, Tuple

from ..function.util import display_name
from ..item.object import Item, Resource, Mob


__all__ = [
    'Npc', 'Region', 'Island', 'calc_dist', 'add_dist', 'path_find',
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
    mobs: List[Mob] = field(default_factory=list)
    portal: Optional[str] = None
    skill_req: Optional[Tuple[str, int]] = None

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
    skill_req: Optional[Tuple[str, int]] = None

    def __repr__(self):
        return display_name(self.name)
