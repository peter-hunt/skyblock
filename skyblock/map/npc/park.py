from ...object.object import *

from ..object import *


PARK_NPCS = [
    Npc('master_tactician_funk',
        trades=[
            (35_000, {'name': 'tacticians_sword'}),
        ]),
    Npc('melancholic_viking',
        trades=[
            (130_000, {'name': 'raider_axe'}),
            (70_000, {'name': 'travel_scroll_to_jungle'}),
            (400_000, {'name': 'enchanted_book',
                       'enchantments': {'experience': 4}}),
        ]),
    Npc('old_shaman_nyko',
        trades=[
            (900_000, {'name': 'enchanted_book',
                       'enchantments': {'true_protection': 1}}),
        ]),
]
