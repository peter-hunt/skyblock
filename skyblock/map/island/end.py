from ...object.mob import get_mob
from ...object.resource import get_resource

from ..npc import get_npc
from ..object import Island, Zone, add_dist


__all__ = ['END']

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
END_CAVES = Zone(
    'end_caves', -580, -290,
    resources=[get_resource('end_stone'), get_resource('obsidian')],
    mobs=[get_mob('enderman', level=50)],
)
DRAGONS_NEST = Zone(
    'drag', -600, -280,
    resources=[get_resource('end_stone')],
    mobs=[get_mob('watcher'), get_mob('obsidian_defender'), get_mob('zealot')],
)

END_JOINTS = [END_ENTRENCE, END_TUNNEL, END_CAVES, DRAGONS_NEST]
END_CONNS = [
    (DRAGONS_NEST, END_CAVES),
    (END_ENTRENCE, END_TUNNEL),
    (END_CAVES, END_TUNNEL),
]

END_DISTS = {}

for conn in END_CONNS:
    add_dist(*conn, END_DISTS)

END = Island(
    'end', 'end_entrence', END_JOINTS, END_CONNS, END_DISTS,
    skill_req=('combat', 12),
)
