from os import walk
from os.path import join
from pathlib import Path

from ._lib import add_history
from .constant.colors import *
from .constant.doc import menu_doc
from .function.io import *
from .function.util import checkpoint, clear, generate_help, is_valid_usage
from .path import is_dir, is_profile
from .profile.object import Profile


__all__ = ['main']

menu_help = generate_help(menu_doc)


@checkpoint
def new():
    name = input_regex('Please enter the name of the profile.', r'\w+')
    Profile(name).dump()
    green('New profile created!')


def get_profiles() -> list[str]:
    if not is_dir() or not is_dir('saves'):
        red('path not found: ~/skyblock/saves.')
        return []
    names = [*walk(join(Path.home(), 'skyblock', 'saves'))][0][2]
    return [name[:-5] for name in names if name.endswith('.json')]


@checkpoint
def ls():
    names = get_profiles()
    if len(names) == 0:
        yellow('No profiles to be displayed.')
    else:
        gray('Avaliable profiles:')
        for name in names:
            if is_profile(name):
                aqua(f' {name}')
            else:
                yellow(f' {name}')


@checkpoint
def main():
    clear()
    yellow(f'Welcome to {GREEN}Skyblock{YELLOW}!')

    if is_dir() and is_dir('saves'):
        names = get_profiles()
        if len(names) != 0:
            lastest, lastest_profile = 0, None
            for name in names:
                profile = Profile.load(name)
                if profile.last_update > lastest:
                    lastest = profile.last_update
                    lastest_profile = profile

            if lastest_profile is not None:
                lastest_profile.mainloop()
    else:
        red('folder not found: ~/skyblock/saves.')

    while True:
        original_input = input('> ')
        words = original_input.split()

        if len(words) == 0:
            continue

        add_history(original_input)

        phrase = words[0]
        if len(words) >= 2:
            phrase = ' '.join(words[:2])
            if phrase not in menu_help:
                phrase = words[0]

        if phrase not in menu_help:
            red(f'Command not found: {phrase!r}.')
            continue
        if not is_valid_usage(menu_help[phrase][0], words):
            red(f'Invalid usage of command: {words[0]}.')
            continue

        if words[0] == 'clear':
            clear()

        elif words[0] in {'delete', 'remove'}:
            path = Path(join(Path.home(), 'skyblock',
                             'saves', f'{words[1]}.json'))
            if path.is_file():
                path.unlink()
                green(f'Deleted profile {AQUA}{words[1]}{GREEN}!')
            else:
                red(f'Profile not found: {words[1]!r}.')

        elif words[0] in {'exit', 'quit'}:
            break

        elif words[0] == 'help':
            if len(words) == 1:
                gray(f'\n{menu_doc}\n')
                continue

            phrase = ' '.join(words[1:])
            help_found = []
            for key, pair in menu_help.items():
                if key.startswith(phrase):
                    usage, description = pair
                    help_found.append(f'{usage}\n{description}')
            if len(help_found) != 0:
                gray('\n' + '\n\n'.join(help_found) + '\n')
            else:
                red(f'Command not found: {phrase!r}.')

        elif words[0] == 'ls':
            ls()

        elif words[0] in {'load', 'open'}:
            profile = Profile.load(words[1])
            if profile is not None:
                profile.mainloop()

        elif words[0] in {'new', 'touch'}:
            new()

        else:
            red(f'Unknown command: {words[0]!r}')
