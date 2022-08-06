from ...object.mobs import get_mob
from ...object.resources import get_resource

from ..npc import get_npc
from ..object import *


__all__ = ['END']

DRAGONS_NEST = Zone(
    'drag', -600, -280,
    resources=[get_resource('end_stone'), get_resource('obsidian')],
    mobs=[get_mob('watcher'), get_mob('obsidian_defender'),
          get_mob('zealot'), get_mob('endermite', level=40)],
)
END_CAVES = Zone(
    'end_caves', -580, -290,
    resources=[get_resource('end_stone'), get_resource('obsidian')],
    mobs=[get_mob('enderman', level=50)],
)
END_ENTRENCE = Zone(
    'end_entrence', -540, -300, portal='spider',
    npcs=[get_npc('pearl_dealer')],
    resources=[get_resource('end_stone'), get_resource('obsidian')],
    mobs=[get_mob('enderman', level=42)],
)
END_TUNNEL = Zone(
    'end_tunnel', -560, -300,
    resources=[get_resource('end_stone'), get_resource('obsidian')],
    mobs=[get_mob('enderman', level=45)],
)
VOID_SEPULTURE = Zone(
    'void', -575, -320,
    resources=[get_resource('end_stone'), get_resource('obsidian')],
    mobs=[get_mob('voidling_fanatic'), get_mob('voidling_extremist')],
    skill_req=('combat', 25),
)

END_JOINTS = [
    DRAGONS_NEST, END_CAVES, END_ENTRENCE, END_TUNNEL, VOID_SEPULTURE,
]
END_CONNS = [
    (DRAGONS_NEST, END_CAVES),
    (DRAGONS_NEST, VOID_SEPULTURE),
    (END_CAVES, END_TUNNEL),
    (END_ENTRENCE, END_TUNNEL),
]

END_DISTS = {}

for conn in END_CONNS:
    add_dist(*conn, END_DISTS)

END = Island(
    'end', 'end_entrence', END_JOINTS, END_CONNS, END_DISTS,
    skill_req=('combat', 12),
)
