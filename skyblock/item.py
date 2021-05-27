from typing import Dict, Optional, Union

__all__ = [
    'item_type', 'ItemType',
    'Item', 'Empty',
    'Tool', 'Pickaxe', 'Weapon', 'Armor',
    'Potion', 'Pet', 'Resource', 'Mineral',
    'from_obj',
    'ITEMS', 'MINERALS', 'TOOLS', 'ALL_ITEM',
]

Number = Union[int, float]

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
        to_obj_str += f"'type': {cls.__name__.lower()!r}}}"
    # print(to_obj_str)
    setattr(cls, 'to_obj', eval(to_obj_str))

    from_obj_str = 'lambda cls, obj: cls('
    from_obj_str += ', '.join(
        f'obj.get({key!r}, {default[key]!r})' if key in default
        else f'obj[{key!r}]' for key in anno
    )
    from_obj_str += ')'
    # print(from_obj_str)
    setattr(cls, 'from_obj', classmethod(eval(from_obj_str)))

    display_str = "lambda self: f'{self.__class__.__name__}("
    display_str += ', '.join(
        f'{{key}}={{obj[{key!r}]}}' for key in anno
    )
    display_str += ")'"
    # print(display_str)
    setattr(cls, 'display', eval(to_obj_str))

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


@item_type
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


@item_type
class Potion(ItemType):
    name: str
    rarity: str
    potion: str
    duration: int
    level: int


@item_type
class Pet(ItemType):
    name: str
    rarity: str
    active: bool = False
    exp: float = 0.0
    candy_used: int = 0


class Resource:
    pass


@item_type
class Mineral(Resource):
    name: str
    drop: str
    amount: int = 1
    exp: Number = 1
    mining_exp: Number = 1


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


ITEMS = [
    # name, stack_size, rarity
    Item('wheat', 64, 'common'),
    Item('carrot', 64, 'common'),
    Item('potato', 64, 'common'),
    Item('pumpkin', 64, 'common'),
    Item('melon', 64, 'common'),
    Item('seeds', 64, 'common'),
    Item('red_mushroom', 64, 'common'),
    Item('brown_mushroom', 64, 'common'),
    Item('cocoa_beans', 64, 'common'),
    Item('cactus', 64, 'common'),
    Item('sugar_cane', 64, 'common'),
    Item('feather', 64, 'common'),
    Item('leather', 64, 'common'),
    Item('porkchop', 64, 'common'),
    Item('chicken', 64, 'common'),
    Item('mutton', 64, 'common'),
    Item('rabbit', 64, 'common'),
    Item('nether_wart', 64, 'common'),

    Item('cobblestone', 64, 'common'),
    Item('coal', 64, 'common'),
    Item('iron_ingot', 64, 'common'),
    Item('gold_ingot', 64, 'common'),
    Item('diamond', 64, 'common'),
    Item('lapis_lazuli', 64, 'common'),
    Item('emerald', 64, 'common'),
    Item('redstone', 64, 'common'),
    Item('quartz', 64, 'common'),
    Item('obsidian', 64, 'common'),
    Item('glowstone_dust', 64, 'common'),
    Item('gravel', 64, 'common'),
    Item('ice', 64, 'common'),
    Item('netherrack', 64, 'common'),
    Item('sand', 64, 'common'),
    Item('endstone', 64, 'common'),
    Item('mithril', 64, 'common'),
]

MINREALS = [
    Mineral('coal_ore', 'coal', 1, 1, 5),
]

TOOLS = [
    Pickaxe('rookie_pickaxe', rarity='common',
            breaking_power=2, mining_speed=150),
    Pickaxe('promising_pickaxe', rarity='uncommon',
            breaking_power=3, mining_speed=190),
]

ALL_ITEM = ITEMS + MINREALS + TOOLS
