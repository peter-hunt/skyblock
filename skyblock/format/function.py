from typing import Any, Dict

from ..constant.colors import *
from ..function.math import fround
from ..function.util import format_name, format_number, format_zone


__all__ = ['format_temp']


def format_temp(template: str, params: Dict[str, Any] = {}, /) -> str:
    result = template

    for code, color in COLOR_CODE.items():
        result = result.replace(f'%%{code}%%', color)

    for code, color in STAT_COLORS.items():
        result = result.replace(f'%%{code}%%', f'{color} {format_name(code)}')

    for key, value in params.items():
        if key == 'place':
            value_str = ', '.join(
                f'{BLUE}{format_zone(zone)}{GRAY}' for zone in value
            )
        elif isinstance(value, (int, float)):
            value_str = format_number(fround(value, 1))
        elif isinstance(value, tuple):
            if len(value) == 0:
                value_str = ''
            elif len(value) == 1:
                value_str = f'{value[0]}'
            elif len(value) == 2:
                value_str = f'{value[0]} and {value[1]}'
            else:
                names = [format_name(name) for name in value]
                names[-1] = f'and {names[-1]}'
                value_str = ', '.join(names)
        else:
            value_str = f'{value}'

        result = result.replace(f'%%{key}%%', value_str)

    return result
