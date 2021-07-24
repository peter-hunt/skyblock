from os.path import join
from pathlib import Path


__all__ = ['is_data', 'is_dir', 'is_file', 'is_profile', 'join_path']


def is_dir(*names):
    return Path(join(Path.home(), 'skyblock', *names)).is_dir()


def is_file(*names):
    return Path(join(Path.home(), 'skyblock', *names)).is_file()


def is_data():
    if not is_dir() or not is_dir('data'):
        return False

    for category in {'collections', 'fishing', 'items', 'minions', 'mobs',
                     'recipes', 'resources', 'templates'}:
        if not is_dir('data', category):
            return False

    return True


def is_profile(name: str, /):
    if not is_dir() or not is_dir('saves'):
        return False
    else:
        return is_file('saves', f'{name}.json')


def join_path(*names) -> str:
    return join(Path.home(), *names)
