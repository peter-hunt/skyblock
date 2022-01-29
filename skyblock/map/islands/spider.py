from ...object.mobs import get_mob
from ...object.resources import get_resource

from ..npc import get_npc
from ..object import *


__all__ = ['SPIDER']

DARK_SPIDER_CAVES = Zone(
    'dark_spider_caves', -240, -335,
    mobs=[get_mob('dasher_spider', level=50),
          get_mob('voracious_spider', level=50)],
)
DEEPER_SPIDER_CAVES = Zone(
    'deeper_spider_caves', -215, -330,
    mobs=[get_mob('dasher_spider', level=45),
          get_mob('voracious_spider', level=45)],
)
FOSSIL = Zone(
    'fossil', -340, -255, portal='end', fishable=True,
    npcs=[get_npc('bramass_beastslayer'),
          get_npc('grandma_wolf'),
          get_npc('shaggy')],
)
SPIDER_CAVES = Zone(
    'spider_caves', -235, -315,
    mobs=[get_mob('dasher_spider', level=42),
          get_mob('voracious_spider', level=42)],
)
SPIDERS_PATH = Zone(
    'spiders_path', -315, -240, portal='hub',
    npcs=[get_npc('haysmith')],
    mobs=[get_mob('gravel_skeleton'),
          get_mob('rain_slime')],
)
SPIDER_TOWER = Zone(
    'spider_tower', -380, -210,
    mobs=[get_mob('weaver_spider', level=3),
          get_mob('voracious_spider', level=10),
          get_mob('dasher_spider', level=4)],
)
GRAVEL_MINE = Zone(
    'gravel_mine', -250, -320, portal='nether',
    npcs=[get_npc('rick')],
    resources=[get_resource('gravel')],
)
TOP_OF_NEST = Zone(
    'nest', -365, -220,
    mobs=[get_mob('splitter_spider'),
          get_mob('weaver_spider', level=5),
          get_mob('dasher_spider')],
)

SPIDER_REGIONS = [
    DARK_SPIDER_CAVES, DEEPER_SPIDER_CAVES, FOSSIL, SPIDER_CAVES, SPIDERS_PATH,
    SPIDER_TOWER, GRAVEL_MINE, TOP_OF_NEST,
]
SPIDER_CONNS = [
    (DARK_SPIDER_CAVES, DEEPER_SPIDER_CAVES),
    (DEEPER_SPIDER_CAVES, SPIDER_CAVES),
    (FOSSIL, SPIDER_CAVES),
    (FOSSIL, SPIDERS_PATH),
    (SPIDER_CAVES, SPIDERS_PATH),
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
