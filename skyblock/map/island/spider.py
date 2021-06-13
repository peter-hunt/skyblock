from ...item.mob import get_mob

from ..object import Region, Island, add_dist

__all__ = ['SPIDER']


SPIDERS_PATH = Region(
    'spiders_path', -315, -240,
    portal='hub',
)
SPIDER_TOWER = Region(
    'spider_tower', -365, -220,
    mobs=[get_mob('splitter_spider'),
          get_mob('weaver_spider'),
          get_mob('voracious_spider'),
          get_mob('dasher_spider')],
)
FOSSIL = Region(
    'fossil', -340, -255,
    portal='end',
)

SPIDER_JOINTS = [SPIDERS_PATH, SPIDER_TOWER, FOSSIL]
SPIDER_CONNS = [
    (FOSSIL, SPIDERS_PATH),
    (SPIDER_TOWER, SPIDERS_PATH),
]

SPIDER_DISTS = {}

for conn in SPIDER_CONNS:
    add_dist(*conn, SPIDER_DISTS)

SPIDER = Island(
    'spider', 'spiders_path', SPIDER_JOINTS, SPIDER_CONNS, SPIDER_DISTS,
    skill_req=('combat', 1),
)
