"""
Collection of IO streaming functions for easier printing and getting input.

Contains printers with starting color of each name.

  gray('Hello World!')  # prints 'Hello World!' in gray

  # get input of word characters, will retry if not found
  string = input_regex('Please input a name: ', r'\w+')
"""

from re import compile as re_compile, error as re_error, escape
from sys import stdout

from ..constant.color import (
    DARK_GREEN, DARK_AQUA, GOLD, GRAY, DARK_GRAY,
    BLUE, GREEN, AQUA, RED, YELLOW, WHITE,
)


__all__ = [
    'dark_green', 'dark_aqua', 'gold', 'gray', 'dark_gray', 'blue',
    'green', 'aqua', 'red', 'yellow', 'white',
    'input_regex']


def dark_green(*args, sep=' ', end='\n'):
    """
    Print things in dark green.

    Almost the same as default `print`, but colored.
    """

    string = sep.join(f'{arg}' for arg in args)
    stdout.write(f'{DARK_GREEN}{string}{end}\x1b[0m')


def dark_aqua(*args, sep=' ', end='\n'):
    """
    Print things in dark aqua.

    Almost the same as default `print`, but colored.
    """

    string = sep.join(f'{arg}' for arg in args)
    stdout.write(f'{DARK_AQUA}{string}{end}\x1b[0m')


def gold(*args, sep=' ', end='\n'):
    """
    Print things in gold.

    Almost the same as default `print`, but colored.
    """

    string = sep.join(f'{arg}' for arg in args)
    stdout.write(f'{GOLD}{string}{end}\x1b[0m')


def gray(*args, sep=' ', end='\n'):
    """
    Print things in gray.

    Almost the same as default `print`, but colored.
    """

    string = sep.join(f'{arg}' for arg in args)
    stdout.write(f'{GRAY}{string}{end}\x1b[0m')


def dark_gray(*args, sep=' ', end='\n'):
    """
    Print things in dark gray.

    Almost the same as default `print`, but colored.
    """

    string = sep.join(f'{arg}' for arg in args)
    stdout.write(f'{DARK_GRAY}{string}{end}\x1b[0m')


def blue(*args, sep=' ', end='\n'):
    """
    Print things in blue.

    Almost the same as default `print`, but colored.
    """

    string = sep.join(f'{arg}' for arg in args)
    stdout.write(f'{BLUE}{string}{end}\x1b[0m')


def green(*args, sep=' ', end='\n'):
    """
    Print things in green.

    Almost the same as default `print`, but colored.
    """

    string = sep.join(f'{arg}' for arg in args)
    stdout.write(f'{GREEN}{string}{end}\x1b[0m')


def aqua(*args, sep=' ', end='\n'):
    """
    Print things in aqua.

    Almost the same as default `print`, but colored.
    """

    string = sep.join(f'{arg}' for arg in args)
    stdout.write(f'{AQUA}{string}{end}\x1b[0m')


def red(*args, sep=' ', end='\n'):
    """
    Print things in red.

    Almost the same as default `print`, but colored.
    """

    string = sep.join(f'{arg}' for arg in args)
    stdout.write(f'{RED}{string}{end}\x1b[0m')


def yellow(*args, sep=' ', end='\n'):
    """
    Print things in yellow.

    Almost the same as default `print`, but colored.
    """

    string = sep.join(f'{arg}' for arg in args)
    stdout.write(f'{YELLOW}{string}{end}\x1b[0m')


def white(*args, sep=' ', end='\n'):
    """
    Print things in white.

    Almost the same as default `print`, but colored.
    """

    string = sep.join(f'{arg}' for arg in args)
    stdout.write(f'{WHITE}{string}{end}\x1b[0m')


def input_regex(prompt: str, /, pattern: str) -> str:
    """
    Recieve input matching the given pattern.

    Args:
        prompt: Instructions for the user printed without a new line.
        pattern: A string of regex pattern to be matched by the input string.

    Returns:
        A string matching the pattern input by the user.

    Raises:
        ValueError: invalid pattern: (re.error)
    """

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
