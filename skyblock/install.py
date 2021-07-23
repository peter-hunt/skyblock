from os import mkdir
from os.path import join
from pathlib import Path
from subprocess import run


__all__ = ['install']


def install(*, is_update=False):
    data_dir = join(Path.home(), 'skyblock', 'data')
    doing_str = 'Updating' if is_update else 'Installing'
    done_str = 'Updated' if is_update else 'Installed'
    if is_update or not Path(data_dir).is_dir():
        if is_update:
            run(['rm', '-rf', data_dir])
        mkdir(data_dir)
        print(f'\x1b[0;38;2;85;255;85m{doing_str} Assets...\x1b[0m')
        run(['git', 'clone', 'https://github.com/peter-hunt/skyblock-data',
             data_dir])
        print(f'\x1b[0;38;2;85;255;85mAssets {done_str}!\x1b[0m')
