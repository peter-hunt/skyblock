from os import walk
from os.path import join
from pathlib import Path

from .constant.color import GREEN, AQUA
from .constant.doc import menu_doc
from .function.io import gray, red, green, yellow, aqua, input_regex
from .function.path import is_dir, is_profile
from .function.util import backupable, generate_help
from .profile.object import Profile

__all__ = ['main']


menu_help = generate_help(menu_doc)


def init_home_dir(*names):
    if not Path(join(Path.home(), *names)).is_dir():
        Path(join(Path.home(), *names)).mkdir()


def init_env():
    init_home_dir('skyblock')
    init_home_dir('skyblock', 'saves')


@backupable
def new():
    name = input_regex('Please enter the name of the profile.', r'\w+')
    Profile(name).dump()
    green('New profile created!')


@backupable
def ls():
    if not is_dir(warn=True):
        return
    if not is_dir('saves', warn=True):
        return
    names = [*walk(join(Path.home(), 'skyblock', 'saves'))][0][2]
    names = [name[:-5] for name in names if name.endswith('.json')]
    if len(names) == 0:
        yellow('No profiles to be displayed.')
    else:
        gray('Avaliable profiles:')
        for name in names:
            if is_profile(name):
                aqua(f' {name}')
            else:
                yellow(f' {name}')


@backupable
def main():
    init_env()

    while True:
        words = input('> ').split()

        if len(words) == 0:
            continue

        elif words[0] in {'new', 'touch'}:
            if len(words) != 1:
                red(f'Invalid usage of command {words[0]}.')
                continue

            new()

        elif words[0] in {'del', 'delete'}:
            if len(words) != 2:
                red(f'Invalid usage of command {words[0]}.')
                continue

            path = Path(join(Path.home(), 'skyblock',
                             'saves', f'{words[1]}.json'))
            if path.is_file():
                path.unlink()
                green(f'Deleted profile {AQUA}{words[1]}{GREEN}!')
            else:
                red(f'Profile not found: {words[1]}')

        elif words[0] in {'exit', 'quit'}:
            if len(words) != 1:
                red(f'Invalid usage of command {words[0]}.')
                continue

            break

        elif words[0] == 'help':
            if len(words) == 1:
                gray(menu_doc)
            else:
                phrase = ' '.join(words[1:])
                if phrase not in menu_help:
                    red(f'Command not found: {phrase!r}.')
                    continue

                usage, description = menu_help[phrase]
                gray(usage)
                gray(description)

        elif words[0] in {'list', 'ls'}:
            if len(words) != 1:
                red(f'Invalid usage of command {words[0]}.')
                continue

            ls()

        elif words[0] in {'load', 'open'}:
            if len(words) != 2:
                red(f'Invalid usage of command {words[0]}.')
                continue

            game = Profile.load(words[1])
            if game is None:
                continue

            game.mainloop()

        else:
            red(f'Unknown command: {words[0]!r}')
