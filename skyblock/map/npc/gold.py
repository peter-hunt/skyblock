from ...object.item import get_item
from ...object.object import Item

from ..object import Npc


GOLD_NPCS = [
    Npc('gold_forger',
        init_dialog=[
            'I love goooold!',
            'Talk to me again to open the Gold Forger Shop!',
        ],
        trades=[
            (5.5, Item('gold')),
            (10, get_item('golden_helmet')),
            (16, get_item('golden_chestplate')),
            (14, get_item('golden_leggings')),
            (9, get_item('golden_boots')),
            (80, get_item('fancy_sword')),
        ]),
    Npc('iron_forger',
        init_dialog=[
            "For my wares, you'll have to pay the iron price!",
            'Seriously though, I accept Coins',
            'Talk to me again to open the Iron Forger Shop!',
        ],
        trades=[
            (60, get_item('iron_pickaxe')),
            (5, Item('iron')),
            (50, get_item('chainmail_helmet')),
            (100, get_item('chainmail_chestplate')),
            (75, get_item('chainmail_leggings')),
            (100, get_item('chainmail_boots')),
        ]),
]
