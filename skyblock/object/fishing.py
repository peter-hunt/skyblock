from json import load
from pathlib import Path

from .._lib import _open
from ..path import join_path

from .object import *


__all__ = ['FISHING_TABLE', 'SEA_CREATRUE_TABLE']

if not Path(join_path('skyblock', 'data', 'fishing')).is_dir():
    raise FileNotFoundError(
        'Required data not found.\nRestart skyblock to fix it automatically.'
    )

with _open(join_path('skyblock', 'data',
                     'fishing', 'fishing_table.json')) as file:
    FISHING_TABLE: list = load(file)

with _open(join_path('skyblock', 'data',
                     'fishing', 'sea_creature_table.json')) as file:
    SEA_CREATRUE_TABLE = load(file)
