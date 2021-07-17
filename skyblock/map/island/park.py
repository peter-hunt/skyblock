from ...object.mob import get_mob
from ...object.resource import get_resource

from ..npc import get_npc
from ..object import *


__all__ = ['PARK']

BIRCH_PARK = Zone(
    'birch', -300, -20, portal='hub', fishable=True,
    resources=[get_resource('birch_wood')],
)
HOWLING_CAVE = Zone(
    'howl', -330, -55, fishable=True,
    mobs=[get_mob('pack_spirit'), get_mob('howling_spirit'),
          get_mob('soul_of_the_alpha')],
    npcs=[get_npc('old_shaman_nyko')],
)
SPRUCE_WOOD = Zone(
    'spruce', -325, 0,
    resources=[get_resource('spruce_wood'), get_resource('ice')],
    npcs=[get_npc('melancholic_viking')],
    skill_req=('foraging', 2),
)
DARK_THICKET = Zone(
    'dark', -330, -45,
    resources=[get_resource('dark_oak_wood')],
    skill_req=('foraging', 3),
)
SAVANNA_WOODLAND = Zone(
    'savanna', -350, -15,
    resources=[get_resource('acacia_wood')],
    npcs=[get_npc('master_tactician_funk')],
    skill_req=('foraging', 4),
)
JUNGLE_ISLAND = Zone(
    'jungle', -55, -60,
    resources=[get_resource('jungle_wood')],
    skill_req=('foraging', 5),
)

PARK_JOINTS = [
    BIRCH_PARK, HOWLING_CAVE, SPRUCE_WOOD,
    DARK_THICKET, SAVANNA_WOODLAND, JUNGLE_ISLAND,
]
PARK_CONNS = [
    (BIRCH_PARK, HOWLING_CAVE),
    (BIRCH_PARK, SPRUCE_WOOD),
    (DARK_THICKET, SAVANNA_WOODLAND),
    (DARK_THICKET, SPRUCE_WOOD),
    (JUNGLE_ISLAND, SAVANNA_WOODLAND),
]

PARK_DISTS = {}

for conn in PARK_CONNS:
    add_dist(*conn, PARK_DISTS)

PARK = Island(
    'park', 'birch', PARK_JOINTS, PARK_CONNS, PARK_DISTS,
    skill_req=('foraging', 1),
)
