from ...object.mob import get_mob
from ...object.resource import get_resource

from ..object import Region, Island, add_dist


__all__ = ['BARN']

ANIMAL_PEN = Region(
    'animal_pen', 90, -230,
    mobs=[get_mob('chicken'), get_mob('cow'), get_mob('pig')])
POTATO_FIELD = Region(
    'potato_field', 150, -245,
    resources=[get_resource('carrot'),
               get_resource('potato')],
    portal='desert')
PUMPKIN_FIELD = Region(
    'pumpkin_field', 190, -225,
    resources=[get_resource('melon'),
               get_resource('pumpkin')])
WHEAT_FIELD = Region(
    'wheat_field', 105, -220,
    resources=[get_resource('wheat')],
    portal='hub')

BARN_JOINTS = [ANIMAL_PEN, POTATO_FIELD, PUMPKIN_FIELD, WHEAT_FIELD]
BARN_CONNS = [
    (ANIMAL_PEN, POTATO_FIELD),
    (ANIMAL_PEN, WHEAT_FIELD),
    (POTATO_FIELD, PUMPKIN_FIELD),
    (POTATO_FIELD, WHEAT_FIELD),
    (PUMPKIN_FIELD, WHEAT_FIELD)]

BARN_DISTS = {}

for conn in BARN_CONNS:
    add_dist(*conn, BARN_DISTS)

BARN = Island(
    'barn', 'wheat_field', BARN_JOINTS, BARN_CONNS, BARN_DISTS,
    skill_req=('farming', 1))
