from ...object.mobs import get_mob
from ...object.resources import get_resource

from ..object import *


__all__ = ['BARN']

ANIMAL_PEN = Zone(
    'animal_pen', 90, -230,
    mobs=[get_mob('chicken'), get_mob('cow'), get_mob('pig')],
)
POTATO_FIELD = Zone(
    'potato_field', 150, -245, portal='desert',
    resources=[get_resource('carrot'),
               get_resource('potato')],
)
PUMPKIN_FIELD = Zone(
    'pumpkin_field', 190, -225,
    resources=[get_resource('melon'),
               get_resource('pumpkin')],
)
WHEAT_FIELD = Zone(
    'wheat_field', 105, -220, portal='hub', fishable=True,
    resources=[get_resource('wheat')],
)

BARN_JOINTS = [ANIMAL_PEN, POTATO_FIELD, PUMPKIN_FIELD, WHEAT_FIELD]
BARN_CONNS = [
    (ANIMAL_PEN, POTATO_FIELD),
    (ANIMAL_PEN, WHEAT_FIELD),
    (POTATO_FIELD, PUMPKIN_FIELD),
    (POTATO_FIELD, WHEAT_FIELD),
    (PUMPKIN_FIELD, WHEAT_FIELD),
]

BARN_DISTS = {}

for conn in BARN_CONNS:
    add_dist(*conn, BARN_DISTS)

BARN = Island(
    'barn', 'wheat_field', BARN_JOINTS, BARN_CONNS, BARN_DISTS,
    skill_req=('farming', 1),
)
