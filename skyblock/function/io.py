from re import compile as re_compile, error as re_error, escape
from sys import stdout

from ..constant.colors import *


__all__ = [
    'black', 'dark_blue', 'dark_green', 'dark_aqua', 'dark_red', 'dark_purple',
    'gold', 'gray', 'dark_gray', 'blue', 'green', 'aqua', 'red', 'light_purple',
    'yellow', 'white',
    'input_regex',
]


def black(*args, sep=' ', end='\n'):
    string = sep.join(f'{arg}' for arg in args)
    stdout.write(f'{BLACK}{string}{end}\x1b[0m')


def dark_blue(*args, sep=' ', end='\n'):
    string = sep.join(f'{arg}' for arg in args)
    stdout.write(f'{DARK_BLUE}{string}{end}\x1b[0m')


def dark_green(*args, sep=' ', end='\n'):
    string = sep.join(f'{arg}' for arg in args)
    stdout.write(f'{DARK_GREEN}{string}{end}\x1b[0m')


def dark_aqua(*args, sep=' ', end='\n'):
    string = sep.join(f'{arg}' for arg in args)
    stdout.write(f'{DARK_AQUA}{string}{end}\x1b[0m')


def dark_red(*args, sep=' ', end='\n'):
    string = sep.join(f'{arg}' for arg in args)
    stdout.write(f'{DARK_RED}{string}{end}\x1b[0m')


def dark_purple(*args, sep=' ', end='\n'):
    string = sep.join(f'{arg}' for arg in args)
    stdout.write(f'{DARK_RED}{string}{end}\x1b[0m')


def gold(*args, sep=' ', end='\n'):
    string = sep.join(f'{arg}' for arg in args)
    stdout.write(f'{GOLD}{string}{end}\x1b[0m')


def gray(*args, sep=' ', end='\n'):
    string = sep.join(f'{arg}' for arg in args)
    stdout.write(f'{GRAY}{string}{end}\x1b[0m')


def dark_gray(*args, sep=' ', end='\n'):
    string = sep.join(f'{arg}' for arg in args)
    stdout.write(f'{DARK_GRAY}{string}{end}\x1b[0m')


def blue(*args, sep=' ', end='\n'):
    string = sep.join(f'{arg}' for arg in args)
    stdout.write(f'{BLUE}{string}{end}\x1b[0m')


def green(*args, sep=' ', end='\n'):
    string = sep.join(f'{arg}' for arg in args)
    stdout.write(f'{GREEN}{string}{end}\x1b[0m')


def aqua(*args, sep=' ', end='\n'):
    string = sep.join(f'{arg}' for arg in args)
    stdout.write(f'{AQUA}{string}{end}\x1b[0m')


def red(*args, sep=' ', end='\n'):
    string = sep.join(f'{arg}' for arg in args)
    stdout.write(f'{RED}{string}{end}\x1b[0m')


def light_purple(*args, sep=' ', end='\n'):
    string = sep.join(f'{arg}' for arg in args)
    stdout.write(f'{LIGHT_PURPLE}{string}{end}\x1b[0m')


def yellow(*args, sep=' ', end='\n'):
    string = sep.join(f'{arg}' for arg in args)
    stdout.write(f'{YELLOW}{string}{end}\x1b[0m')


def white(*args, sep=' ', end='\n'):
    string = sep.join(f'{arg}' for arg in args)
    stdout.write(f'{WHITE}{string}{end}\x1b[0m')


def input_regex(prompt: str, /, pattern: str) -> str:
    try:
        re_pattern = re_compile(pattern)
    except re_error as err:
        raise ValueError(f'invalid pattern: {err}')

    while True:
        green(prompt)
        string = input(']> ')
        if re_pattern.fullmatch(string):
            return string
        red(f'Invalid input for regex pattern {escape(pattern)}')
