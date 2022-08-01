from ...object.mobs import get_mob
from ...object.resources import get_resource

from ..npc import get_npc
from ..object import *


__all__ = ['CRIMSON']

ASHFANG = Zone('ashfang', -500, -1400)
BARBARIAN_OUTPOST = Zone(
    'barbarian_outpost', -650, -1200,
)
BURNING_DESERT = Zone(
    'burning', -550, -1000,
)
DRAGONTAIL = Zone('dragontail', -800, -1000)
FIELDS = Zone(
    'fields', -400, -620,
    resources=[get_resource('netherrack')],
)
GATE = Zone('gate', -300, -400, portal='spider')
MAGE_OUTPOST = Zone(
    'mage_outpost', -150, -1200,
)
MAGMA = Zone('magma', -370, -1000)
MYSTIC_MARSH = Zone(
    'mystic', -250, -1000,
)
ODGERS_HUT = Zone('odgers_hut', -400, -950)
SCARLETON = Zone('scarleton', 0, -1000)
SKULL = Zone('skull', -400, -1450)
SMOLDERING = Zone('smoldering', -300, -1400)
STRONGHOLD = Zone(
    'stronghold', -400, -500,
    npcs=[get_npc('elle_of_the_nether')],
    resources=[get_resource('netherrack'),
               get_resource('nether_wart')],
)
WASTELAND = Zone(
    'wasteland', -400, -1250,
    resources=[get_resource('netherrack')],
)
VOLCANO = Zone('volcano', -400, -1000)

CRIMSON_JOINTS = [
    ASHFANG, BARBARIAN_OUTPOST, BURNING_DESERT, DRAGONTAIL, FIELDS, GATE, MAGE_OUTPOST,
    MAGMA, MYSTIC_MARSH, ODGERS_HUT, SCARLETON, SKULL, SMOLDERING, STRONGHOLD, WASTELAND, VOLCANO,
]
CRIMSON_CONNS = [
    (ASHFANG, DRAGONTAIL),
    (ASHFANG, SKULL),
    (ASHFANG, WASTELAND),
    (BARBARIAN_OUTPOST, BURNING_DESERT),
    (BARBARIAN_OUTPOST, DRAGONTAIL),
    (BARBARIAN_OUTPOST, WASTELAND),
    (BURNING_DESERT, DRAGONTAIL),
    (BURNING_DESERT, FIELDS),
    (BURNING_DESERT, WASTELAND),
    (BURNING_DESERT, VOLCANO),
    (FIELDS, STRONGHOLD),
    (FIELDS, MYSTIC_MARSH),
    (FIELDS, VOLCANO),
    (GATE, STRONGHOLD),
    (MAGE_OUTPOST, MYSTIC_MARSH),
    (MAGE_OUTPOST, SCARLETON),
    (MAGE_OUTPOST, WASTELAND),
    (MAGMA, VOLCANO),
    (MYSTIC_MARSH, SCARLETON),
    (MYSTIC_MARSH, WASTELAND),
    (MYSTIC_MARSH, VOLCANO),
    (ODGERS_HUT, VOLCANO),
    (SCARLETON, SMOLDERING),
    (SKULL, SMOLDERING),
    (SKULL, WASTELAND),
    (SMOLDERING, WASTELAND),
    (WASTELAND, VOLCANO),
]

CRIMSON_DISTS = {}

for conn in CRIMSON_CONNS:
    add_dist(*conn, CRIMSON_DISTS)

CRIMSON = Island(
    'crimson', 'gate', CRIMSON_JOINTS, CRIMSON_CONNS, CRIMSON_DISTS,
    skill_req=('combat', 24),
)
