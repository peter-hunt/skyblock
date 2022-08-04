from ...object.mobs import get_mob
from ...object.resources import get_resource

from ..npc import get_npc
from ..object import *


__all__ = ['CRIMSON']

ASHFANG = Zone(
    'ashfang_ruins', -500, -1400,
    resources=[get_resource('netherrack')],
    mobs=[get_mob('ashfang')],
)
BARBARIAN_OUTPOST = Zone(
    'barbarian_output', -700, -300,
    resources=[get_resource('netherrack'),
               get_resource('red_sand')],
    mobs=[get_mob('barbarian'),
          get_mob('goliath_barbarian')],
)
BURNING_DESERT = Zone(
    'burning', -550, -1000,  # -500, -750
    resources=[get_resource('netherrack'),
               get_resource('red_sand')],
    mobs=[get_mob('flaming_spider'),
          get_mob('magma_cube_rider')],
)
COURTYARD = Zone(
    'courtyard', -150, -1200,
    resources=[get_resource('mycelium'),
               get_resource('netherrack')],
    mobs=[get_mob('mage_outlaw')],
)
DRAGONTAIL = Zone(
    'dragontail', -800, -1000,  # -600, -800
    resources=[get_resource('netherrack'),
               get_resource('red_sand')],
)
DUKEDOM = Zone(
    'dukedom', -650, -1200,  # -550, -900
    resources=[get_resource('netherrack'),
               get_resource('red_sand')],
    mobs=[get_mob('barbarian_duke_x')],
)
FIELDS = Zone(
    'fields', -400, -600,  # -350, -650
    resources=[get_resource('netherrack')],
    mobs=[get_mob('magma_cube')],
)
GATE = Zone('gate', -300, -400, portal='spider')
MAGE_OUTPOST = Zone(
    'mage_outpost', -100, -300,
    resources=[get_resource('mycelium'),
               get_resource('netherrack')],
    mobs=[get_mob('fire_mage'),
          get_mob('krondor_necromancer')],
)
MAGMA = Zone(
    'magma', -370, -1000,  # -350, -800
    resources=[get_resource('glowstone'),
               get_resource('quartz_ore'),
               get_resource('netherrack')],
    mobs=[get_mob('magma_cube_boss')],
)
MYSTIC_MARSH = Zone(
    'mystic', -250, -1000,
    resources=[get_resource('mycelium'),
               get_resource('netherrack')],
    mobs=[get_mob('mushroom_bull')],
)
ODGERS_HUT = Zone('odgers_hut', -400, -950)
SCARLETON = Zone(
    'scarleton', 0, -1000,
    resources=[get_resource('mycelium'),
               get_resource('netherrack')],
)
SKULL = Zone('skull', -400, -1450)
SMOLDERING = Zone(
    'smoldering', -300, -1400,
    resources=[get_resource('netherrack')],
    mobs=[get_mob('millenia_aged_blaze'),
          get_mob('smoldering_blaze')],
)
STRONGHOLD = Zone(
    'stronghold', -400, -500,  # -350, -500
    npcs=[get_npc('elle_of_the_nether')],
    resources=[get_resource('netherrack'),
               get_resource('nether_wart')],
    mobs=[get_mob('bezal'),
          get_mob('bladesoul'),
          get_mob('blaze'),
          get_mob('mutated_blaze'),
          get_mob('wither_skeleton'),
          get_mob('wither_spectre')],
)
WASTELAND = Zone(
    'wasteland', -400, -1250,
    resources=[get_resource('netherrack')],
    mobs=[get_mob('dive_ghast'),
          get_mob('ghast')],
)
VOLCANO = Zone(
    'volcano', -400, -1000,
    resources=[get_resource('glowstone'),
               get_resource('quartz_ore'),
               get_resource('netherrack')],
    mobs=[get_mob('flare'),
          get_mob('kada_knight')],
)

CRIMSON_JOINTS = [
    ASHFANG, BARBARIAN_OUTPOST, BURNING_DESERT, COURTYARD, DRAGONTAIL,
    DUKEDOM, FIELDS, GATE, MAGE_OUTPOST, MAGMA, MYSTIC_MARSH, ODGERS_HUT,
    SCARLETON, SKULL, SMOLDERING, STRONGHOLD, WASTELAND, VOLCANO,
]
CRIMSON_CONNS = [
    (ASHFANG, DRAGONTAIL),
    (ASHFANG, SKULL),
    (ASHFANG, WASTELAND),
    (BARBARIAN_OUTPOST, DRAGONTAIL),
    (BARBARIAN_OUTPOST, FIELDS),
    (BARBARIAN_OUTPOST, VOLCANO),
    (BURNING_DESERT, DRAGONTAIL),
    (BURNING_DESERT, DUKEDOM),
    (BURNING_DESERT, FIELDS),
    (BURNING_DESERT, WASTELAND),
    (BURNING_DESERT, VOLCANO),
    (COURTYARD, MYSTIC_MARSH),
    (COURTYARD, SCARLETON),
    (COURTYARD, WASTELAND),
    (DRAGONTAIL, DUKEDOM),
    (DUKEDOM, WASTELAND),
    (FIELDS, STRONGHOLD),
    (FIELDS, MAGE_OUTPOST),
    (FIELDS, MYSTIC_MARSH),
    (FIELDS, VOLCANO),
    (GATE, STRONGHOLD),
    (MAGMA, VOLCANO),
    (MAGE_OUTPOST, MYSTIC_MARSH),
    (MAGE_OUTPOST, VOLCANO),
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
