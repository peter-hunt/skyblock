from ...constant.colors import *
from ...object.object import *

from ..object import *


END_NPCS = [
    Npc('pearl_dealer',
        init_dialog=[
            ('The End has endless End Stone and Obsidian.'
             ' You may find a special type of these'
             ' resources deep in the caves'),
            ('The items in my shop may be of help as you'
             ' descend into the depths of The End')],
        trades=[
            (10, {'name': 'end_stone'}),
            (50, {'name': 'obsidian'}),
            (2_500, {'name': 'holy_dragon_fragment'}),
            (2_500, {'name': 'old_dragon_fragment'}),
            (2_500, {'name': 'protector_dragon_fragment'}),
            (2_500, {'name': 'unstable_dragon_fragment'}),
            (2_500, {'name': 'young_dragon_fragment'}),
            (15_000, {'name': 'strong_dragon_fragment'}),
            (20_000, {'name': 'wise_dragon_fragment'}),
            (90_000, {'name': 'superior_dragon_fragment'}),
            (499_999, {'name': 'stonk'}),
            (499_999, {'name': 'aspect_of_the_dragons'}),
            (1_500_000, {'name': 'enchanted_book',
                         'enchantments': {'ender_slayer': 6}}),
        ]),
]
