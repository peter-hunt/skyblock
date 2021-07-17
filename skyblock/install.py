from os import mkdir
from pathlib import Path
from subprocess import run

from .function.io import *
from .function.path import join_path


def install():
    if not Path(join_path('skyblock', 'data')).is_dir():
        green('Installing Assets...')
        mkdir(join_path('skyblock', 'data'))
        run(['git', 'clone',
             'https://github.com/peter-hunt/skyblock-data',
            join_path('skyblock', 'data'), '--quiet'])
        green('Assets Installed!')
