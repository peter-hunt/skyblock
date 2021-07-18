from ...constant.colors import *
from ...object.object import *

from ..object import *


END_NPCS = [
    Npc('pearl_dealer',
        init_dialog=[
            (f"Ender Pearls attract the attention of Endermen,"
             f" but {LIGHT_PURPLE}Silent Pearls{WHITE} don't!"
             f" You can get them in my shop."),
            ('The End has endless End Stone and Obsidian.'
             ' You may find a special type of these'
             ' resources deep in the caves'),
            ('The items in my shop may be of help as you'
             ' descend into the depths of The End')],
        trades=[
            (10, {'name': 'end_stone'}),
            (50, {'name': 'obsidian'}),
            (499_999, {'name': 'stonk'}),
            (1_500_000, {'name': 'enchanted_book',
                         'enchantments': {'ender_slayer': 4}}),
        ]),
]
