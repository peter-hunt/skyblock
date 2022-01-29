from ...constant.colors import *
from ...object.object import *

from ..object import *


MINES_NPCS = [
    Npc('brammor'),
    Npc('bubu',
        trades=[
            (10_000,
             {'name': 'fractured_mithril_pickaxe'}),
            ((100_000,
              {'name': 'mithril', 'count': 200}),
             {'name': 'bandaged_mithril_pickaxe'}),
            ((1_000_000,
              {'name': 'titanium', 'count': 100},
              {'name': 'bejeweled_handle'}),
             {'name': 'titanium_pickaxe'}),
            (({'name': 'titanium_pickaxe'},
              {'name': 'refined_titanium', 'count': 3}),
             {'name': 'refined_titanium_pickaxe'}),
        ]),
    Npc('emkam'),
    Npc('emmor'),
    Npc('erren'),
    Npc('gimley',
        dialog=[(
            'Burp', 'Buurp', 'Buuuuurp', 'Buuuuuuuuuuuuuurp',
            'BURP', 'BUURRPPP', '*Inception BRRRAAWWWWWBRBRBB noises*',
        )]),
    Npc('grandan'),
    Npc('hornum',
        dialog=[(
            'Burp', 'Buurp', 'Buuuuurp', 'Buuuuuuuuuuuuuurp',
            'BURP', 'BUURRPPP', '*Inception BRRRAAWWWWWBRBRBB noises*',
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
            'BURP', 'BUURRPPP', '*Inception BRRRAAWWWWWBRBRBB noises*',
        )]),
    Npc('tarwen',
        dialog=[(
            'Burp', 'Buurp', 'Buuuuurp', 'Buuuuuuuuuuuuuurp',
            'BURP', 'BUURRPPP', '*Inception BRRRAAWWWWWBRBRBB noises*',
        )]),
    Npc('thormyr'),
]
