from .combat import *
from .combat import __all__ as __combat__
from .enchanting import *
from .enchanting import __all__ as __enchanting__
from .farming import *
from .farming import __all__ as __farming__
from .fishing import *
from .fishing import __all__ as __fishing__
from .foraging import *
from .foraging import __all__ as __foraging__
from .mining import *
from .mining import __all__ as __mining__


__all__ = (
    ['PETS'] + __combat__ + __enchanting__ + __farming__ + __fishing__
    + __foraging__ + __mining__
)

PETS = (
    COMBAT_PETS + ENCHANTING_PETS + FARMING_PETS + FISHING_PETS + FORAGING_PETS
    + MINING_PETS
)
