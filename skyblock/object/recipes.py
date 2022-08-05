from pathlib import Path

from ..constant.util import Number
from ..function.file import load_recipes
from ..function.io import *
from ..function.util import includes, get
from ..path import join_path

from .items import *
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


for recipe in _RECIPES:
    if isinstance(recipe, RecipeGroup):
        continue

    for pointer in recipe.ingredients + [recipe.result]:
        if isinstance(pointer, Number):
            continue

        pointer = pointer.copy()
        name = pointer['name']
        if not includes(ITEMS, name):
            yellow(f'Item not found: {name!r} in recipe {recipe.name!r}')
            continue
        del pointer['name']
        if get(ITEMS, name, **pointer) is None:
            yellow(f'Invalid item: {name!r} in recipe {recipe.name!r}')
