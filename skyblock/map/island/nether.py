from ...object.mob import get_mob
from ...object.resource import get_resource
from ..object import Island, Npc, Region, add_dist


__all__ = ['NETHER']

FORTRESS = Region(
    'fortress', -320, -400, portal='spider',
    npcs=[
        Npc('elle_of_the_nether',
            dialog=[
                'I have defeated the Magma Boss more times than I can count!',
                ('Many of the creatures on this island drop useful brewing'
                 ' ingredients. Use them in a Brewing Stand to brew strong'
                 ' potions that will aid to your journey.'),
                ("I don't know what would I do without my "
                 "Fire Resistance Potions. Probably burn."),
                'I told you not to come crying to me',
            ]),
    ],
    resources=[get_resource('nether_wart')],
    mobs=[get_mob('mini_blaze'),
          get_mob('blaze'),
          get_mob('wither_skeleton')],
)
MAGMA_FIELD = Region(
    'magma', -200, -650,
    resources=[get_resource('netherrack')],
    mobs=[get_mob('small_magma_cube'),
          get_mob('medium_magma_cube'),
          get_mob('large_magma_cube'),
          get_mob('ghast')],
)
NETHER_CAVES = Region(
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
