from decimal import Decimal
from dataclasses import dataclass
from math import dist
from typing import Dict, List, Tuple


@dataclass
class Map:
    name: str


@dataclass(order=True)
class Joint:
    name: str
    parent: Map
    x: int
    z: int

    def __repr__(self):
        return self.name.upper()

    def __hash__(self):
        return hash((self.parent.name, self.name))


HUB_ISLAND = Map('hub')
VILLAGE = Joint('village', HUB_ISLAND, 0, 0)
COMMUNITY_CENTER = Joint('community_center', HUB_ISLAND, 10, 20)
FOREST = Joint('forest', HUB_ISLAND, -50, -20)
WASTELAND = Joint('wasteland', HUB_ISLAND, -40, 50)
COAL_MINE = Joint('coal_mine', HUB_ISLAND, -10, 60)
FARM = Joint('farm', HUB_ISLAND, 40, 50)
RUINS = Joint('ruins', HUB_ISLAND, -90, -60)
WILDERNESS = Joint('wilderness', HUB_ISLAND, 80, -80)

HUB_DISTS = {}


def calc_dist(joint_1: Joint, joint_2: Joint) -> Decimal:
    return round(Decimal(
        dist(
            (joint_1.x, joint_1.z), (joint_2.x, joint_2.z),
        )
    ), 2)


def add_dist(joint_1: Joint, joint_2: Joint, DISTS: Dict) -> None:
    DISTS[tuple(sorted((joint_1, joint_2)))] = calc_dist(joint_1, joint_2)


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

for conn in HUB_CONNS:
    add_dist(*conn, HUB_DISTS)


def path_find(start_joint: Joint, end_joint: Joint,
              conns: List, dists: Dict) -> Tuple[List, Decimal]:
    paths = []
    for conn in conns:
        if start_joint in conn:
            other_joint = conn[0] if conn[1] == start_joint else conn[1]
            paths.append(  # tuple([*places], accum_dist, heuri_dist)
                (
                    [start_joint, other_joint],
                    dists[tuple(conn)],
                    calc_dist(other_joint, end_joint),
                )
            )
    paths = sorted(paths, key=lambda group: group[1] + group[2])
    best_found = False
    best_path = paths[-1][0]
    best_dist = paths[-1][1]
    while True:
        first, *paths = paths
        first_end = first[0][-1]
        for conn in conns:
            if first_end in conn:
                other_joint = conn[0] if conn[1] == first_end else conn[1]
                if other_joint in first[0]:
                    continue
                path = (
                    first[0] + [other_joint],
                    first[1] + dists[tuple(conn)],
                    calc_dist(other_joint, end_joint),
                )
                slower = False
                for other_path in paths:
                    if other_joint == other_path[0][-1]:
                        if path[1] < other_path[1]:
                            slower = True
                            break
                if slower:
                    continue
                else:
                    if best_found:
                        if path[1] >= best_dist:
                            continue
                        elif other_joint == end_joint:
                            best_path = path[0]
                            best_dist = path[1]
                            continue
                    elif other_joint == end_joint:
                        best_found = True
                        best_path = path[0]
                        best_dist = path[1]
                        continue
                    paths = [other_path for other_path in paths
                             if other_joint != other_path[0][-1]]
                    paths.append(path)
        paths = sorted(paths, key=lambda group: group[1] + group[2])
        if len(paths) == 0 and best_found == True:
            return best_path, best_dist
