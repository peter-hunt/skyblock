from typing import Optional

from ...function.io import red
from ...function.util import includes, get

from ..object import Recipe

from .combat import *
from .combat import __all__ as __combat_all__
from .farming import *
from .farming import __all__ as __farming_all__
from .foraging import *
from .foraging import __all__ as __foraging_all__
from .fishing import *
from .fishing import __all__ as __fishing_all__
from .mining import *
from .mining import __all__ as __mining_all__
from .misc import *
from .misc import __all__ as __misc_all__


__all__ = (
    __combat_all__ + __farming_all__ + __fishing_all__ + __foraging_all__
    + __mining_all__ + __misc_all__
    + ['get_recipe']
)

RECIPES = (
    COMBAT_RECIPES + FARMING_RECIPES + FISHING_RECIPES + FORAGING_RECIPES
    + MINING_RECIPES + MISC_RECIPES
)


def get_recipe(name: str, **kwargs) -> Optional[Recipe]:
    if not includes(RECIPES, name):
        red(f'Invalid recipe: {name!r}')
        return
    return get(RECIPES, name, **kwargs)
