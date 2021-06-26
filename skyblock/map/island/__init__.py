from .barn import BARN
from .deep import DEEP
from .desert import DESERT
from .end import END
from .gold import GOLD
from .hub import HUB
from .mines import MINES
from .nether import NETHER
from .park import PARK
from .spider import SPIDER


__all__ = [
    'ISLANDS',
    'HUB', 'BARN', 'DESERT', 'GOLD', 'DEEP', 'MINES',
    'NETHER', 'PARK', 'SPIDER', 'END']

ISLANDS = [HUB, BARN, DESERT, GOLD, DEEP, MINES, PARK, SPIDER, NETHER, END]
