from typing import Optional

from ...function.io import *
from ...function.util import includes, get

from ..object import *

from .combat import *
from .combat import __all__ as __combat__
from .farming import *
from .farming import __all__ as __farming__
from .foraging import *
from .foraging import __all__ as __foraging__
from .fishing import *
from .fishing import __all__ as __fishing__
from .mining import *
from .mining import __all__ as __mining__
from .misc import *
from .misc import __all__ as __misc__


__all__ = (
    __combat__ + __farming__ + __fishing__ + __foraging__
    + __mining__ + __misc__ + ['get_recipe']
)

RECIPES = (
    FARMING_RECIPES + MINING_RECIPES + COMBAT_RECIPES + FORAGING_RECIPES
    + FISHING_RECIPES + MISC_RECIPES
)


def get_recipe(name: str, **kwargs) -> Optional[Recipe]:
    if not includes(RECIPES, name):
        red(f'Recipe not found: {name!r}')
        return
    return get(RECIPES, name, **kwargs)
