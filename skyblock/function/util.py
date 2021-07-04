from itertools import cycle
from re import fullmatch
from subprocess import call
from textwrap import wrap
from typing import Any, Dict, List, Optional, Tuple, Union
from types import FunctionType

from ..constant.color import CRIT_COLORS
from ..constant.enchanting import ENCHS
from ..constant.util import (
    NUMBER_SCALES, ROMAN_NUM, SPECIAL_NAMES, IGNORED_WORDS,
)

from .io import red, yellow


__all__ = [
    'checkpoint', 'clear', 'format_name', 'format_number', 'format_roman',
    'format_short',  'get', 'generate_help', 'includes', 'index',
    'is_valid_usage',
]


def checkpoint(func: FunctionType, /) -> FunctionType:
    """
    Make the function immute to KeyboardInterrupt.

    Args:
        func: Original function.

    Returns:
        Wrapped function.
    """

    def result(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyboardInterrupt:
            yellow('\nKeyboardInterruption')

    result.__name__ = func.__name__
    result.__doc__ = func.__doc__
    return result


def clear():
    """
    Clear the command line buffer.
    """

    call(['clear'])


def _format_word(word: str, /) -> str:
    """
    Display a word. Used in name displaying.

    Args:
        word: A word to format.

    Returns:
        A string of the formatted word.
    """

    return word.lower() if word in IGNORED_WORDS else word.capitalize()


def format_crit(string: str, /) -> str:
    """
    Format a crit damage.

    Args:
        string: Formatted string to be colored.

    Returns:
        A string of the colored damage.
    """

    result = ''
    color_iter = iter(cycle(CRIT_COLORS))
    last_color = next(color_iter)
    next_color = last_color

    for i, char in enumerate(string):
        if fullmatch(r'\d', char):
            last_color = next_color
        result += last_color
        if i == 0:
            result += '✧'
        result += char
        if fullmatch(r'\d', char):
            next_color = next(color_iter)
    result += '✧'

    return result


def format_name(name: str, /) -> str:
    """
    Format a name.

    Args:
        name: A name to format.

    Returns:
        A string of the formatted name.
    """

    if name in SPECIAL_NAMES:
        return SPECIAL_NAMES[name]
    else:
        return ' '.join(_format_word(word) for word in name.split('_'))


def format_number(number: Union[int, float], /) -> str:
    """
    Format an number with commas for readability.

    Args:
        number: A float or an integer.

    Returns:
        A string of the formatted number.
    """

    if number % 1 == 0:
        string = f'{number:.0f}'
        string = ','.join(part[::-1] for part in wrap(string[::-1], 3)[::-1])
        return string
    else:
        string = f'{number:.1f}'
        integer, floating = string.split('.')
        integer = ','.join(part[::-1] for part in wrap(integer[::-1], 3)[::-1])
        return f'{integer}.{floating}'


def format_roman(number: int, /) -> str:
    """
    Format an number in roman numerals.

    Args:
        number: An integer to be converted.

    Returns:
        A string of the formatted number.
    """

    result = ''
    for letter, amount in reversed(ROMAN_NUM):
        while number >= amount:
            number -= amount
            result += letter
    return result


def format_short(number: Union[int, float], /) -> str:
    """
    Format an number in shortened form.

    Args:
        number: An integer to be converted.

    Returns:
        A string of the formatted number.
    """

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


def generate_help(doc: str, /) -> Dict[str, str]:
    """
    Generate help dict.

    Args:
        doc: Original documentation string.

    Returns:
        A dict of the commands and descriptions.
    """

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
    """
    Get an object from the list.

    Args:
        ls: List to find the object from.
        name: Name of the target object.
        default: Object returned if object with the given name is not found.
        **kwargs: Restrictions to be found and attributes to be added.

    Returns:
        An object found or default if not found.
    """

    attrs = {}
    args = {}
    for key, value in kwargs.items():
        if key in {'count', 'enchantments'}:
            attrs[key] = value
        else:
            args[key] = value

    for item in ls:
        if name is not None and item.name != name:
            continue
        for key, value in args.items():
            if getattr(item, key, None) != value:
                break
        else:
            result = item.copy() if hasattr(item, 'copy') else item
            for attr, value in attrs.items():
                setattr(result, attr, value)
            return result

    return default.copy() if hasattr(default, 'copy') else default


def get_ench(name: str, /) -> Tuple[str, Tuple[int]]:
    """
    Get experience level costs for an enchantment.

    Args:
        name: Name of the enchantment.

    Returns:
        Tuple of level cost to enchant the item with the enchantment.
    """

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
    """
    Detect whether if object with given name is in the list.

    Args:
        ls: List to find the object from.
        name: Name of the object.

    Returns:
        Boolean of whether if the name is found from the list
    """

    for obj in ls:
        if obj.name == name:
            return True
    return False


def index(ls: List[Any], name: str, /) -> int:
    """
    Get index of the object with the given name from the list.

    Args:
        ls: List to find the object from.
        name: Name of the object.

    Returns:
        Integer of the object
    """

    for i, obj in enumerate(ls):
        if obj.name == name:
            return i
    raise ValueError(f'{name!r} not found from the list.')


def is_valid_usage(usage: str, words: List[str], /) -> bool:
    """
    Detect whether command usage is valid.

    Args:
        usage: Command from the user.
        words: Usage of the command from the documentation.

    Returns:
        Boolean of whether if the command usage is valid.
    """

    all_words = usage.split()[1:]
    pos_words = [word for word in all_words if word[0] != '[']

    if len(words) > len(all_words):
        return False
    if len(words) < len(pos_words):
        return False
    return True


def parse_int(string: str, /) -> Optional[int]:
    """
    Parse integer from string.

    Args:
        string: String of the integer to be parsed.

    Returns:
        Integer parsed if the string is valid, otherwise warn the user.
    """

    if fullmatch(r'\d+', string):
        return int(string)
    else:
        red('Please input a valid number!')
        return
