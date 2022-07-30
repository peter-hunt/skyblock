from json import load
from pathlib import Path

from .._lib import _open
from ..myjson import dump
from ..path import join_path


__all__ = ['OPTIONS']

with _open(join_path('skyblock', 'data', 'default_options.json')) as file:
    default_options = load(file)

if not Path(join_path('skyblock', 'options.json')).is_file():
    raise FileNotFoundError(
        'Required data not found.\nRestart skyblock to fix it automatically.'
    )

OPTIONS = default_options.copy()

with _open(join_path('skyblock', 'options.json')) as file:
    obj = load(file)
    if isinstance(obj.get('debug', None), bool):
        OPTIONS['debug'] = obj['debug']

with open(join_path('skyblock', 'options.json'), 'w') as file:
    dump(OPTIONS, file)
