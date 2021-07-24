from json import load
from os import walk
from pathlib import Path
from typing import Optional

from ..function.io import *
from ..function.util import get, includes
from ..path import join_path

from .object import *


__all__ = ['RESOURCES', 'get_resource']


def load_resource(obj, /):
    if isinstance(obj, Resource):
        return obj
    elif obj['type'] == 'crop':
        return Crop.from_obj(obj)
    elif obj['type'] == 'mineral':
        return Mineral.from_obj(obj)
    elif obj['type'] == 'wood':
        return Wood.from_obj(obj)
    else:
        return obj


if not Path(join_path('skyblock', 'data', 'resources')).is_dir():
    raise FileNotFoundError(
        'Required data not found.\nRestart skyblock to fix it automatically.'
    )

RESOURCES = []
for file_name in [*walk(join_path('skyblock', 'data', 'resources'))][0][2]:
    if not file_name.endswith('.json'):
        continue

    with open(join_path('skyblock', 'data', 'resources', file_name)) as file:
        RESOURCES.append(load_resource(load(file)))


def get_resource(name: str, **kwargs) -> Optional[ItemType]:
    if includes(RESOURCES, name):
        return get(RESOURCES, name, **kwargs)
    else:
        red(f'Resource not found: {name!r}')
