from itertools import count
from os.path import join
from pathlib import Path
from random import random
from re import escape, fullmatch
from sys import stdout
from textwrap import wrap
from typing import Any, Dict, List, Optional, Union
from types import FunctionType

from .constant import (
    Number,
    SKILL_EXP, DUNGEON_EXP, EXP_LIMITS, ROMAN_NUM, NUMBER_SCALES, SPECIAL_NAMES,
)

__all__ = [
    'get', 'includes', 'is_dir', 'is_file',
    'roman', 'random_int',
    'display_name', 'display_money', 'shorten_money',
    'calc_exp', 'calc_skill_exp',
    'gen_help', 'backupable', 'input_regex',
    'black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white',
    'BLACK', 'RED', 'GREEN', 'YELLOW', 'BLUE', 'MAGENTA', 'CYAN', 'WHITE',
]


def get(ls: List[Any], name: str, *, default: Optional[Any] = None) -> Any:
    for item in ls:
        if item.name == name:
            return item.copy() if hasattr(item, 'copy') else item
    return default.copy() if hasattr(default, 'copy') else default


def includes(ls: List[Any], name: str) -> bool:
    for item in ls:
        if item.name == name:
            return True
    return False


def is_dir(*names, warn: bool = False):
    if not Path(join(Path.home(), 'skyblock', *names)).is_dir():
        path = join('~', 'skyblock', *names)
        if warn:
            yellow(f'Warning: folder {path} not found.')
        return False
    return True


def is_file(*names, warn: bool = False):
    if not Path(join(Path.home(), 'skyblock', *names)).is_file():
        path = join('~', 'skyblock', *names)
        if warn:
            yellow(f'Warning: file {path} not found.')
        return False
    return True


def roman(num: int, /) -> str:
    result = ''
    for letter, amount in reversed(ROMAN_NUM):
        while num >= amount:
            num -= amount
            result += letter
    return result


def random_int(num: float, /) -> int:
    int_part, float_part = divmod(num, 1)
    return int(int_part + (float_part > random()))


def display_name(name: str, /) -> str:
    if name in SPECIAL_NAMES:
        return SPECIAL_NAMES[name]
    else:
        return ' '.join(word.capitalize() for word in name.split('_'))


def display_money(money: Union[int, float], /) -> str:
    string = f'{money:.1f}'
    integer, floating = string.split('.')
    integer = ','.join(part[::-1] for part in wrap(integer[::-1], 3)[::-1])
    return f'{integer}.{floating}'


def shorten_money(money: Union[int, float], /) -> str:
    for letter, amount in reversed(NUMBER_SCALES):
        if money > amount:
            return f'{money / amount:.1f}{letter}'
    return f'{money / amount:.1f}'


def calc_exp(amount: Number, /) -> int:
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


def calc_skill_exp(name: str, amount: Number, /) -> int:
    exp_table = DUNGEON_EXP if name == 'catacombs' else SKILL_EXP
    for line in exp_table:
        lvl, _, cumulative = line[:3]
        if amount < cumulative:
            return lvl - 1
    else:
        return EXP_LIMITS[name]


# 5l*4% + 5l*5% + 5l*6% + 5l*7% + 5l*8% + 5l*9% +
# 5l*10% + 5l*12% + 5l*14% + 16% + 17% + 18% + 19% + 20%
def dung_stat(num: int, lvl: int, stars: int) -> Number:
    mult = 1 + 0.1 * stars
    for i in range(lvl):
        if i < 35:
            mult += 0.01 * (4 + (i // 5))
        elif i < 45:
            mult += 0.01 * (10 + 2 * ((i - 35) // 5))
        else:
            mult += 0.01 * ((i - 45) + 16)
    return num * mult


def gen_help(doc: str, /) -> Dict[str, str]:
    description = {}
    for para in doc.split('\n\n'):
        desc = para.split('\n')[-1]
        for _cmd in para.split('\n')[:-1]:
            description[' '.join(part for part in _cmd[2:].split()
                                 if not part.startswith(('[', '<')))] = desc
    return description


def backupable(func: FunctionType, /) -> FunctionType:
    def result(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyboardInterrupt:
            yellow('\nKeyboardInterruption')
    result.__name__ = func.__name__
    return result


def input_regex(prompt: str, /, pattern: str) -> str:
    while True:
        green(prompt)
        string = input(']> ')
        if fullmatch(pattern, string):
            return string
        red(f'Invalid input for regex pattern {escape(pattern)}')


def black(*args, sep=' ', end='\n') -> None:
    string = sep.join(f'{arg}' for arg in args)
    stdout.write(f'\x1b[0;90m{string}{end}\x1b[0m')


def red(*args, sep=' ', end='\n') -> None:
    string = sep.join(f'{arg}' for arg in args)
    stdout.write(f'\x1b[0;91m{string}{end}\x1b[0m')


def green(*args, sep=' ', end='\n') -> None:
    string = sep.join(f'{arg}' for arg in args)
    stdout.write(f'\x1b[0;92m{string}{end}\x1b[0m')


def yellow(*args, sep=' ', end='\n') -> None:
    string = sep.join(f'{arg}' for arg in args)
    stdout.write(f'\x1b[0;93m{string}{end}\x1b[0m')


def blue(*args, sep=' ', end='\n') -> None:
    string = sep.join(f'{arg}' for arg in args)
    stdout.write(f'\x1b[0;94m{string}{end}\x1b[0m')


def magenta(*args, sep=' ', end='\n') -> None:
    string = sep.join(f'{arg}' for arg in args)
    stdout.write(f'\x1b[0;95m{string}{end}\x1b[0m')


def cyan(*args, sep=' ', end='\n') -> None:
    string = sep.join(f'{arg}' for arg in args)
    stdout.write(f'\x1b[0;96m{string}{end}\x1b[0m')


def white(*args, sep=' ', end='\n') -> None:
    string = sep.join(f'{arg}' for arg in args)
    stdout.write(f'\x1b[0;97m{string}{end}\x1b[0m')
