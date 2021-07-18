from json import load as json_load
from os.path import join
from pathlib import Path
from re import sub

from ..constant.colors import *
from ..myjson import dump as json_dump
from ..function.io import *
from ..function.path import is_profile
from ..object.collection import COLLECTIONS
from ..object.object import *
from ..object.placed_minion import load_minion
from ..map.object import *

from .function import profile_functions


__all__ = ['profile_wrapper']


def profile_wrapper(cls):
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
                value = getattr(self, key)

                if key in {
                    'armor', 'pets', 'ender_chest', 'inventory',
                    'placed_minions', 'potion_bag', 'quiver', 'stash',
                    'talisman_bag', 'wardrobe',
                }:
                    obj[key] = [item.to_obj() for item in value]
                elif key in {'collection', 'stats'}:
                    obj[key] = {
                        name: param for name, param in value.items()
                        if param != 0
                    }
                else:
                    obj[key] = value

            json_dump(obj, file, indent=2)

    cls.dump = dump

    load_str = '''
    lambda cls, name: ((
        file := open(join(Path.home(), 'skyblock',
                          'saves', f'{name}.json')),
        obj := json_load(file),
        result := cls(name, %s),
        file.close(),
        result,
    ) if (is_profile(name)) else (
        red('Error: Profile not found.'),
        None,
    ))[-1]
    '''

    content = ''
    for i, key in enumerate(default):
        if i != 0:
            content += ', '

        if key in {'armor', 'pets', 'ender_chest', 'inventory', 'potion_bag',
                   'quiver', 'stash', 'talisman_bag', 'wardrobe'}:
            content += (f'{key}=[load_item(item)'
                        f' for item in obj.get({key!r}, {default[key]!r})]')
        elif key == 'placed_minions':
            content += (f'{key}=[result if'
                        f' (result := load_minion(item)) != {{}} else Empty()'
                        f' for item in obj.get({key!r}, {default[key]!r})]')
        elif key == 'collection':
            coll_names = [coll.name for coll in COLLECTIONS]
            content += (f'collection={{coll: obj.get({key!r},'
                        f' {{}}).get(coll, 0)'
                        f' for coll in {coll_names}}}')
        elif key == 'stats':
            content += f'stats=obj.get({key!r}, {{}})'
        else:
            content += f'{key}=obj.get({key!r}, {default[key]!r})'
    load_str = load_str.replace('%s', content)
    load_str = sub(r'\n\s+', '', load_str)

    cls.load = classmethod(eval(load_str))

    for name, func in profile_functions.items():
        setattr(cls, name, func)

    return cls
