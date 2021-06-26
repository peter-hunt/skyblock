from ...object.item import get_item, get_scroll
from ...object.mob import get_mob
from ...object.resource import get_resource

from ..object import Npc, Region, Island, add_dist


__all__ = ['PARK']

BIRCH_PARK = Region(
    'birch', -300, -20,
    resources=[get_resource('birch_wood')],
    portal='hub')
HOWLING_CAVE = Region(
    'howl', -330, -55,
    mobs=[get_mob('pack_spirit'),
          get_mob('soul_of_the_alpha')])
SPRUCE_WOOD = Region(
    'spruce', -325, 0,
    resources=[get_resource('spruce_wood')],
    npcs=[
        Npc('melancholic_viking',
            init_dialog=[
                "For my wares, you'll have to pay the iron price!",
                'Seriously though, I accept Coins',
                'Talk to me again to open the Iron Forger Shop!',
            ],
            trades=[
                (130_000, get_item('raider_axe')),
                (70_000, get_scroll('jungle')), ]), ],
    skill_req=('foraging', 2))
DARK_THICKET = Region(
    'dark', -330, -45,
    resources=[get_resource('dark_oak_wood')],
    skill_req=('foraging', 3))
SAVANNA_WOODLAND = Region(
    'savanna', -350, -15,
    resources=[get_resource('acacia_wood')],
    npcs=[
        Npc('master_tactician_funk',
            trades=[(35_000, get_item('tacticians_sword'))]), ],
    skill_req=('foraging', 4))
JUNGLE_ISLAND = Region(
    'jungle', -55, -60,
    resources=[get_resource('jungle_wood')],
    skill_req=('foraging', 5))

PARK_JOINTS = [
    BIRCH_PARK, HOWLING_CAVE, SPRUCE_WOOD,
    DARK_THICKET, SAVANNA_WOODLAND, JUNGLE_ISLAND]
PARK_CONNS = [
    (BIRCH_PARK, HOWLING_CAVE),
    (BIRCH_PARK, SPRUCE_WOOD),
    (DARK_THICKET, SAVANNA_WOODLAND),
    (DARK_THICKET, SPRUCE_WOOD),
    (JUNGLE_ISLAND, SAVANNA_WOODLAND)]

PARK_DISTS = {}

for conn in PARK_CONNS:
    add_dist(*conn, PARK_DISTS)

PARK = Island(
    'park', 'birch', PARK_JOINTS, PARK_CONNS, PARK_DISTS,
    skill_req=('foraging', 1))
