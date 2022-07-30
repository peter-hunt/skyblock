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
    Npc('tony',
        trades=[
            (({'name': 'cocoa_minion', 'tier': 11},
              {'name': 'enchanted_cookie', 'count': 16}),
             {'name': 'cocoa_minion', 'tier': 12}),
            (({'name': 'pumpkin_minion', 'tier': 11},
              {'name': 'enchanted_pumpkin', 'count': 1_024}),
             {'name': 'pumpkin_minion', 'tier': 12}),
            (({'name': 'chicken_minion', 'tier': 11},
              {'name': 'enchanted_chicken', 'count': 1_024}),
             {'name': 'chicken_minion', 'tier': 12}),
            (({'name': 'mushroom_minion', 'tier': 11},
              {'name': 'enchanted_brown_mushroom', 'count': 512},
              {'name': 'enchanted_red_mushroom', 'count': 512}),
             {'name': 'mushroom_minion', 'tier': 12}),
            (({'name': 'cactus_minion', 'tier': 11},
              {'name': 'enchanted_cactus', 'count': 32}),
             {'name': 'cactus_minion', 'tier': 12}),
            (({'name': 'pig_minion', 'tier': 11},
              {'name': 'enchanted_grilled_pork', 'count': 32}),
             {'name': 'pig_minion', 'tier': 12}),
            (({'name': 'wheat_minion', 'tier': 11},
              {'name': 'enchanted_hay_bale', 'count': 32}),
             {'name': 'wheat_minion', 'tier': 12}),
            (({'name': 'cow_minion', 'tier': 11},
              {'name': 'enchanted_leather', 'count': 512}),
             {'name': 'cow_minion', 'tier': 12}),
            (({'name': 'melon_minion', 'tier': 11},
              {'name': 'enchanted_melon_block', 'count': 32}),
             {'name': 'melon_minion', 'tier': 12}),
            (({'name': 'nether_wart_minion', 'tier': 11},
              {'name': 'enchanted_nether_wart', 'count': 1_024}),
             {'name': 'nether_wart_minion', 'tier': 12}),
            (({'name': 'carrot_minion', 'tier': 11},
              {'name': 'enchanted_golden_carrot', 'count': 32}),
             {'name': 'carrot_minion', 'tier': 12}),
            (({'name': 'potato_minion', 'tier': 11},
              {'name': 'enchanted_baked_potato', 'count': 32}),
             {'name': 'potato_minion', 'tier': 12}),
            (({'name': 'sheep_minion', 'tier': 11},
              {'name': 'enchanted_cooked_mutton', 'count': 32}),
             {'name': 'sheep_minion', 'tier': 12}),
            (({'name': 'rabbit_minion', 'tier': 11},
              {'name': 'enchanted_rabbit_hide', 'count': 1_024}),
             {'name': 'rabbit_minion', 'tier': 12}),
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
