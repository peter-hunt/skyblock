from typing import Dict, List, Tuple
from json import load
from os import walk

from ..constant.util import Number, ItemPointer
from ..function.path import join_path


__all__ = ['MINION_LOOT']

MINION_LOOT: Dict[str, List[Tuple[ItemPointer, Number]]] = {}
for category in [*walk(join_path('skyblock', 'data', 'minion'))][0][1]:
    for file_name in [*walk(join_path('skyblock', 'data',
                                      'minion', category))][0][2]:
        if not file_name.endswith('.json'):
            continue

        minion_name = file_name[:-5]

        with open(join_path('skyblock', 'data', 'minion',
                            category, file_name)) as file:
            MINION_LOOT[minion_name] = [
                (pointer, count) for pointer, count in load(file)
            ]


# print(MINION_LOOT)
# exit()
