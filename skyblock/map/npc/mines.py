from ...constant.color import *
from ...object.item import get_item
from ...object.object import *

from ..object import *


MINES_NPCS = [
    Npc('brammor'),
    Npc('bubu',
        trades=[
            (10_000,
             get_item('fractured_mithril_pickaxe')),
            ((100_000,
              (Item('mithril'), 200)),
             get_item('bandaged_mithril_pickaxe')),
            ((1_000_000,
              (Item('titanium'), 100),
              (Item('bejeweled_handle'), 1)),
             get_item('titanium_pickaxe')),
            (((Item('titanium_pickaxe'), 1),
              (Item('refined_titanium'), 3)),
             get_item('refined_titanium_pickaxe')),
        ]),
    Npc('emkam'),
    Npc('emmor'),
    Npc('erren'),
    Npc('gimley',
        dialog=[(
            'Burp', 'Buurp', 'Buuuuurp', 'Buuuuuuuuuuuuuurp',
            'BURP', 'BUURRPPP', '‎*Inception BRRRAAWWWWWBRBRBB noises*',
        )]),
    Npc('grandan'),
    Npc('hornum',
        dialog=[(
            'Burp', 'Buurp', 'Buuuuurp', 'Buuuuuuuuuuuuuurp',
            'BURP', 'BUURRPPP', '‎*Inception BRRRAAWWWWWBRBRBB noises*',
        )]),
    Npc('jotraeline_greatforge',
        dialog=[
            (f"Drills are sweet! Too bad you don't have one."
             f" I hear you can create them in the {GOLD}Forge{WHITE}!"),
            (f'Come back to me when you have '
             f'a {GREEN}Drill{WHITE} in your inventory!'),
            (f'What are you doing talking to me without '
             f'a {GREEN}Drill{WHITE}? Come back when you have one!'),
        ]),
    Npc('life_operator',
        dialog=[
            'Hey Feller!',
            'I control this lift here behind me.',
            ("Once you've explored an area"
             " I can give you a safe ride back there."),
            ("Be careful not to fall down the shaft though,"
             " it's a long fall!"),
            'Good luck on your adventures.',
        ]),
    Npc('redos'),
    Npc('sargwyn',
        dialog=[(
            'Burp', 'Buurp', 'Buuuuurp', 'Buuuuuuuuuuuuuurp',
            'BURP', 'BUURRPPP', '‎*Inception BRRRAAWWWWWBRBRBB noises*',
        )]),
    Npc('tarwen',
        dialog=[(
            'Burp', 'Buurp', 'Buuuuurp', 'Buuuuuuuuuuuuuurp',
            'BURP', 'BUURRPPP', '‎*Inception BRRRAAWWWWWBRBRBB noises*',
        )]),
    Npc('thormyr'),
]
