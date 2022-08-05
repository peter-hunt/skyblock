from pathlib import Path

from ..function.file import load_folder
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
    elif obj['type'] == 'log':
        return Log.from_obj(obj)
    elif obj['type'] == 'mineral':
        return Mineral.from_obj(obj)
    else:
        red(f"Invalid Resource type: {obj['type']}")
        exit()


if not Path(join_path('skyblock', 'data', 'resources')).is_dir():
    raise FileNotFoundError(
        'Required data not found.\nRestart skyblock to fix it automatically.'
    )

RESOURCES = load_folder(join_path('skyblock', 'data', 'resources'), load_resource)


def get_resource(name: str, **kwargs) -> ItemType | None:
    if includes(RESOURCES, name):
        return get(RESOURCES, name, **kwargs)
    else:
        red(f'Resource not found: {name!r}')
