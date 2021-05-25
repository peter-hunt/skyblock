from os import walk
from os.path import join
from pathlib import Path

from .func import gen_help, backupable, input_regex, red, green, cyan
from .profile import Profile


menu_doc = """
> help [command]
Show this message or get command description.

> exit
> quit
Exit the menu.

> create
> new
Create a new profile.

> list
> ls
List all the profile avaliable.

> delete <name>
Delete a profile.

> load <name>
> open <name>
> start <name>
Load a profile and run it.
""".strip()
menu_help = gen_help(menu_doc)


def init_home_dir(*names):
    if not Path(join(Path.home(), *names)).is_dir():
        Path(join(Path.home(), *names)).mkdir()


def init_env():
    init_home_dir('skyblock')
    init_home_dir('skyblock', 'saves')


@backupable
def create():
    name = input_regex('Please enter the name of the profile.', r'\w+')


@backupable
def ls():
    path = join(Path.home(), 'skyblock')
    if not Path(path).is_dir():
        print('Directory not found: {path}')
    path = join(Path.home(), 'skyblock', 'saves')
    if not Path(path).is_dir():
        print('Directory not found: {path}')
    names = [*walk(join(Path.home(), 'skyblock', 'saves'))][0][2]
    names = [name[:-5] for name in names if name.endswith('.json')]
    if len(names) == 0:
        print('No profiles to be displayed.')
    else:
        print('Avaliable profiles:')
        for name in names:
            if Profile.is_valid(name):
                cyan(f' {name}')
            else:
                red(f' {name}')


@backupable
def main():
    print('Checking environment...')
    init_env()

    while True:
        words = input('> ').split()

        if len(words) == 0:
            continue

        elif words[0] in {'exit', 'quit'}:
            if len(words) == 1:
                break
            else:
                red(f'Invalid usage of command {words[0]!r}.')

        elif words[0] == 'help':
            if len(words) == 1:
                print(menu_doc)
            else:
                phrase = ' '.join(words[1:])
                if phrase in menu_help:
                    print(f'> {phrase}')
                    print(menu_help[phrase])
                else:
                    red(f'Command not found: {phrase!r}.')

        elif words[0] in {'create', 'new'}:
            if len(words) == 1:
                create()
            else:
                red(f'Invalid usage of command {words[0]!r}.')

        elif words[0] == 'delete':
            if len(words) == 2:
                path = Path(join(Path.home(), 'saves', f'{words[1]}.json'))
                if path.is_file():
                    path.unlink()
                    green(f'Deleted profile {words[1]}!')
                else:
                    red(f'Profile not found: {words[1]}')
            else:
                red(f'Invalid usage of command {words[0]!r}.')

        elif words[0] in {'list', 'ls'}:
            if len(words) == 1:
                ls()
            else:
                red(f'Invalid usage of command {words[0]!r}.')

        elif words[0] in {'load', 'open', 'start'}:
            if len(words) == 2:
                game = Profile.load(words[1])
                if game is None:
                    continue
                game.mainloop()
            else:
                red(f'Invalid usage of command {words[0]!r}.')

        else:
            red(f'Unknown command: {words[0]!r}')
