from ...object import *

from .farming import FARMING_MINIONS as FARMING
from .mining import MINING_MINIONS as MINING


__all__ = [
    'MINIONS'
]

MINIONS = FARMING + MINING
