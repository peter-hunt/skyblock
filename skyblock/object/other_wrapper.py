from typing import Dict, Optional

from ..constant.color import GRAY, GREEN, RED
from ..function.util import format_name, format_number, format_short


__all__ = ['collection_type', 'mob_type', 'enchanted_book_type', 'init_type']


def collection_type(cls: type, /) -> type:
    anno = getattr(cls, '__annotations__', {})
    default = {}
    for name in anno:
        if hasattr(cls, name):
            default[name] = getattr(cls, name)

    init_str = 'lambda self'
    for key in anno:
        if key in default:
            init_str += f', {key}={default[key]!r}'
        else:
            init_str += f', {key}'

    init_str += ': ('
    for key in anno:
        init_str += f'setattr(self, {key!r}, {key}), '
    init_str += 'None,)[-1]'

    cls.__init__ = eval(init_str)

    return cls


def mob_type(cls):
    anno = getattr(cls, '__annotations__', {})
    default = {}
    for name in anno:
        if hasattr(cls, name):
            default[name] = getattr(cls, name)

    init_str = 'lambda self'
    for key in anno:
        if key in default:
            init_str += f', {key}={default[key]!r}'
        else:
            init_str += f', {key}'
    init_str += ': ('
    for key in anno:
        init_str += f'setattr(self, {key!r}, {key}), '
    init_str += 'None,)[-1]'

    cls.__init__ = eval(init_str)

    copy_str = 'lambda self: self.__class__('
    copy_str += ', '.join(f'self.{key}' for key in anno)
    copy_str += ')'

    cls.copy = eval(copy_str)

    def display(self):
        if self.health < 100_000:
            health_str = format_number(self.health)
        else:
            health_str = format_short(self.health)
        return (f'{GRAY}Lv{self.level} {RED}{format_name(self.name)}'
                f' {GREEN}{health_str}{RED}❤{GREEN}')

    cls.display = display

    return cls


def enchanted_book_type(cls: type, /) -> type:
    def __init__(self, enchantments: Dict[str, int] = {},
                 rarity: str = 'common',
                 name: str = 'enchanted_book'):
        self.name = 'enchanted_book'
        self.enchantments = enchantments

        max_lvl = 0
        if len(enchantments) != 0:
            max_lvl = max(enchantments.values())
        if max_lvl <= 4:
            self.rarity = 'common'
        elif max_lvl == 5:
            self.rarity = 'uncommon'
        elif max_lvl == 6:
            self.rarity = 'rare'
        elif max_lvl == 7:
            self.rarity = 'epic'
        elif max_lvl == 8:
            self.rarity = 'legendary'
        elif max_lvl == 9:
            self.rarity = 'mythic'
        else:
            self.rarity = 'supreme'

    cls.__init__ = __init__

    def copy(self, /):
        return type(self)(self.name, self.enchantments, self.rarity)

    cls.copy = copy

    return cls


def init_type(cls: type, /) -> type:
    anno = getattr(cls, '__annotations__', {})
    default = {}
    for name in anno:
        if hasattr(cls, name):
            default[name] = getattr(cls, name)

    init_str = 'lambda self'
    for key in anno:
        if key in default:
            init_str += f', {key}={default[key]!r}'
        else:
            init_str += f', {key}'
    init_str += ': ('
    for key in anno:
        init_str += f'setattr(self, {key!r}, {key}), '
    init_str += 'None,)[-1]'

    cls.__init__ = eval(init_str)

    return cls
