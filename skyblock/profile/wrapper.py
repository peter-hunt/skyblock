from json import dump, load
from os.path import join
from pathlib import Path
from random import choices
from re import sub
from time import sleep
from typing import Iterable, Optional

from ..constant.color import WHITE
from ..function.item import load_item
from ..function.io import red, yellow
from ..function.path import is_profile
from ..function.util import display_name, parse_int
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

    # with open(join(Path.home(), 'skyblock',
    #             'saves', f'{self.name}.json'), 'w') as file:

    dump_str = '''
    lambda self: (
        file := open(join(Path.home(), 'skyblock',
                     'saves', f'{self.name}.json'), 'w'),
        dump({'name': self.name, %s}, file, indent=4),
        file.close(),
        None,
    )[-1]
    '''
    content = ', '.join(
        f'{key!r}: [item.to_obj() for item in self.{key}]'
        if key in {'armor', 'pets', 'ender_chest', 'inventory',
                   'potion_bag', 'quiver', 'stash', 'talisman_bag',
                   'wardrobe'}
        else f'{key!r}: self.{key}'
        for key in anno
    )
    dump_str = dump_str.replace('%s', content)
    dump_str = sub(r'\n\s+', '', dump_str)

    cls.dump = eval(dump_str)

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
        sentence = choices((
            "%s doesn't seem to want to talk to you.",
            "%s has got nothing to say to you.",
            "%s is in his peace.",
            "%s seems tired and sleepy.",
            "%s stared at you and didn't talk.",
            "%s smiled mysteriously.",
            "%s made a strange noise.",
            "%s spoke a strange language you've never heard before.",
        ), (20, 25, 20, 18, 10, 4, 2, 1))[0]
        sentence = sentence.replace('%s', display_name(npc.name))
        yellow(f'[NPC] {display_name(npc.name)}'
               f'{WHITE}: ({sentence})')

    cls.npc_silent = npc_silent

    @staticmethod
    def npc_talk(name: str, dialog: Iterable):
        iterator = iter(dialog)
        yellow(f'[NPC] {display_name(name)}{WHITE}: {next(iterator)}')
        for sentence in iterator:
            sleep(1.5)
            yellow(f'[NPC] {display_name(name)}{WHITE}: {sentence}')

    cls.npc_talk = npc_talk

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
