from ...item.item import get_item
from ...item.resource import get_resource

from ..object import Npc, Region, Island, add_dist

__all__ = ['PARK']


BIRCH_PARK = Region(
    'birch_park', -300, -20,
    resources=[get_resource('birch')],
    portal='hub',
)
SPRUCE_WOOD = Region(
    'spruce_wood', -325, 0,
    resources=[get_resource('spruce')],
    npcs=[
        Npc('melancholic_viking',
            init_dialog=[
                "For my wares, you'll have to pay the iron price!",
                'Seriously though, I accept Coins',
                'Talk to me again to open the Iron Forger Shop!',
            ],
            trades=[
                (130_000, get_item('raider_axe')),
            ]),
    ],
    skill_req=('foraging', 2),
)
DARK_THICKET = Region(
    'dark_thicket', -330, -45,
    resources=[get_resource('dark_oak')],
    skill_req=('foraging', 3),
)
SAVANNA_WOODLAND = Region(
    'savanna_woodland', -350, -15,
    resources=[get_resource('acacia')],
    npcs=[
        Npc('master_tactician_funk',
            trades=[
                (35_000, get_item('tacticians_sword')),
            ]),
    ],
    skill_req=('foraging', 4),
)
JUNGLE_ISLAND = Region(
    'jungle_island', -55, -60,
    resources=[get_resource('jungle')],
    skill_req=('foraging', 5),
)

PARK_JOINTS = [
    BIRCH_PARK, SPRUCE_WOOD, DARK_THICKET, SAVANNA_WOODLAND, JUNGLE_ISLAND,
]
PARK_CONNS = [
    (BIRCH_PARK, SPRUCE_WOOD),
    (DARK_THICKET, SAVANNA_WOODLAND),
    (DARK_THICKET, SPRUCE_WOOD),
    (JUNGLE_ISLAND, SAVANNA_WOODLAND),
]

PARK_DISTS = {}

for conn in PARK_CONNS:
    add_dist(*conn, PARK_DISTS)

PARK = Island(
    'park', 'birch', PARK_JOINTS, PARK_CONNS, PARK_DISTS,
    skill_req=('foraging', 1),
)
