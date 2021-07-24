from os import mkdir
from os.path import join
from pathlib import Path
from subprocess import run

from .path import is_data


__all__ = ['install']


def install(*, force=False, is_update=False):
    data_dir = join(Path.home(), 'skyblock', 'data')
    if is_update:
        doing_str, done_str = 'Updating', 'Updated'
    elif is_data():
        doing_str, done_str = 'Installing', 'Installed'
    else:
        doing_str, done_str = 'Fixing', 'Fixed'
    if is_update or force or not is_data():
        if Path(data_dir).is_dir():
            run(['rm', '-rf', data_dir])
        mkdir(data_dir)
        print(f'\x1b[0;38;2;85;255;85m{doing_str} Assets...\x1b[0m')
        run(['git', 'clone', '-q',
             'https://github.com/peter-hunt/skyblock-data', data_dir])
        print(f'\x1b[0;38;2;85;255;85mAssets {done_str}!\x1b[0m')
