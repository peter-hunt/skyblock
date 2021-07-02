from ...object.mob import get_mob
from ...object.resource import get_resource

from ..npc import get_npc
from ..object import Zone, Island, add_dist


__all__ = ['DESERT']

DESERT_SETTLEMENT = Zone(
    'desert_settlement', 180, -380, portal='barn',
    resources=[get_resource('cactus'), get_resource('sand')],
    npcs=[get_npc('beth'), get_npc('friendly_hiker'), get_npc('mason')],
)
GLOWING_MUSHROOM_CAVE = Zone(
    'glowing_mushroom_cave', 245, -500,
    resources=[get_resource('mushroom'), get_resource('sand')],
    mobs=[get_mob('mooshroom')],
)
JAKES_HOUSE = Zone('jakes_house', 255, -565)
MUSHROOM_GORGE = Zone(
    'mushroom_gorge', 205, -480,
    resources=[get_resource('mushroom'), get_resource('sand')],
    mobs=[get_mob('mooshroom')],
    npcs=[get_npc('hungry_hiker')],
)
OASIS = Zone(
    'oasis', 165, -410, fishable=True,
    resources=[get_resource('cocoa'), get_resource('sugar_cane')],
    mobs=[get_mob('rabbit'), get_mob('sheep')],
)
OVERGROWN_MUSHROOM_CAVE = Zone(
    'overgrown_mushroom_cave', 270, -365,
    resources=[get_resource('mushroom'), get_resource('sand')],
    mobs=[get_mob('mooshroom')],
)
SHEPHERDS_KEEP = Zone(
    'shepherds_keep', 360, -370,
    resources=[get_resource('cactus'), get_resource('sand')],
    mobs=[get_mob('sheep')],
    npcs=[get_npc('shepherd')],
)
TRAPPERS_DEN = Zone('trappers_den', 285, -570)
TREASURE_HUNTER_CAMP = Zone(
    'treasure_hunter_camp', 200, -430,
    npcs=[get_npc('treasure_hunter')],
)

DESERT_JOINTS = [
    DESERT_SETTLEMENT, GLOWING_MUSHROOM_CAVE, JAKES_HOUSE, MUSHROOM_GORGE,
    OASIS, OVERGROWN_MUSHROOM_CAVE, SHEPHERDS_KEEP, TRAPPERS_DEN,
    TREASURE_HUNTER_CAMP,
]
DESERT_CONNS = [
    (DESERT_SETTLEMENT, MUSHROOM_GORGE),
    (DESERT_SETTLEMENT, OASIS),
    (DESERT_SETTLEMENT, SHEPHERDS_KEEP),
    (DESERT_SETTLEMENT, TREASURE_HUNTER_CAMP),
    (GLOWING_MUSHROOM_CAVE, MUSHROOM_GORGE),
    (GLOWING_MUSHROOM_CAVE, OVERGROWN_MUSHROOM_CAVE),
    (JAKES_HOUSE, OASIS),
    (JAKES_HOUSE, TRAPPERS_DEN),
    (MUSHROOM_GORGE, JAKES_HOUSE),
    (MUSHROOM_GORGE, OASIS),
    (MUSHROOM_GORGE, OVERGROWN_MUSHROOM_CAVE),
    (MUSHROOM_GORGE, SHEPHERDS_KEEP),
    (MUSHROOM_GORGE, TRAPPERS_DEN),
    (MUSHROOM_GORGE, TREASURE_HUNTER_CAMP),
    (OASIS, TREASURE_HUNTER_CAMP),
    (SHEPHERDS_KEEP, TRAPPERS_DEN),
]

DESERT_DISTS = {}

for conn in DESERT_CONNS:
    add_dist(*conn, DESERT_DISTS)

DESERT = Island(
    'desert', 'desert_settlement', DESERT_JOINTS, DESERT_CONNS, DESERT_DISTS,
    skill_req=('farming', 5),
)
