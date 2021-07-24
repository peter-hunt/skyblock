from json import load
from os import walk
from pathlib import Path

from ..path import join_path


__all__ = ['MINION_LOOT']

if not Path(join_path('skyblock', 'data', 'minions')).is_dir():
    raise FileNotFoundError(
        'Required data folder not found.\n'
        'Delete the `data` folder in ~/skyblock to fix it automatically.'
    )

MINION_LOOT = {}
for category in [*walk(join_path('skyblock', 'data', 'minions'))][0][1]:
    for file_name in [*walk(join_path('skyblock', 'data',
                                      'minions', category))][0][2]:
        if not file_name.endswith('.json'):
            continue

        minion_name = file_name[:-5]

        with open(join_path('skyblock', 'data', 'minions',
                            category, file_name)) as file:
            MINION_LOOT[minion_name] = [
                (pointer, count) for pointer, count in load(file)
            ]
