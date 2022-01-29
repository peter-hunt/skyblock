from ..object import *


DESERT_NPCS = [
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
    Npc('hungry_hiker',
        init_dialog=[
            'Hello there stranger!',
            ("I fell down into this ravine "
             "a couple days ago and can't climb out"),
            ("My friend Jake said he would come get me "
             "but he hasn't arrived yet"),
            'Could you bring me some food until he gets here?',
        ]),
    Npc('mason',
        dialog=[
            'I think the Treasure Hunter is a scammer.',
            ("He's always selling information about treasure locations"
             " but I always hear that no one finds treasure"),
        ]),
    Npc('shepherd',
        init_dialog=[
            'Hello traveller!',
            'Welcome to my keep, my sheep are some of the best in the world.',
            ('They have regenerative properties that allow for them '
             'the regenerate their wool faster than normal!'),
            "I'm feeling tired today.",
            'Could you shear all my sheep at once?',
            'I will have a reward if you do so!',
        ]),
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
]
