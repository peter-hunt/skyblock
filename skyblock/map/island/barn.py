from ...object.resource import get_resource

from ..object import Region, Island, add_dist

__all__ = ['BARN']


POTATO_FIELD = Region(
    'potato_field', 150, -245,
    resources=[
        get_resource('carrot'),
        get_resource('potato'),
    ],
)
PUMPKIN_FIELD = Region(
    'pumpkin_field', 190, -225,
    resources=[
        get_resource('melon'),
        get_resource('pumpkin'),
    ],
)
WHEAT_FIELD = Region(
    'wheat_field', 105, -220,
    resources=[get_resource('wheat')],
    portal='hub',
)

BARN_JOINTS = [POTATO_FIELD, PUMPKIN_FIELD, WHEAT_FIELD]
BARN_CONNS = [
    (POTATO_FIELD, WHEAT_FIELD),
    (POTATO_FIELD, PUMPKIN_FIELD),
    (PUMPKIN_FIELD, WHEAT_FIELD),
]

BARN_DISTS = {}

for conn in BARN_CONNS:
    add_dist(*conn, BARN_DISTS)

BARN = Island(
    'barn', 'wheat_field', BARN_JOINTS, BARN_CONNS, BARN_DISTS,
    skill_req=('farming', 1),
)
