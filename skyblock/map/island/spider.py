from ...item.mob import get_mob

from ..object import Region, Island, add_dist

__all__ = ['SPIDER']


FOSSIL = Region(
    'fossil', -340, -255,
    portal='end',
)
SPIDERS_PATH = Region(
    'spiders_path', -315, -240,
    portal='hub',
)
SPIDER_TOWER = Region(
    'spider_tower', -380, -210,
    mobs=[get_mob('weaver_spider'),
          get_mob('voracious_spider'),
          get_mob('dasher_spider')],
)
TOP_OF_NEST = Region(
    'nest', -365, -220,
    mobs=[get_mob('splitter_spider'),
          get_mob('weaver_spider'),
          get_mob('dasher_spider')],
)

SPIDER_REGIONS = [FOSSIL, SPIDERS_PATH, SPIDER_TOWER, TOP_OF_NEST]
SPIDER_CONNS = [
    (FOSSIL, SPIDERS_PATH),
    (SPIDER_TOWER, SPIDERS_PATH),
    (TOP_OF_NEST, SPIDER_TOWER),
]

SPIDER_DISTS = {}

for conn in SPIDER_CONNS:
    add_dist(*conn, SPIDER_DISTS)

SPIDER = Island(
    'spider', 'spiders_path', SPIDER_REGIONS, SPIDER_CONNS, SPIDER_DISTS,
    skill_req=('combat', 1),
)
