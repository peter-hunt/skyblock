from random import random
from re import escape, fullmatch
from sys import stdout
from typing import Any, Dict, List
from types import FunctionType

ROMAN_NUM = [
    ('I', 1), ('IV', 4), ('V', 5), ('IX', 9), ('X', 10),
    ('XL', 40), ('L', 50), ('XC', 90), ('C', 100),
    ('CD', 400), ('D', 500), ('CM', 900), ('M', 1000),
]


def get(ls: List[Any], name: str, default=None) -> Any:
    for item in ls:
        if item.name == name:
            return item
    return default


def roman(num: int) -> str:
    result = ''
    for letter, amount in reversed(ROMAN_NUM):
        while num >= amount:
            num -= amount
            result += letter
    return result


def random_int(num: float) -> int:
    int_part, float_part = divmod(num, 1)
    return int(int_part + (float_part > random()))


def gen_help(doc: str) -> Dict[str, str]:
    description = {}
    for para in doc.split('\n\n'):
        desc = para.split('\n')[-1]
        for _cmd in para.split('\n')[:-1]:
            description[' '.join(part for part in _cmd[2:].split()
                                 if not part.startswith(('[', '<')))] = desc
    return description


def backupable(func: FunctionType) -> FunctionType:
    def result(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyboardInterrupt:
            yellow('\nKeyboardInterruption')
    result.__name__ = func.__name__
    return result


def input_regex(prompt: str, pattern: str) -> str:
    while True:
        print(prompt)
        string = input(']> ')
        if fullmatch(pattern, string):
            return string
        red(f'Invalid input for regex pattern {escape(pattern)}')


def black(*args, sep=' ', end='\n'):
    string = sep.join(f'{arg}' for arg in args)
    stdout.write(f'\x1b[90m{string}{end}\x1b[0m')


def red(*args, sep=' ', end='\n'):
    string = sep.join(f'{arg}' for arg in args)
    stdout.write(f'\x1b[91m{string}{end}\x1b[0m')


def green(*args, sep=' ', end='\n'):
    string = sep.join(f'{arg}' for arg in args)
    stdout.write(f'\x1b[92m{string}{end}\x1b[0m')


def yellow(*args, sep=' ', end='\n'):
    string = sep.join(f'{arg}' for arg in args)
    stdout.write(f'\x1b[93m{string}{end}\x1b[0m')


def blue(*args, sep=' ', end='\n'):
    string = sep.join(f'{arg}' for arg in args)
    stdout.write(f'\x1b[94m{string}{end}\x1b[0m')


def magenta(*args, sep=' ', end='\n'):
    string = sep.join(f'{arg}' for arg in args)
    stdout.write(f'\x1b[95m{string}{end}\x1b[0m')


def cyan(*args, sep=' ', end='\n'):
    string = sep.join(f'{arg}' for arg in args)
    stdout.write(f'\x1b[96m{string}{end}\x1b[0m')


def white(*args, sep=' ', end='\n'):
    string = sep.join(f'{arg}' for arg in args)
    stdout.write(f'\x1b[97m{string}{end}\x1b[0m')
