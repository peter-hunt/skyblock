from ...object.mob import get_mob
from ...object.resource import get_resource

from ..npc import get_npc
from ..object import *


__all__ = ['NETHER']

FORTRESS = Zone(
    'fortress', -320, -400, portal='spider',
    npcs=[get_npc('elle_of_the_nether')],
    resources=[get_resource('nether_wart')],
    mobs=[get_mob('mini_blaze'),
          get_mob('blaze'),
          get_mob('wither_skeleton')],
)
MAGMA_FIELD = Zone(
    'magma', -200, -650,
    resources=[get_resource('netherrack')],
    mobs=[get_mob('small_magma_cube'),
          get_mob('medium_magma_cube'),
          get_mob('large_magma_cube'),
          get_mob('ghast')],
)
NETHER_CAVES = Zone(
    'nether_caves', -400, -500,
    resources=[get_resource('glowstone'),
               get_resource('netherrack'),
               get_resource('quartz_ore')],
    mobs=[get_mob('zombie_pigman')],
)

NETHER_JOINTS = [FORTRESS, MAGMA_FIELD, NETHER_CAVES]
NETHER_CONNS = [
    (FORTRESS, MAGMA_FIELD),
    (FORTRESS, NETHER_CAVES),
    (MAGMA_FIELD, NETHER_CAVES),
]

NETHER_DISTS = {}

for conn in NETHER_CONNS:
    add_dist(*conn, NETHER_DISTS)

NETHER = Island(
    'nether', 'fortress', NETHER_JOINTS, NETHER_CONNS, NETHER_DISTS,
    skill_req=('combat', 5),
)
