from .axe import *
from .axe import __all__ as __axe__
from .fishing_rod import *
from .fishing_rod import __all__ as __fishing_rod__
from .hoe import *
from .hoe import __all__ as __hoe__
from .pickaxe import *
from .pickaxe import __all__ as __pickaxe__


__all__ = ['TOOLS'] + __axe__ + __fishing_rod__ + __hoe__ + __pickaxe__

TOOLS = AXES + FISHING_RODS + HOES + PICKAXES
