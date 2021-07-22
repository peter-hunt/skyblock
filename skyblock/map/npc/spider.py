from ...constant.colors import *

from ..object import *


SPIDER_NPCS = [
    Npc('bramass_beastslayer',
        init_dialog=[
            (f"Hello, adventurer! I am {RED}Bramass Beastslayer{WHITE}!"
             f" I've slain beasts of all sorts across SkyBlock"),
            ('I sure wish there was a record all of'
             ' my accomplishments in one place!'),
            'Oh wait...there is!',
            (f'Your {BLUE}Bestiary{WHITE} is'
             f' a compendium of all of the mobs in SkyBlock!'),
            'View your mob stats, unlock rewards, and more!',
            f"You can find the Bestiary with {GREEN}/bestiary{WHITE}!",
        ],
        dialog=[[
            (f'Killing enough mobs in a given {GREEN}Family{WHITE}'
             f' unlocks {GREEN}rewards{WHITE}!'),
            (f'You can unlock {AQUA}Magic Find{WHITE}, Strength bonuses,'
             f' and loot drop information for that Family!'),
            ('Reach Milestones in your Beastiary'
             ' by unlocking unique Family tiers'),
            (f'Reaching Milestones rewards Health,'
             f' {BLUE}Combat Exp{WHITE}, and more!'),
            (f'You can always view your Beastiary'
             f' with {GREEN}/bestiary{WHITE}!'),
            (f'Killing mobs in a Family enough times rewards you '
             f'with {AQUA}Magic Find{WHITE} towards that mob!'),
            ('This increases your chance to find rare loot'
             ' when killing this mob!')],
        ]),
    Npc('haysmith',
        init_dialog=[
            'Easy there, adventurer! Lots of spiders creeping about!',
            'Personally I love them, collecting string is my passion.',
            'You should try it!',
        ],
        dialog=[
            'String! Yes! Wow!',
            ("The gravel on this island seems to magically reappear"
             " when you break it. I don't ask questions"),
            ('Those Dashing Spiders are pretty obnoxious.'
             ' I find a well-placed arrow can help with that.'),
        ]),
    Npc('rick',
        dialog=[
            'Careful when it rains around here, it gets dangerous!',
            "Have you met Pat? He's my brother, We're the Flint Bros!",
            'Mining gravel is hard work, but the flint is worth it.',
        ]),
    Npc('shaggy',
        dialog=[
            ('I used to think this world was peaceful, but there are some'
             ' beings in this world that are stronger than I could ever hope'
             ' to handle...'),
        ]),
]
