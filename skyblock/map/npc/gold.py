from ...object.object import *

from ..object import *


GOLD_NPCS = [
    Npc('gold_forger',
        init_dialog=[
            'I love goooold!',
            'Talk to me again to open the Gold Forger Shop!',
        ],
        trades=[
            (5.5, {'name': 'gold'}),
            (10, {'name': 'golden_helmet'}),
            (16, {'name': 'golden_chestplate'}),
            (14, {'name': 'golden_leggings'}),
            (9, {'name': 'golden_boots'}),
            (80, {'name': 'fancy_sword'}),
        ]),
    Npc('iron_forger',
        init_dialog=[
            "For my wares, you'll have to pay the iron price!",
            'Seriously though, I accept Coins',
            'Talk to me again to open the Iron Forger Shop!',
        ],
        trades=[
            (60, {'name': 'iron_pickaxe'}),
            (5, {'name': 'iron'}),
            (50, {'name': 'chainmail_helmet'}),
            (100, {'name': 'chainmail_chestplate'}),
            (75, {'name': 'chainmail_leggings'}),
            (100, {'name': 'chainmail_boots'}),
        ]),
]
