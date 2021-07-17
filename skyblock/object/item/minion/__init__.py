from ...object import *

from .combat import COMBAT_MINIONS as COMBAT
from .farming import FARMING_MINIONS as FARMING
from .fishing import FISHING_MINIONS as FISHING
from .foraging import FORAGING_MINIONS as FORAGING
from .mining import MINING_MINIONS as MINING


__all__ = ['MINIONS']

MINIONS = FARMING + MINING + COMBAT + FORAGING + FISHING
