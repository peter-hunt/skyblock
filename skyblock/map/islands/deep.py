from ...object.mobs import get_mob
from ...object.resources import get_resource

from ..npc import get_npc
from ..object import *


__all__ = ['DEEP']

DEEP_ENTRANCE = Zone('deep_entrance', 0, 90, portal='gold')
GUNPOWDER_MINES = Zone(
    'gunpowder_mines', 5, 20,
    resources=[get_resource('stone'), get_resource('coal_ore'),
               get_resource('iron_ore'), get_resource('gold_ore')],
    mobs=[get_mob('sneaky_creeper')],
)
LAPIS_QUARRY = Zone(
    'lapis_quarry', -30, -35,
    resources=[get_resource('stone'), get_resource('lapis_ore')],
    mobs=[get_mob('lapis_zombie')],
)
PIGMANS_DEN = Zone(
    'pigmans_den', -10, 70,
    resources=[get_resource('stone'), get_resource('redstone_ore')],
    mobs=[get_mob('redstone_pigman')],
)
SLIMEHILL = Zone(
    'slimehill', 20, -10,
    resources=[get_resource('stone'), get_resource('emerald_ore')],
    mobs=[get_mob('small_emerald_slime'),
          get_mob('medium_emerald_slime'),
          get_mob('large_emerald_slime')],
)
DIAMOND_RESERVE = Zone(
    'diamond_reserve', -35, 15,
    resources=[get_resource('stone'), get_resource('diamond_ore')],
    mobs=[get_mob('diamond_zombie', level=15),
          get_mob('diamond_skeleton', level=15)],
)
OBSIDIAN_SANCTUARY = Zone(
    'obsidian_sanctuary', -10, 70, portal='mines',
    resources=[get_resource('stone'), get_resource('diamond_ore'),
               get_resource('diamond_block'), get_resource('obsidian')],
    mobs=[get_mob('diamond_zombie', level=20),
          get_mob('diamond_skeleton', level=20)],
)
LIFT = Zone(
    'lift', 50, 0,
    npcs=[get_npc('life_operator')],
)

DEEP_JOINTS = [
    DEEP_ENTRANCE, DIAMOND_RESERVE, GUNPOWDER_MINES, LAPIS_QUARRY, LIFT,
    OBSIDIAN_SANCTUARY, PIGMANS_DEN, SLIMEHILL,
]
DEEP_CONNS = [
    (DIAMOND_RESERVE, LIFT),
    (DIAMOND_RESERVE, OBSIDIAN_SANCTUARY),
    (DIAMOND_RESERVE, SLIMEHILL),
    (DEEP_ENTRANCE, GUNPOWDER_MINES),
    (GUNPOWDER_MINES, LAPIS_QUARRY),
    (GUNPOWDER_MINES, LIFT),
    (LAPIS_QUARRY, PIGMANS_DEN),
    (LAPIS_QUARRY, LIFT),
    (LIFT, OBSIDIAN_SANCTUARY),
    (LIFT, PIGMANS_DEN),
    (LIFT, SLIMEHILL),
    (PIGMANS_DEN, SLIMEHILL),
]

DEEP_DISTS = {}

for conn in DEEP_CONNS:
    add_dist(*conn, DEEP_DISTS)

DEEP = Island(
    'deep', 'deep_entrance', DEEP_JOINTS, DEEP_CONNS, DEEP_DISTS,
    skill_req=('mining', 5),
)
