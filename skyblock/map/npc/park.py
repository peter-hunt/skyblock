from ...object.item import get_item, get_scroll
from ...object.object import *

from ..object import *


PARK_NPCS = [
    Npc('master_tactician_funk',
        trades=[
            (35_000, get_item('tacticians_sword')),
        ]),
    Npc('melancholic_viking',
        init_dialog=[
            "For my wares, you'll have to pay the iron price!",
            'Seriously though, I accept Coins',
            'Talk to me again to open the Iron Forger Shop!',
        ],
        trades=[
            (130_000, get_item('raider_axe')),
            (70_000, get_scroll('jungle')),
            (400_000, EnchantedBook({'experience': 4})),
        ]),
    Npc('old_shaman_nyko',
        trades=[
            (900_000, EnchantedBook({'true_protection': 1})),
        ]),
]
