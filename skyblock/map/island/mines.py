from ...constant.color import GOLD, GREEN, WHITE
from ...object.item import get_item
from ...object.object import Item
from ...object.mob import get_mob
from ...object.resource import get_resource

from ..object import Npc, Region, Island, add_dist

__all__ = ['MINES']

DWARVEN_ENTRENCE = Region(
    'dwarven_entrence', -60, -120,
    npcs=[
        Npc('life_operator',
            dialog=[
                'Hey Feller!',
                'I control this lift here behind me.',
                ("Once you've explored an area"
                 " I can give you a safe ride back there."),
                ("Be careful not to fall down the shaft though,"
                 " it's a long fall!"),
                'Good luck on your adventures.',
            ])
    ],
    portal='deep',
)
DWARVEN_VILLAGE = Region(
    'dwarven_village', 20, -140,
    resources=[get_resource('stone')],
    npcs=[
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
        Npc('gimley',
            dialog=[(
                'Burp',
                'Buurp',
                'Buuuuurp',
                'Buuuuuuuuuuuuuurp',
                'BURP',
                'BURP',
                'BUURRPPP',
                '‎*Inception BRRRAAWWWWWBRBRBB noises*',
            )]),
        Npc('hornum',
            dialog=[(
                'Burp',
                'Buurp',
                'Buuuuurp',
                'Buuuuuuuuuuuuuurp',
                'BURP',
                'BURP',
                'BUURRPPP',
                '‎*Inception BRRRAAWWWWWBRBRBB noises*',
            )]),
        Npc('sargwyn',
            dialog=[(
                'Burp',
                'Buurp',
                'Buuuuurp',
                'Buuuuuuuuuuuuuurp',
                'BURP',
                'BURP',
                'BUURRPPP',
                '‎*Inception BRRRAAWWWWWBRBRBB noises*',
            )]),
        Npc('tarwen',
            dialog=[(
                'Burp',
                'Buurp',
                'Buuuuurp',
                'Buuuuuuuuuuuuuurp',
                'BURP',
                'BURP',
                'BUURRPPP',
                '‎*Inception BRRRAAWWWWWBRBRBB noises*',
            )]),
    ],
)
FAR = Region(
    'far', -120, 70,
    resources=[get_resource('stone'), get_resource('gray_mithril'),
               get_resource('dark_mithril'), get_resource('light_mithril')],
)
FORGE = Region(
    'forge', 0, -70,
    npcs=[
        Npc('jotraeline_greatforge',
            dialog=[
                (f"Drills are sweet! Too bad you don't have one."
                 f" I hear you can create them in the {GOLD}Forge{WHITE}!"),
                (f'Come back to me when you have '
                 f'a {GREEN}Drill{WHITE} in your inventory!'),
                (f'What are you doing talking to me without '
                 f'a {GREEN}Drill{WHITE}? Come back when you have one!'),
            ]),
    ],
)
GOBLINS = Region(
    'goblins', -110, 110,
    mobs=[get_mob('goblin')],
)
ICE_WALLS = Region(
    'ice_walls', 0, 100,
    mobs=[get_mob('ice_walker')],
)
MIST = Region(
    'mist', 0, 40,
)
PALACE = Region(
    'palace', 120, 120,
    npcs=[
        Npc('brammor'),
        Npc('emkam'),
        Npc('emmor'),
        Npc('erren'),
        Npc('grandan'),
        Npc('redos'),
        Npc('thormyr'),
    ],
)
RAMPARTS = Region(
    'ramparts', -25, -50,
    resources=[get_resource('stone'), get_resource('gray_mithril'),
               get_resource('dark_mithril'), get_resource('light_mithril')],
)
ROYAL = Region(
    'royal', 140, 35,
    resources=[get_resource('stone'), get_resource('gray_mithril'),
               get_resource('dark_mithril'), get_resource('light_mithril'),
               get_resource('gold_block')],
)
SPRINGS = Region(
    'springs', 60, -70,
    resources=[get_resource('stone'), get_resource('gray_mithril'),
               get_resource('dark_mithril'), get_resource('light_mithril')],
)
VEINS = Region(
    'veins', 20, 0,
    resources=[get_resource('stone'), get_resource('gray_mithril'),
               get_resource('dark_mithril'), get_resource('light_mithril')],
)
UPPER = Region(
    'upper', -125, -50,
    resources=[get_resource('stone'), get_resource('gray_mithril'),
               get_resource('dark_mithril'), get_resource('light_mithril')],
)

MINES_JOINTS = [
    DWARVEN_ENTRENCE, DWARVEN_VILLAGE, FAR, FORGE, GOBLINS, ICE_WALLS, MIST,
    PALACE, RAMPARTS, ROYAL, SPRINGS, VEINS, UPPER,
]
MINES_CONNS = [
    (DWARVEN_ENTRENCE, DWARVEN_VILLAGE),
    (DWARVEN_VILLAGE, RAMPARTS),
    (DWARVEN_VILLAGE, ROYAL),
    (DWARVEN_VILLAGE, SPRINGS),
    (FAR, GOBLINS),
    (FAR, RAMPARTS),
    (FAR, UPPER),
    (FORGE, VEINS),
    (GOBLINS, ICE_WALLS),
    (ICE_WALLS, MIST),
    (MIST, VEINS),
    (PALACE, ROYAL),
    (RAMPARTS, UPPER),
    (RAMPARTS, VEINS),
    (ROYAL, SPRINGS),
    (SPRINGS, VEINS),
]

MINES_DISTS = {}

for conn in MINES_CONNS:
    add_dist(*conn, MINES_DISTS)

MINES = Island(
    'mines', 'dwarven_entrence', MINES_JOINTS, MINES_CONNS, MINES_DISTS,
    skill_req=('mining', 12),
)
