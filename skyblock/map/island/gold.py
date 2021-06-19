from ...object.item import get_item
from ...object.object import Item
from ...object.resource import get_resource
from ..object import Island, Npc, Region, add_dist

__all__ = ['GOLD']


GOLD_GATE = Region(
    'gold_gate', 0, -300,
    npcs=[
        Npc('gold_forger',
            init_dialog=[
                'I love goooold!',
                'Talk to me again to open the Gold Forger Shop!',
            ],
            trades=[
                (5.5, Item('gold')),
                (10, get_item('golden_helmet')),
                (16, get_item('golden_chestplate')),
                (14, get_item('golden_leggings')),
                (9, get_item('golden_boots')),
                (80, get_item('fancy_sword')),
            ]),
        Npc('iron_forger',
            init_dialog=[
                "For my wares, you'll have to pay the iron price!",
                'Seriously though, I accept Coins',
                'Talk to me again to open the Iron Forger Shop!',
            ],
            trades=[
                (60, get_item('iron_pickaxe')),
                (5, Item('iron')),
                (50, get_item('chainmail_helmet')),
                (100, get_item('chainmail_chestplate')),
                (75, get_item('chainmail_leggings')),
                (100, get_item('chainmail_boots')),
            ]),
    ],
    portal='hub',
)
GOLD_MINE = Region(
    'gold_mine', 0, -360,
    resources=[get_resource('stone'), get_resource('coal_ore'),
               get_resource('iron_ore'), get_resource('gold_ore')],
    portal='deep',
)

GOLD_JOINTS = [GOLD_GATE, GOLD_MINE]
GOLD_CONNS = [
    (GOLD_GATE, GOLD_MINE),
]

GOLD_DISTS = {}

for conn in GOLD_CONNS:
    add_dist(*conn, GOLD_DISTS)

GOLD = Island(
    'gold', 'gold_gate', GOLD_JOINTS, GOLD_CONNS, GOLD_DISTS,
    skill_req=('mining', 1),
)
