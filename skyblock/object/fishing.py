from json import load

from ..function.path import join_path

from .object import *


__all__ = ['FISHING_TABLE', 'SEA_CREATRUE_TABLE']

with open(join_path('skyblock', 'data',
                    'fishing', 'fishing_table.json')) as file:
    FISHING_TABLE = load(file)

with open(join_path('skyblock', 'data',
                    'fishing', 'sea_creature_table.json')) as file:
    SEA_CREATRUE_TABLE = load(file)
