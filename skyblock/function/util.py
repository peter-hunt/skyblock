from random import randint, random
from textwrap import wrap
from typing import Any, Dict, List, Optional, Union
from types import FunctionType

from ..constant.main import SPECIAL_NAMES
from ..constant.util import NUMBER_SCALES, ROMAN_NUM, Amount

from .io import yellow

__all__ = [
    'backupable', 'display_money', 'display_name', 'display_number', 'get',
    'generate_help', 'includes', 'random_amount', 'random_bool', 'roman',
    'shorten_money',
]


def backupable(func: FunctionType, /) -> FunctionType:
    def result(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyboardInterrupt:
            yellow('\nKeyboardInterruption')
    result.__name__ = func.__name__
    return result


def display_money(money: Union[int, float], /) -> str:
    string = f'{money:.1f}'
    integer, floating = string.split('.')
    integer = ','.join(part[::-1] for part in wrap(integer[::-1], 3)[::-1])
    return f'{integer}.{floating}'


def display_name(name: str, /) -> str:
    if name in SPECIAL_NAMES:
        return SPECIAL_NAMES[name]
    else:
        return ' '.join(word.capitalize() for word in name.split('_'))


def display_number(number: int, /) -> str:
    string = f'{number}'
    string = ','.join(part[::-1] for part in wrap(string[::-1], 3)[::-1])
    return string


def generate_help(doc: str, /) -> Dict[str, str]:
    description = {}
    for para in doc.split('\n\n'):
        desc = para.split('\n')[-1]
        for _cmd in para.split('\n')[:-1]:
            description[' '.join(part for part in _cmd[2:].split()
                                 if not part.startswith(('[', '<')))] = desc
    return description


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


def random_amount(amount: Amount = 1, /) -> int:
    if isinstance(amount, int):
        return amount
    else:
        return randint(amount[0], amount[1])


def random_bool(chance: float = 0.5, /) -> bool:
    return random() < chance


def roman(num: int, /) -> str:
    result = ''
    for letter, amount in reversed(ROMAN_NUM):
        while num >= amount:
            num -= amount
            result += letter
    return result


def shorten_money(money: Union[int, float], /) -> str:
    for letter, amount in reversed(NUMBER_SCALES):
        if money > amount:
            return f'{money / amount:.1f}{letter}'
    return f'{money / amount:.1f}'
