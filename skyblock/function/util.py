from random import randint, random
from textwrap import wrap
from typing import Any, Dict, List, Optional, Union
from types import FunctionType

from ..constant.main import SPECIAL_NAMES
from ..constant.util import NUMBER_SCALES, ROMAN_NUM, Amount

from .io import yellow

__all__ = [
    'backupable', 'display_int', 'display_name', 'display_number', 'get',
    'generate_help', 'includes', 'random_amount', 'random_bool', 'roman',
    'shorten_number',
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
        return ' '.join(word.capitalize() for word in name.split('_'))


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


def get(ls: List[Any], name: Optional[str] = None,
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


def shorten_number(number: Union[int, float], /) -> str:
    for letter, amount in reversed(NUMBER_SCALES):
        if number >= amount:
            return f'{number / amount:.1f}{letter}'
    return f'{number / amount:.1f}'
