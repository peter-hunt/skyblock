from re import escape, fullmatch
from sys import stdout

from ..constant.colors import GRAY, RED, GREEN, YELLOW, BLUE, AQUA, WHITE

__all__ = [
    'gray', 'red', 'green', 'yellow', 'blue', 'aqua', 'white',
    'input_regex',
]


def gray(*args, sep=' ', end='\n') -> None:
    string = sep.join(f'{arg}' for arg in args)
    stdout.write(f'{GRAY}{string}{end}\x1b[0m')


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
