from typing import Dict, Optional


ITEM_OBJS = []


def item_type(cls):
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
    # print(init_str)
    setattr(cls, '__init__', eval(init_str))

    if cls.__name__ == 'Empty':
        to_obj_str = 'lambda self: {}'
    else:
        to_obj_str = 'lambda self: {'
        for key in anno:
            to_obj_str += f'{key!r}: self.{key}, '
        to_obj_str += f"'type': {cls.__name__.lower()!r}" + '}'
    # print(to_obj_str)
    setattr(cls, 'to_obj', eval(to_obj_str))

    from_obj_str = 'lambda cls, obj: cls('
    from_obj_str += ', '.join(
        f'obj.get({key!r}, {default[key]!r})' if key in default
        else f'obj[{key!r}]' for key in anno
    )
    from_obj_str += ')'
    # print(from_obj_str)
    setattr(cls, 'from_obj', classmethod(eval(to_obj_str)))

    ITEM_OBJS.append(cls)

    return cls


class ItemType:
    pass


@item_type
class Item(ItemType):
    name: str
    count: int
    # common | uncommon | rare | epic | legendary |
    # mythic | supreme | special | very_special
    rarity: str = 'common'


@item_type
class Empty(ItemType):
    pass


@item_type
class Tool(ItemType):
    name: str
    rarity: str = 'common'
    modifier: Optional[str] = None
    enchantments: Dict[str, int] = {}


@item_type
class Pickaxe(ItemType):
    name: str
    rarity: str
    breaking_power: int
    mining_speed: int
    modifier: Optional[str] = None,
    enchantments: Dict[str, int] = {}


@item_type
class Weapon(ItemType):
    name: str
    rarity: str
    damage: int
    modifier: Optional[str] = None
    enchantments: Dict[str, int] = {}
    dungeon_stars: Optional[int] = None
    combat_skill_req: Optional[int] = None
    dungeon_skill_req: Optional[int] = None


class Armor(ItemType):
    name: str
    rarity: str
    # helmet | chestplate | leggings | boots
    part: str
    modifier: Optional[str] = None
    enchantments: Dict[str, int] = {}
    dungeon_stars: Optional[int] = None
    combat_skill_req: Optional[int] = None
    dungeon_skill_req: Optional[int] = None


class Potion(ItemType):
    name: str
    rarity: str
    potion: str
    duration: int
    level: int


class Pet(ItemType):
    name: str
    rarity: str
    active: bool = False
    exp: float = 0.0
    candy_used: int = 0


def from_obj(obj):
    if isinstance(obj, ItemType):
        return obj
    elif 'type' not in obj:
        return Empty()
    for cls in ITEM_OBJS:
        if obj['type'] == cls.__name__.lower():
            return cls.from_obj(obj)
    else:
        raise ValueError(f"invalid item obj type: {obj['type']!r}")


MATERIALS = [
    # name, stack_size, rarity
    Item('wheat', 64, 'common'),
    Item('carrot', 64, 'common'),
    Item('potato', 64, 'common'),
    Item('melon', 64, 'common'),
    Item('sugar_cane', 64, 'common'),
    Item('pumpkin', 64, 'common'),
    Item('cocoa_beans', 64, 'common'),
    Item('red_mushroom', 64, 'common'),
    Item('brown_mushroom', 64, 'common'),
    Item('sand', 64, 'common'),
]

ITEMS = [
    Pickaxe('rookie_pickaxe', rarity='common',
            breaking_power=2, mining_speed=150),
    Pickaxe('promising_pickaxe', rarity='uncommon',
            breaking_power=3, mining_speed=190),
]
