from pathlib import Path

from ..function.file import load_recipes
from ..function.io import red
from ..function.util import includes, get
from ..path import join_path

from .object import *

__all__ = ['RECIPES', 'CRAFTABLES', 'get_recipe']


def _select_recipes(recipes: list[Recipe], category: str) -> list[Recipe]:
    has_not_req = [recipe for recipe in recipes
                   if recipe.collection_req is not None
                   and recipe.category == category]
    has_req = [recipe for recipe in recipes
               if recipe.collection_req is None
               and recipe.category == category]

    return has_not_req + has_req


if not Path(join_path('skyblock', 'data', 'recipes')).is_dir():
    raise FileNotFoundError(
        'Required data not found.\nRestart skyblock to fix it automatically.'
    )

_RECIPES = load_recipes(join_path('skyblock', 'data', 'recipes'), Recipe.from_obj, RecipeGroup.from_obj)
_RECIPES = sorted(_RECIPES, key=lambda recipe: recipe.name)


RECIPES = []
for category in {'farming', 'combat', 'mining', 'fishing', 'foraging',
                 'enchanting', 'forging', 'smelting'}:
    RECIPES.extend(_select_recipes(_RECIPES, category))

CRAFTABLES = [recipe for recipe in RECIPES
              if isinstance(recipe, Recipe)]


def get_recipe(name: str, /, *, warn: bool = True
               ) -> Recipe | RecipeGroup | None:
    if includes(RECIPES, name):
        return get(RECIPES, name)
    elif warn:
        red(f'Recipe or Group not found: {name!r}')
