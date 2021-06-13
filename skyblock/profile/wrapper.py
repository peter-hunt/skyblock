from json import dump as json_dump, load
from os.path import join
from pathlib import Path
from re import sub
from typing import Optional

from ..constant.color import WHITE
from ..function.item import load_item
from ..function.io import red, yellow
from ..function.path import is_profile
from ..function.util import display_name, parse_int
from ..item.object import Empty
from ..map.object import Npc

__all__ = ['profile_type']


def profile_type(cls):
    anno = [key for key in getattr(cls, '__annotations__', {})
            if key != 'name']

    default = {}
    for name in anno:
        if hasattr(cls, name):
            default[name] = getattr(cls, name)

    init_str = 'lambda self, name'
    for key in anno:
        if key in default:
            init_str += f', {key}={default[key]!r}'
        else:
            init_str += f', {key}'
    init_str += ": (setattr(self, 'name', name), "
    for key in anno:
        init_str += f'setattr(self, {key!r}, {key}), '
    init_str += 'None,)[-1]'

    cls.__init__ = eval(init_str)

    def dump(self, /):
        with open(join(Path.home(), 'skyblock',
                       'saves', f'{self.name}.json'), 'w') as file:
            obj = {'name': self.name}
            for key in anno:
                if key in {'armor', 'pets', 'ender_chest', 'inventory',
                           'potion_bag', 'quiver', 'stash', 'talisman_bag',
                           'wardrobe'}:
                    obj[key] = [item.to_obj() for item in getattr(self, key)]
                else:
                    obj[key] = getattr(self, key)

            json_dump(obj, file)

    cls.dump = dump

    load_str = '''
    lambda cls, name: ((
        file := open(join(Path.home(), 'skyblock',
                          'saves', f'{name}.json')),
        obj := load(file),
        result := cls(name, %s),
        file.close(),
        result,
    ) if (is_profile(name)) else (
        red('Error: Profile not found.'),
        None,
    ))[-1]
    '''
    content = ', '.join(
        (
            f'{key}=[load_item(item) for item in obj.get({key!r}, {default[key]!r})]'
            if key in {'armor', 'pets', 'ender_chest', 'inventory',
                       'potion_bag', 'quiver', 'stash', 'talisman_bag',
                       'wardrobe'}
            else f'{key}=obj.get({key!r}, {default[key]!r})'
        )
        if key in default
        else f'{key}=obj[{key!r}]' for key in anno
    )
    load_str = load_str.replace('%s', content)
    load_str = sub(r'\n\s+', '', load_str)

    cls.load = classmethod(eval(load_str))

    @staticmethod
    def npc_silent(npc: Npc, /):
        yellow(f'[NPC] {display_name(npc.name)}'
               f"{WHITE}: ({display_name(npc.name)} said nothing)")

    cls.npc_silent = npc_silent

    def parse_index(self, word: str, length: Optional[int] = None, /) -> Optional[int]:
        index = parse_int(word)
        if index is None:
            return
        if length is None:
            length = len(self.inventory)
        if index <= 0 or index > length:
            red(f'Index out of bound: {index}')
            return
        return index - 1

    cls.parse_index = parse_index

    return cls
