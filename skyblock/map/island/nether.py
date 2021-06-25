from ...constant.color import LIGHT_PURPLE, WHITE
from ...object.item import get_item
from ...object.mob import get_mob
from ...object.object import Item
from ...object.resource import get_resource
from ..object import Island, Npc, Region, add_dist

__all__ = ['NETHER']


FORTRESS = Region(
    'fortress', -320, -400,
    npcs=[
        Npc('pearl_dealer',
            init_dialog=[
                (f"Ender Pearls attract the attention of Endermen,"
                 f" but {LIGHT_PURPLE}Silent Pearls{WHITE} don't!"
                 f" You can get them in my shop."),
                ('The End has endless End Stone and Obsidian.'
                 ' You may find a special type of these'
                 ' resources deep in the caves'),
                ('The items in my shop may be of help as you'
                 ' descend into the depths of The End'),
            ],
            trades=[
                (10, Item('end_stone')),
                (50, Item('obsidian')),
                (499_999, get_item('stonk')),
            ]),
    ],
    resources=[get_resource('nether_wart')],
    mobs=[get_mob('mini_blaze'),
          get_mob('blaze'),
          get_mob('wither_skeleton')],
    portal='spider',
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
