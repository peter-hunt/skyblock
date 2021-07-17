from typing import Dict

from ..constant.color import *
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

    def to_obj(self, /):
        result = {}
        result['name'] = self.name
        result['category'] = self.category
        result['levels'] = self.levels

    cls.to_obj = to_obj

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
                 name: str = 'enchanted_book',
                 rarity: str = 'common'):
        self.name = 'enchanted_book'
        self.enchantments = enchantments

        max_level = 0
        if len(enchantments) != 0:
            max_level = max(enchantments.values())
        if max_level <= 4:
            self.rarity = 'common'
        elif max_level == 5:
            self.rarity = 'uncommon'
        elif max_level == 6:
            self.rarity = 'rare'
        elif max_level == 7:
            self.rarity = 'epic'
        elif max_level == 8:
            self.rarity = 'legendary'
        elif max_level == 9:
            self.rarity = 'mythic'
        else:
            self.rarity = 'supreme'

    cls.__init__ = __init__

    def copy(self, /):
        return type(self)(self.enchantments, self.name, self.rarity)

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

    copy_str = 'lambda self: self.__class__('
    copy_str += ', '.join(f'self.{key}' for key in anno)
    copy_str += ')'

    cls.copy = eval(copy_str)

    return cls
