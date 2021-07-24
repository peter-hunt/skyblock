from json import load
from os import walk
from pathlib import Path
from typing import List, Optional, Union

from ..function.io import *
from ..function.util import includes, get
from ..path import join_path

from .object import *

__all__ = ['RECIPES', 'CRAFTABLES', 'get_recipe']


def _select_recipes(recipes: List[Recipe], category: str) -> List[Recipe]:
    has_not_req = [recipe for recipe in recipes
                   if recipe.collection_req is not None
                   and recipe.category == category]
    has_req = [recipe for recipe in recipes
               if recipe.collection_req is None
               and recipe.category == category]

    return has_not_req + has_req


if not Path(join_path('skyblock', 'data', 'recipes')).is_dir():
    raise FileNotFoundError(
        'Required data not found.\n'
        'Restart skyblock to fix it automatically.'
    )

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
                _RECIPES.append(RecipeGroup.from_obj(obj))
            else:
                _RECIPES.append(Recipe.from_obj(obj))
_RECIPES = sorted(_RECIPES, key=lambda recipe: recipe.name)


for category in {'farming', 'combat', 'mining', 'fishing', 'foraging',
                 'enchanting', 'forging', 'smelting'}:
    RECIPES.extend(_select_recipes(_RECIPES, category))

CRAFTABLES = [recipe for recipe in RECIPES
              if isinstance(recipe, Recipe)]


def get_recipe(name: str, /, *, warn: bool = True
               ) -> Optional[Union[Recipe, RecipeGroup]]:
    if not includes(RECIPES, name):
        if warn:
            red(f'Recipe or Group not found: {name!r}')
        return
    return get(RECIPES, name)
