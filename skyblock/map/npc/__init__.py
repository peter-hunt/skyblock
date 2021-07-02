from ...function.io import red
from ...function.util import get, includes

from ..object import Npc

from .desert import DESERT_NPCS
from .end import END_NPCS
from .gold import GOLD_NPCS
from .hub import HUB_NPCS
from .mines import MINES_NPCS
from .nether import NETHER_NPCS
from .park import PARK_NPCS
from .spider import SPIDER_NPCS

__all__ = ['NPCS', 'get_npc']

NPCS = (
    HUB_NPCS + DESERT_NPCS + GOLD_NPCS + MINES_NPCS
    + SPIDER_NPCS + NETHER_NPCS + END_NPCS + PARK_NPCS
)


def get_npc(name: str, **kwargs) -> Npc:
    if not includes(NPCS, name):
        red(f'Npc not found: {name!r}')
        exit()
    return get(NPCS, name, **kwargs)
