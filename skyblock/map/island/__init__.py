from ...function.io import *
from ...function.util import get, includes

from ..object import *

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


__all__ = ['ISLANDS', 'get_island']

ISLANDS = [HUB, BARN, DESERT, GOLD, DEEP, MINES, PARK, SPIDER, NETHER, END]


def get_island(name: str, **kwargs) -> Npc:
    if not includes(ISLANDS, name):
        red(f'Island not found: {name!r}')
        exit()
    return get(ISLANDS, name, **kwargs)
