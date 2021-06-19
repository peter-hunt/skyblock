from re import fullmatch
from textwrap import wrap
from typing import Any, Dict, List, Optional, Tuple, Union
from types import FunctionType

from ..constant.enchanting import ENCHS
from ..constant.util import (
    NUMBER_SCALES, ROMAN_NUM, SPECIAL_NAMES, IGNORED_WORDS,
)

from .io import red, yellow

__all__ = [
    'backupable', 'display_int', 'display_name', 'display_number', 'get',
    'generate_help', 'includes', 'index', 'roman', 'shorten_number',
]


def backupable(func: FunctionType, /) -> FunctionType:
    def result(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyboardInterrupt:
            yellow('\nKeyboardInterruption')
    result.__name__ = func.__name__
    return result


def display_int(number: Union[int, float], /) -> str:
    if number % 1 == 0:
        string = f'{number:.0f}'
        string = ','.join(part[::-1] for part in wrap(string[::-1], 3)[::-1])
        return string
    else:
        return display_number(number)


def display_number(number: Union[int, float], /) -> str:
    string = f'{number:.1f}'
    integer, floating = string.split('.')
    integer = ','.join(part[::-1] for part in wrap(integer[::-1], 3)[::-1])
    return f'{integer}.{floating}'


def display_name(name: str, /) -> str:
    if name in SPECIAL_NAMES:
        return SPECIAL_NAMES[name]
    else:
        return ' '.join(_display_word(word) for word in name.split('_'))


def _display_word(word: str, /) -> str:
    return word.lower() if word in IGNORED_WORDS else word.capitalize()


def generate_help(doc: str, /) -> Dict[str, str]:
    description = {}
    for para in doc.split('\n\n'):
        desc = para.split('\n')[-1]
        for _cmd in para.split('\n')[:-1]:
            description[
                ' '.join(part for part in _cmd[2:].split()
                         if not part.startswith(('[', '<')))
            ] = (_cmd, desc)
    return description


def get(ls: List[Any], /, name: Optional[str] = None,
        default: Optional[Any] = None, **kwargs) -> Any:
    attrs = {}

    for item in ls:
        if name is not None and item.name != name:
            continue
        for kwarg in kwargs:
            if kwarg in {'enchantments', 'hot_potato'}:
                attrs[kwarg] = kwargs[kwarg]
                continue
            if getattr(item, kwarg, None) != kwargs[kwarg]:
                break
        else:
            result = item.copy() if hasattr(item, 'copy') else item
            for attr, value in attrs.items():
                setattr(result, attr, value)
            return result

    return default.copy() if hasattr(default, 'copy') else default


def get_ench(name: str, /) -> Tuple[str, Tuple[int]]:
    for row in ENCHS:
        if row[0] == name:
            if isinstance(row[2], tuple):
                return row[2]
            exp_lvls = tuple(lvl * row[2] + row[3]
                             for lvl in range(1, row[1] + 1))
            return exp_lvls
    else:
        red(f'Enchantment not fonud: {name!r}')


def includes(ls: List[Any], name: str, /) -> bool:
    for item in ls:
        if item.name == name:
            return True
    return False


def index(ls: List[Any], name: str, /) -> bool:
    for i, item in enumerate(ls):
        if item.name == name:
            return i
    raise ValueError(f'{name!r} is not in list')


def parse_int(string: str, /) -> Optional[int]:
    if fullmatch(r'\d+', string):
        return int(string)
    else:
        red('Please input a valid number!')
        return


def roman(num: int, /) -> str:
    result = ''
    for letter, amount in reversed(ROMAN_NUM):
        while num >= amount:
            num -= amount
            result += letter
    return result


def shorten_number(number: Union[int, float], /) -> str:
    for letter, amount in reversed(NUMBER_SCALES):
        if number >= amount:
            break
    else:
        amount = 1
        letter = ''

    string = f'{number / amount:.1f}'
    if string.endswith('.0'):
        string = string[:-2]
    return f'{string}{letter}'
