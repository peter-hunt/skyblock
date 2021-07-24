from os import walk
from pathlib import Path
from typing import Optional

from ..function.io import *
from ..path import join_path


__all__ = ['TEMPLATES', 'get_template']

if not Path(join_path('skyblock', 'data', 'templates')).is_dir():
    raise FileNotFoundError(
        'Required data not found.\n'
        'Restart skyblock to fix it automatically.'
    )

TEMPLATES = {}
for category in [*walk(join_path('skyblock', 'data', 'templates'))][0][1]:
    for file_name in sorted([*walk(join_path('skyblock', 'data',
                                             'templates', category))][0][2]):
        if not file_name.endswith('.txt'):
            continue

        with open(join_path('skyblock', 'data', 'templates',
                            category, file_name)) as file:
            TEMPLATES[file_name[:-4]] = file.read()


def get_template(name: str) -> Optional[str]:
    if name in TEMPLATES:
        return TEMPLATES[name]
    else:
        red(f'Template not found: {name!r}')
