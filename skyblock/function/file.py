from json import load
from os.path import join
from os import walk
from pathlib import Path
from types import FunctionType

from .._lib import _open


__all__ = ['load_folder', 'load_recipes']


def load_folder(path: str | Path, load_func: FunctionType=None, /, *, json=True) -> list:
    result = []
    for subpath, folders, file_names in walk(path):
        for file_name in file_names:
            if json and not file_name.endswith('.json'):
                continue
            with _open(join(subpath, file_name)) as file:
                if json is not None:
                    content = load(file)
                else:
                    content = file.read()
                if load_func is not None:
                    content = load_func(content)
                result.append(content)
    return result


def load_recipes(path: str | Path, load_recipe: FunctionType, load_group: FunctionType) -> list:
    result = []
    for subpath, folders, file_names in walk(path):
        for file_name in file_names:
            if not file_name.endswith('.json'):
                continue
            with _open(join(subpath, file_name)) as file:
                obj = load(file)
                if 'recipes' in obj:
                    result.append(load_group(obj))
                else:
                    result.append(load_recipe(obj))
    return result
