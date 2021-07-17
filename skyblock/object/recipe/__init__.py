from typing import List, Optional, Union

from ...function.io import *
from ...function.util import includes, get

from ..object import *

from .combat import COMBAT_RECIPES as _COMBAT
from .combat_minion import COMBAT_MINION_RECIPES as _COMBAT_MINION
from .farming import FARMING_RECIPES as _FARMING
from .farming_minion import FARMING_MINION_RECIPES as _FARMING_MINION
from .foraging import FORAGING_RECIPES as FORAGING
from .fishing import FISHING_RECIPES as FISHING
from .mining import MINING_RECIPES as _MINING
from .mining_minion import MINING_MINION_RECIPES as _MINING_MINION
from .misc import MISC_RECIPES as MISC

__all__ = ['RECIPES', 'CRAFTABLES', 'get_recipe']


def _gen_recipes(recipes: List[Recipe],
                 minion_recipes: List[Recipe]) -> List[Recipe]:
    _recipes = [recipe for recipe in recipes
                if recipe.collection_req is not None]
    result = [recipe for recipe in recipes
              if recipe.collection_req is None]
    collections = [*{recipe.collection_req[0] for recipe in _recipes}]

    for collection in collections:
        for recipe in minion_recipes:
            if recipe.collection_req[0] == collection:
                result.append(recipe)
        for recipe in _recipes:
            if recipe.collection_req[0] == collection:
                result.append(recipe)

    return result


FARMING = _gen_recipes(_FARMING, _FARMING_MINION)
MINING = _gen_recipes(_MINING, _MINING_MINION)
COMBAT = _gen_recipes(_COMBAT, _COMBAT_MINION)
RECIPES = FARMING + MINING + COMBAT + FORAGING + FISHING + MISC
CRAFTABLES = [recipe for recipe in RECIPES
              if isinstance(recipe, Recipe)]


def get_recipe(name: str, warn: bool = True
               ) -> Optional[Union[Recipe, RecipeGroup]]:
    if not includes(RECIPES, name):
        if warn:
            red(f'Recipe or Group not found: {name!r}')
        return
    return get(RECIPES, name)
