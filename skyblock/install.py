from os import mkdir
from os.path import join
from pathlib import Path
from subprocess import run
from sys import platform

from .path import is_data, join_path


__all__ = ['init']


def init_home_dir(*names):
    if not Path(join_path(*names)).is_dir():
        Path(join_path(*names)).mkdir()


def install_data(*, is_update=False):
    data_dir = join(Path.home(), 'skyblock', 'data')
    if is_update:
        doing_str, done_str = 'Updating', 'Updated'
    elif not is_data():
        doing_str, done_str = 'Installing', 'Installed'
    else:
        doing_str, done_str = 'Fixing', 'Fixed'
    if is_update or not is_data():
        if Path(data_dir).is_dir():
            if platform == 'win32':
                run(['rm', data_dir, '-Recurse', '-Force'])
            else:
                run(['rm', '-rf', data_dir])
        mkdir(data_dir)
        print(f'\x1b[0;38;2;85;255;85m{doing_str} Assets...\x1b[0m')
        run(['git', 'clone', '-q',
             'https://github.com/peter-hunt/skyblock-data', data_dir])
        print(f'\x1b[0;38;2;85;255;85mAssets {done_str}!\x1b[0m')


def init():
    init_home_dir('skyblock')
    init_home_dir('skyblock', 'saves')
    install_data()
