from ...constant.color import LIGHT_PURPLE, WHITE
from ...object.item import get_item
from ...object.mob import get_mob
from ...object.object import Item
from ...object.resource import get_resource
from ..object import Island, Npc, Region, add_dist

__all__ = ['END']


END_ENTRENCE = Region(
    'end_entrence', -540, -300,
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
    resources=[get_resource('end_stone'),
               get_resource('obsidian')],
    mobs=[get_mob('enderman', level=42)],
    portal='spider',
)
END_TUNNEL = Region(
    'end_tunnel', -560, -300,
    resources=[get_resource('end_stone'),
               get_resource('obsidian')],
    mobs=[get_mob('enderman', level=45)],
)
END_CAVES = Region(
    'end_caves', -580, -290,
    resources=[get_resource('end_stone'),
               get_resource('obsidian')],
    mobs=[get_mob('enderman', level=50)],
)
DRAGONS_NEST = Region(
    'dragons_nest', -600, -280,
    resources=[get_resource('end_stone')],
    mobs=[get_mob('watcher'),
          get_mob('obsidian_defender'),
          get_mob('zealot')],
)

END_JOINTS = [END_ENTRENCE, END_TUNNEL, END_CAVES, DRAGONS_NEST]
END_CONNS = [
    (DRAGONS_NEST, END_CAVES),
    (END_ENTRENCE, END_TUNNEL),
    (END_CAVES, END_TUNNEL),
]

END_DISTS = {}

for conn in END_CONNS:
    add_dist(*conn, END_DISTS)

END = Island(
    'end', 'end_entrence', END_JOINTS, END_CONNS, END_DISTS,
    skill_req=('combat', 12),
)
