from re import escape, fullmatch
from sys import stdout

from ..constant import F_GRAY, F_RED, F_GREEN, F_YELLOW, F_BLUE, F_AQUA, F_WHITE

__all__ = [
    'gray', 'red', 'green', 'yellow', 'blue', 'aqua', 'white',
    'input_regex',
]


def gray(*args, sep=' ', end='\n') -> None:
    string = sep.join(f'{arg}' for arg in args)
    stdout.write(f'{F_GRAY}{string}{end}\x1b[0m')


def red(*args, sep=' ', end='\n') -> None:
    string = sep.join(f'{arg}' for arg in args)
    stdout.write(f'{F_RED}{string}{end}\x1b[0m')


def green(*args, sep=' ', end='\n') -> None:
    string = sep.join(f'{arg}' for arg in args)
    stdout.write(f'{F_GREEN}{string}{end}\x1b[0m')


def yellow(*args, sep=' ', end='\n') -> None:
    string = sep.join(f'{arg}' for arg in args)
    stdout.write(f'{F_YELLOW}{string}{end}\x1b[0m')


def blue(*args, sep=' ', end='\n') -> None:
    string = sep.join(f'{arg}' for arg in args)
    stdout.write(f'{F_BLUE}{string}{end}\x1b[0m')


def aqua(*args, sep=' ', end='\n') -> None:
    string = sep.join(f'{arg}' for arg in args)
    stdout.write(f'{F_AQUA}{string}{end}\x1b[0m')


def white(*args, sep=' ', end='\n') -> None:
    string = sep.join(f'{arg}' for arg in args)
    stdout.write(f'{F_WHITE}{string}{end}\x1b[0m')


def input_regex(prompt: str, /, pattern: str) -> str:
    while True:
        green(prompt)
        string = input(']> ')
        if fullmatch(pattern, string):
            return string
        red(f'Invalid input for regex pattern {escape(pattern)}')
