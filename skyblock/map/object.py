from decimal import Decimal
from dataclasses import dataclass, field
from math import dist, inf
from types import FunctionType
from typing import Dict, List, Optional, Tuple, Union

from ..function.util import format_zone
from ..object.object import *


__all__ = ['Npc', 'Zone', 'Island', 'calc_dist', 'add_dist', 'path_find']


@dataclass
class Npc:
    name: str
    init_dialog: Optional[List[str]] = None
    dialog: Optional[List[List[str]]] = None
    # price, item, amount
    trades: Optional[List[Tuple[Union[Tuple[int, ItemType], int],
                                Union[ItemType, List[ItemType]]]]] = None
    claim_item: Optional[ItemType] = None
    function: Optional[FunctionType] = None

    def __repr__(self):
        return format_zone(self.name)


@dataclass(order=True)
class Zone:
    name: str
    x: int
    z: int
    portal: Optional[str] = None
    fishable: bool = False
    npcs: List[Npc] = field(default_factory=list)
    resources: List[Resource] = field(default_factory=list)
    mobs: List[Mob] = field(default_factory=list)
    skill_req: Optional[Tuple[str, int]] = None

    def __repr__(self):
        return format_zone(self.name)

    def __hash__(self):
        return hash(self.name)


def calc_dist(zone_1: Zone, zone_2: Zone) -> Decimal:
    return round(Decimal(
        dist((zone_1.x, zone_1.z), (zone_2.x, zone_2.z))
    ), 2)


def add_dist(zone_1: Zone, zone_2: Zone, DISTS: Dict) -> None:
    DISTS[tuple(sorted((zone_1, zone_2)))] = calc_dist(zone_1, zone_2)


def path_find(start_zone: Zone, end_zone: Zone,
              conns: List, dists: Dict) -> Tuple[List, Decimal]:
    paths = []
    for conn in conns:
        if start_zone in conn:
            other_zone = conn[0] if conn[1] == start_zone else conn[1]
            if other_zone == end_zone:
                return [start_zone, end_zone], calc_dist(start_zone, end_zone)
            paths.append(  # tuple([*places], accum_dist, heuri_dist)
                ([start_zone, other_zone], dists[tuple(conn)],
                 calc_dist(other_zone, end_zone))
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
                other_zone = conn[0] if conn[1] == first_end else conn[1]
                if other_zone in first[0]:
                    continue
                path = (first[0] + [other_zone], first[1] + dists[tuple(conn)],
                        calc_dist(other_zone, end_zone))
                slower = False
                for other_path in paths:
                    if other_zone == other_path[0][-1]:
                        if path[1] >= other_path[1]:
                            slower = True
                            break
                if slower:
                    continue
                else:
                    if other_zone == end_zone:
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
                             if other_zone != other_path[0][-1]]
                    paths.append(path)

        paths = sorted(paths, key=lambda group: group[1] + group[2])
        if len(paths) == 0 and best_found == True:
            return best_path, best_dist


@dataclass
class Island:
    name: str
    spawn: str
    zones: List[Zone]
    conns: List[Tuple[Zone, Zone]]
    dists: Dict[Tuple[Zone, Zone], Decimal]
    skill_req: Optional[Tuple[str, int]] = None

    def __repr__(self):
        return format_zone(self.name)
