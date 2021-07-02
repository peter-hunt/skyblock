from ...object.mob import get_mob
from ...object.resource import get_resource

from ..npc import get_npc
from ..object import Zone, Island, add_dist


__all__ = ['SPIDER']

FOSSIL = Zone(
    'fossil', -340, -255, portal='end', fishable=True,
    npcs=[get_npc('bramass_beastslayer')],
)
SPIDERS_PATH = Zone(
    'spiders_path', -315, -240, portal='hub',
    npcs=[get_npc('haysmith'), ],
    mobs=[get_mob('gravel_skeleton'),
          get_mob('rainy_slime')],
)
SPIDER_TOWER = Zone(
    'spider_tower', -380, -210,
    mobs=[get_mob('weaver_spider'),
          get_mob('voracious_spider'),
          get_mob('dasher_spider')],
)
GRAVEL_MINE = Zone(
    'gravel_mine', -250, -320, portal='nether',
    npcs=[get_npc('rick')],
    resources=[get_resource('gravel')],
)
TOP_OF_NEST = Zone(
    'nest', -365, -220,
    mobs=[get_mob('splitter_spider'),
          get_mob('weaver_spider'),
          get_mob('dasher_spider')],
)

SPIDER_REGIONS = [FOSSIL, SPIDERS_PATH, SPIDER_TOWER, GRAVEL_MINE, TOP_OF_NEST]
SPIDER_CONNS = [
    (FOSSIL, SPIDERS_PATH),
    (GRAVEL_MINE, SPIDERS_PATH),
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
