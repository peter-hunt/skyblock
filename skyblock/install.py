from os import mkdir
from os.path import join
from pathlib import Path
from subprocess import run


def install():
    data_dir = join(Path.home(), 'skyblock', 'data')
    if not Path(data_dir).is_dir():
        print('\x1b[0;38;2;85;255;85mInstalling Assets...\x1b[0m')
        mkdir(data_dir)
        run(['git', 'clone', 'https://github.com/peter-hunt/skyblock-data',
             data_dir])
        print('\x1b[0;38;2;85;255;85mAssets Installed!\x1b[0m')
