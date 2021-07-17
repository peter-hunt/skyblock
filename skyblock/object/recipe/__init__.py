from json import load
from os import walk
from typing import List, Optional, Union

from ...function.io import *
from ...function.path import join_path
from ...function.util import includes, get
from ...myjson import dump

from ..object import *

# from .combat import COMBAT_RECIPES as _COMBAT
# from .combat_minion import COMBAT_MINION_RECIPES as _COMBAT_MINION
# from .farming import FARMING_RECIPES as _FARMING
# from .farming_minion import FARMING_MINION_RECIPES as _FARMING_MINION
# from .foraging import FORAGING_RECIPES as _FORAGING
# from .foraging_minion import FORAGING_MINION_RECIPES as _FORAGING_MINION
# from .fishing import FISHING_RECIPES as _FISHING
# from .fishing_minion import FISHING_MINION_RECIPES as _FISHING_MINION
# from .mining import MINING_RECIPES as _MINING
# from .mining_minion import MINING_MINION_RECIPES as _MINING_MINION
# from .misc import MISC_RECIPES as MISC

__all__ = ['RECIPES', 'CRAFTABLES', 'get_recipe']


def _select_recipes(recipes: List[Recipe], category: str) -> List[Recipe]:
    has_not_req = [recipe for recipe in recipes
                   if recipe.collection_req is not None
                   and recipe.category == category]
    has_req = [recipe for recipe in recipes
               if recipe.collection_req is None
               and recipe.category == category]

    return has_not_req + has_req


_RECIPES = []
RECIPES = []
for category in [*walk(join_path('skyblock', 'data', 'recipes'))][0][1]:
    for file_name in sorted([*walk(join_path('skyblock', 'data',
                                   'recipes', category))][0][2]):
        if not file_name.endswith('.json'):
            continue

        with open(join_path('skyblock', 'data', 'recipes',
                            category, file_name)) as file:
            obj = load(file)
            if 'recipes' in obj:
                _RECIPES.append(RecipeGroup.load(obj))
            else:
                _RECIPES.append(Recipe.load(obj))
for recipe in _RECIPES:
    if recipe.category not in {'farming', 'combat', 'mining', 'fishing', 'foraging',
                               'enchanting', 'forging', 'smelting'}:
        print(recipe.category)
        exit()


for category in {'farming', 'combat', 'mining', 'fishing', 'foraging',
                 'enchanting', 'forging', 'smelting'}:
    RECIPES.extend(_select_recipes(_RECIPES, category))

CRAFTABLES = [recipe for recipe in RECIPES
              if isinstance(recipe, Recipe)]


def get_recipe(name: str, warn: bool = True
               ) -> Optional[Union[Recipe, RecipeGroup]]:
    if not includes(RECIPES, name):
        if warn:
            red(f'Recipe or Group not found: {name!r}')
        return
    return get(RECIPES, name)
