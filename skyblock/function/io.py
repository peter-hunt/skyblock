from re import escape, fullmatch
from sys import stdout

from ..constant.color import (
    DARK_AQUA, GOLD, GRAY, DARK_GRAY, RED, GREEN, YELLOW, BLUE, AQUA, WHITE,
)

__all__ = [
    'dark_aqua', 'gold',
    'gray', 'dark_gray', 'red', 'green', 'yellow', 'blue', 'aqua', 'white',
    'input_regex',
]


def dark_aqua(*args, sep=' ', end='\n') -> None:
    string = sep.join(f'{arg}' for arg in args)
    stdout.write(f'{DARK_AQUA}{string}{end}\x1b[0m')


def gold(*args, sep=' ', end='\n') -> None:
    string = sep.join(f'{arg}' for arg in args)
    stdout.write(f'{GOLD}{string}{end}\x1b[0m')


def gray(*args, sep=' ', end='\n') -> None:
    string = sep.join(f'{arg}' for arg in args)
    stdout.write(f'{GRAY}{string}{end}\x1b[0m')


def dark_gray(*args, sep=' ', end='\n') -> None:
    string = sep.join(f'{arg}' for arg in args)
    stdout.write(f'{DARK_GRAY}{string}{end}\x1b[0m')


def red(*args, sep=' ', end='\n') -> None:
    string = sep.join(f'{arg}' for arg in args)
    stdout.write(f'{RED}{string}{end}\x1b[0m')


def green(*args, sep=' ', end='\n') -> None:
    string = sep.join(f'{arg}' for arg in args)
    stdout.write(f'{GREEN}{string}{end}\x1b[0m')


def yellow(*args, sep=' ', end='\n') -> None:
    string = sep.join(f'{arg}' for arg in args)
    stdout.write(f'{YELLOW}{string}{end}\x1b[0m')


def blue(*args, sep=' ', end='\n') -> None:
    string = sep.join(f'{arg}' for arg in args)
    stdout.write(f'{BLUE}{string}{end}\x1b[0m')


def aqua(*args, sep=' ', end='\n') -> None:
    string = sep.join(f'{arg}' for arg in args)
    stdout.write(f'{AQUA}{string}{end}\x1b[0m')


def white(*args, sep=' ', end='\n') -> None:
    string = sep.join(f'{arg}' for arg in args)
    stdout.write(f'{WHITE}{string}{end}\x1b[0m')


def input_regex(prompt: str, /, pattern: str) -> str:
    while True:
        green(prompt)
        string = input(']> ')
        if fullmatch(pattern, string):
            return string
        red(f'Invalid input for regex pattern {escape(pattern)}')
