from ...object.mob import get_mob
from ...object.resource import get_resource

from ..object import Npc, Zone, Island, add_dist


__all__ = ['DESERT']

DESERT_SETTLEMENT = Zone(
    'desert_settlement', 180, -380, portal='barn',
    resources=[get_resource('cactus'),
               get_resource('sand')],
    npcs=[
        Npc('beth',
            dialog=[
                'That Jake fellow is a bit suspicious.',
                ("He says he can't leave his house"
                 "but I've seen him walking around all the time..."),
            ]),
        Npc('friendly_hiker',
            dialog=[
                'My hiking buddy has been missing for a few couple days...',
                ('He said he was going to explore the gorge,'
                 ' but that was a while ago'),
                "I'm getting worried, could you go check on him?",
            ]),
        Npc('mason',
            dialog=[
                'I think the Treasure Hunter is a scammer.',
                ("He's always selling information about treasure locations"
                 " but I always hear that no one finds treasure"),
            ])],
)
GLOWING_MUSHROOM_CAVE = Zone(
    'glowing_mushroom_cave', 245, -500,
    resources=[get_resource('mushroom'),
               get_resource('sand')],
    mobs=[get_mob('mooshroom')],
)
JAKES_HOUSE = Zone('jakes_house', 255, -565)
MUSHROOM_GORGE = Zone(
    'mushroom_gorge', 205, -480,
    resources=[get_resource('mushroom'),
               get_resource('sand')],
    mobs=[get_mob('mooshroom')],
    npcs=[
        Npc('hungry_hiker',
            init_dialog=[
                'Hello there stranger!',
                ("I fell down into this ravine "
                 "a couple days ago and can't climb out"),
                ("My friend Jake said he would come get me "
                 "but he hasn't arrived yet"),
                'Could you bring me some food until he gets here?',
            ]),
    ],
)
OASIS = Zone(
    'oasis', 165, -410, fishable=True,
    resources=[get_resource('cocoa'),
               get_resource('sugar_cane')],
    mobs=[get_mob('rabbit'), get_mob('sheep')],
)
OVERGROWN_MUSHROOM_CAVE = Zone(
    'overgrown_mushroom_cave', 270, -365,
    resources=[get_resource('mushroom'),
               get_resource('sand')],
    mobs=[get_mob('mooshroom')],
)
SHEPHERDS_KEEP = Zone(
    'shepherds_keep', 360, -370,
    resources=[get_resource('cactus'),
               get_resource('sand')],
    mobs=[get_mob('sheep')],
    npcs=[
        Npc('shepherd',
            init_dialog=[
                'Hello traveller!',
                ('Welcome to my keep, my sheep are'
                 ' some of the best in the world.'),
                ('They have regenerative properties that allow for them '
                 'the regenerate their wool faster than normal!'),
                "I'm feeling tired today.",
                'Could you shear all my sheep at once?',
                'I will have a reward if you do so!',
            ]),
    ],
)
TRAPPERS_DEN = Zone('trappers_den', 285, -570)
TREASURE_HUNTER_CAMP = Zone(
    'treasure_hunter_camp', 200, -430,
    npcs=[
        Npc('treasure_hunter',
            dialog=[
                'Hello adventurer!',
                ("I'm the Treasure Hunter, "
                 "I've been searching for treasure all over this island."),
                ('Rumor has it that there are rare stones and other valuable'
                 ' bounty hidden in the ground all over the island.'),
                ("Tell you what, for a small price"
                 " I'll give you the info I know about."),
            ]),
    ],
)

DESERT_JOINTS = [
    DESERT_SETTLEMENT, GLOWING_MUSHROOM_CAVE, JAKES_HOUSE, MUSHROOM_GORGE,
    OASIS, OVERGROWN_MUSHROOM_CAVE, SHEPHERDS_KEEP, TRAPPERS_DEN,
    TREASURE_HUNTER_CAMP,
]
DESERT_CONNS = [
    (DESERT_SETTLEMENT, MUSHROOM_GORGE),
    (DESERT_SETTLEMENT, OASIS),
    (DESERT_SETTLEMENT, SHEPHERDS_KEEP),
    (DESERT_SETTLEMENT, TREASURE_HUNTER_CAMP),
    (GLOWING_MUSHROOM_CAVE, MUSHROOM_GORGE),
    (GLOWING_MUSHROOM_CAVE, OVERGROWN_MUSHROOM_CAVE),
    (JAKES_HOUSE, OASIS),
    (JAKES_HOUSE, TRAPPERS_DEN),
    (MUSHROOM_GORGE, JAKES_HOUSE),
    (MUSHROOM_GORGE, OASIS),
    (MUSHROOM_GORGE, OVERGROWN_MUSHROOM_CAVE),
    (MUSHROOM_GORGE, SHEPHERDS_KEEP),
    (MUSHROOM_GORGE, TRAPPERS_DEN),
    (MUSHROOM_GORGE, TREASURE_HUNTER_CAMP),
    (OASIS, TREASURE_HUNTER_CAMP),
    (SHEPHERDS_KEEP, TRAPPERS_DEN),
]

DESERT_DISTS = {}

for conn in DESERT_CONNS:
    add_dist(*conn, DESERT_DISTS)

DESERT = Island(
    'desert', 'desert_settlement', DESERT_JOINTS, DESERT_CONNS, DESERT_DISTS,
    skill_req=('farming', 5),
)
