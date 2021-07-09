from ...object.mob import get_mob
from ...object.resource import get_resource

from ..npc import get_npc
from ..object import *


__all__ = ['MINES']

DWARVEN_ENTRENCE = Zone(
    'dwarven_entrence', -60, -120, portal='deep',
    npcs=[get_npc('life_operator')],
)
DWARVEN_VILLAGE = Zone(
    'dwarven_village', 20, -140,
    resources=[get_resource('stone')],
    npcs=[get_npc('bubu'),
          get_npc('gimley'),
          get_npc('hornum'),
          get_npc('sargwyn'),
          get_npc('tarwen')],
)
FAR = Zone(
    'far', -120, 70,
    resources=[get_resource('stone'), get_resource('gray_mithril'),
               get_resource('dark_mithril'), get_resource('light_mithril')],
)
FORGE = Zone(
    'forge', 0, -70,
    npcs=[get_npc('jotraeline_greatforge'), ],
)
GOBLINS = Zone(
    'goblins', -110, 110,
    resources=[get_resource('stone')],
    mobs=[get_mob('goblin')],
)
ICE_WALLS = Zone(
    'ice_walls', 0, 100,
    resources=[get_resource('stone'), get_resource('gray_mithril'),
               get_resource('dark_mithril'), get_resource('light_mithril'),
               get_resource('gold_block')],
    mobs=[get_mob('ice_walker')],
)
MIST = Zone(
    'mist', 0, 40,
    mobs=[get_mob('ghost')],
)
PALACE = Zone(
    'palace', 120, 120,
    npcs=[get_npc('brammor'), get_npc('emkam'), get_npc('emmor'),
          get_npc('erren'), get_npc('grandan'), get_npc('redos'),
          get_npc('thormyr')],
)
RAMPARTS = Zone(
    'ramparts', -25, -50,
    resources=[get_resource('stone'), get_resource('gray_mithril'),
               get_resource('dark_mithril'), get_resource('light_mithril')],
)
ROYAL = Zone(
    'royal', 140, 35,
    resources=[get_resource('stone'), get_resource('gray_mithril'),
               get_resource('dark_mithril'), get_resource('light_mithril'),
               get_resource('gold_block')],
)
SPRINGS = Zone(
    'springs', 60, -70,
    resources=[get_resource('stone'), get_resource('gray_mithril'),
               get_resource('dark_mithril'), get_resource('light_mithril')],
)
VEINS = Zone(
    'veins', 20, 0,
    resources=[get_resource('stone'), get_resource('gray_mithril'),
               get_resource('dark_mithril'), get_resource('light_mithril')],
)
UPPER = Zone(
    'upper', -125, -50, fishable=True,
    resources=[get_resource('stone'), get_resource('gray_mithril'),
               get_resource('dark_mithril'), get_resource('light_mithril')],
)

MINES_JOINTS = [
    DWARVEN_ENTRENCE, DWARVEN_VILLAGE, FAR, FORGE, GOBLINS, ICE_WALLS, MIST,
    PALACE, RAMPARTS, ROYAL, SPRINGS, VEINS, UPPER,
]
MINES_CONNS = [
    (DWARVEN_ENTRENCE, DWARVEN_VILLAGE),
    (DWARVEN_VILLAGE, RAMPARTS),
    (DWARVEN_VILLAGE, ROYAL),
    (DWARVEN_VILLAGE, SPRINGS),
    (FAR, GOBLINS),
    (FAR, RAMPARTS),
    (FAR, UPPER),
    (FORGE, VEINS),
    (GOBLINS, ICE_WALLS),
    (ICE_WALLS, MIST),
    (MIST, VEINS),
    (PALACE, ROYAL),
    (RAMPARTS, UPPER),
    (RAMPARTS, VEINS),
    (ROYAL, SPRINGS),
    (SPRINGS, VEINS),
]

MINES_DISTS = {}

for conn in MINES_CONNS:
    add_dist(*conn, MINES_DISTS)

MINES = Island(
    'mines', 'dwarven_entrence', MINES_JOINTS, MINES_CONNS, MINES_DISTS,
    skill_req=('mining', 12),
)
