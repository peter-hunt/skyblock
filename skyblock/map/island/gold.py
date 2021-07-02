from ...object.resource import get_resource

from ..npc import get_npc
from ..object import Island, Zone, add_dist


__all__ = ['GOLD']

GOLD_GATE = Zone(
    'gold_gate', 0, -300, portal='hub',
    npcs=[get_npc('gold_forger'), get_npc('iron_forger')],
)
GOLD_MINE = Zone(
    'gold_mine', 0, -360, portal='deep',
    resources=[get_resource('stone'), get_resource('coal_ore'),
               get_resource('iron_ore'), get_resource('gold_ore')],
)

GOLD_JOINTS = [GOLD_GATE, GOLD_MINE]
GOLD_CONNS = [(GOLD_GATE, GOLD_MINE)]

GOLD_DISTS = {}

for conn in GOLD_CONNS:
    add_dist(*conn, GOLD_DISTS)

GOLD = Island(
    'gold', 'gold_gate', GOLD_JOINTS, GOLD_CONNS, GOLD_DISTS,
    skill_req=('mining', 1),
)
