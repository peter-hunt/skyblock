from itertools import count
from os.path import join
from pathlib import Path
from random import random
from re import escape, fullmatch
from sys import stdout
from textwrap import wrap
from typing import Any, Dict, List, Union
from types import FunctionType

from .const import SKILL_EXP, DUNGEON_EXP, EXP_LIMITS, ROMAN_NUM, NUMBER_SCALES

__all__ = [
    'Number', 'get', 'exist_dir', 'exist_file', 'roman', 'random_int',
    'display_money', 'shorten_money', 'calc_exp', 'calc_skill_exp',
    'gen_help', 'backupable', 'input_regex',
    'black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white',
    'BLACK', 'RED', 'GREEN', 'YELLOW', 'BLUE', 'MAGENTA', 'CYAN', 'WHITE',
]


Number = Union[float, int]


def get(ls: List[Any], name: str, default=None) -> Any:
    for item in ls:
        if item.name == name:
            return item
    return default


def exist_dir(*names, warn=False):
    if not Path(join(Path.home(), 'skyblock', *names)).is_dir():
        path = join('~', 'skyblock', *names)
        if warn:
            print(f'Warning: folder {path} not found.')
        return False
    return True


def exist_file(*names, warn=False):
    if not Path(join(Path.home(), 'skyblock', *names)).is_file():
        path = join('~', 'skyblock', *names)
        if warn:
            print(f'Warning: file {path} not found.')
        return False
    return True


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


def display_money(money: Union[int, float]) -> str:
    string = f'{money:.1f}'
    integer, floating = string.split('.')
    integer = ','.join(part[::-1] for part in wrap(integer[::-1], 3)[::-1])
    return f'{integer}.{floating}'


def shorten_money(money: Union[int, float]) -> str:
    for letter, amount in reversed(NUMBER_SCALES):
        if money > amount:
            return f'{money / amount:.1f}{letter}'
    return f'{money / amount:.1f}'


def calc_exp(amount):
    if amount <= 352:
        for lvl in range(17):
            if (lvl + 1) ** 2 + 6 * (lvl + 1) > amount:
                return lvl

    elif amount <= 1507:
        for lvl in range(17, 32):
            if 2.5 ** (lvl + 1) ** 2 - 40.5 * (lvl + 1) + 360 > amount:
                return lvl

    else:
        for lvl in count(32):
            if 4.5 ** (lvl + 1) ** 2 - 162.5 * (lvl + 1) + 2220 > amount:
                return lvl


def calc_skill_exp(name, amount):
    exp_table = DUNGEON_EXP if name == 'dungeoneering' else SKILL_EXP
    for lvl, _, cumulative, _ in exp_table:
        if amount < cumulative:
            return lvl - 1
    else:
        return EXP_LIMITS[name]


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


BLACK = '\x1b[0;90m'
RED = '\x1b[0;91m'
GREEN = '\x1b[0;92m'
YELLOW = '\x1b[0;93m'
BLUE = '\x1b[0;94m'
MAGENTA = '\x1b[0;95m'
CYAN = '\x1b[0;96m'
WHITE = '\x1b[0;97m'
