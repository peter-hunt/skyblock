from typing import Dict, Optional, Union

from .const import RARITY_COLORS
from .func import roman

__all__ = [
    'item_type', 'ItemType',
    'Item', 'Empty',
    'Pickaxe', 'Weapon', 'Armor',
    'Potion', 'Pet', 'Resource', 'Mineral',
    'from_obj',
    'ITEMS', 'MINERALS', 'RESOURCES', 'TOOLS', 'ALL_ITEM',
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

    display_str = """
    lambda self: (
        rarity_color := RARITY_COLORS[self.rarity],
        name := ' '.join(word.capitalize() for word in self.name.split('_')),
        count := f' x {self.count}' if getattr(self, 'count', 1) != 1 else '',
        display := f'{rarity_color}{name}{count}'
    )[-1] if (not isinstance(self, Empty)) else (
        '\x1b[1;38;2;255;255;255mEmpty\x1b[0m'
    )
    """.replace('\n', '')
    # print(display_str)
    setattr(cls, 'display', eval(display_str))
    # 170	170	170
    info_str = """
    lambda self: (
        rarity_color := RARITY_COLORS[self.rarity],
        display_name := ' '.join(word.capitalize()
                                 for word in self.name.split('_')),
        info := f'{rarity_color}{display_name}\\x1b[0m',
        type_name := self.__class__.__name__.upper(),
        (
            info := (info + f'\\n\\x1b[38;2;170;170;170m'
                     f'Damage: \\x1b[38;2;255;85;85m+{self.damage}\\x1b[0m'),
        ) if (hasattr(self, 'damage')) else (),
        (
            info := (info + '\\n\\n\\x1b[38;2;85;85;85m'
                     'This item can be reforged!\\x1b[0m'),
        ) if (hasattr(self, 'modifier')) else (),
        (
            info := (info + f'\\n\\x1b[38;2;170;0;0m❣ '
                     f'\\x1b[38;2;255;85;85mRequires '
                     f'\\x1b[38;2;85;255;85mCombat Skill '
                     f'{self.combat_skill_req}\\x1b[0m'),
        ) if (hasattr(self, 'combat_skill_req') and
              self.combat_skill_req is not None) else (),
        (
            info := (info + f'\\n\\x1b[38;2;170;0;0m❣ '
                     f'\\x1b[38;2;255;85;85mRequires '
                     f'\\x1b[38;2;85;255;85mCatacombs Skill '
                     f'{self.dungeon_skill_req}\\x1b[0m'),
        ) if (hasattr(self, 'dungeon_skill_req') and
              self.dungeon_skill_req is not None) else (),
        (
            info := (info + f'\\n\\x1b[38;2;170;0;0m❣ '
                     f'\\x1b[38;2;255;85;85mRequires '
                     f'\\x1b[38;2;85;255;85mCatacombs Floor '
                     f'{roman(self.dungeon_completion_req)} Completion\\x1b[0m'),
        ) if (hasattr(self, 'dungeon_completion_req') and
              self.dungeon_completion_req is not None) else (),
        info := (info + f'\\n{rarity_color}{self.rarity.upper()} '
                 f'{type_name}\\x1b[0m'),
        info,
    )[-1]
    """.replace('\n', '')
    # print(info_str)
    setattr(cls, 'info', eval(info_str))

    # inform_str = "lambda self: f'{self.__class__.__name__}'"
    # # print(inform_str)
    # setattr(cls, 'inform', eval(inform_str))

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
class Pickaxe(ItemType):
    name: str
    rarity: str
    breaking_power: int
    mining_speed: int
    modifier: Optional[str] = None
    enchantments: Dict[str, int] = {}


@item_type
class Sword(ItemType):
    name: str
    rarity: str
    damage: int
    modifier: Optional[str] = None
    enchantments: Dict[str, int] = {}
    dungeon_stars: Optional[int] = None
    combat_skill_req: Optional[int] = None
    dungeon_skill_req: Optional[int] = None
    dungeon_completion_req: Optional[int] = None


@item_type
class Bow(ItemType):
    name: str
    rarity: str
    damage: int
    modifier: Optional[str] = None
    enchantments: Dict[str, int] = {}
    dungeon_stars: Optional[int] = None
    combat_skill_req: Optional[int] = None
    dungeon_skill_req: Optional[int] = None
    dungeon_completion_req: Optional[int] = None


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
    def type(self):
        return type(self).__name__


@item_type
class Mineral(Resource):
    name: str
    drop: str
    amount: int = 1
    breaking_power: int = 0
    exp: Number = 1
    hardness: int = 2
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

MINERALS = [
    Mineral('stone', 'cobblestone', 1, 1, 0, 1.5, 1),
    Mineral('coal_ore', 'coal', 1, 1, 1, 3, 5),
]

RESOURCES = MINERALS + []

WEAPONS = [
    Sword('aspect_of_the_dragons', 'legendary', 225,
          combat_skill_req=18),
    Sword('dreadlord_sword', 'rare', 120,
          dungeon_skill_req=5),
    Sword('livid_dagger', 'legendary', 210,
          dungeon_completion_req=5),
]

TOOLS = [
    Pickaxe('wooden_pickaxe', rarity='common',
            breaking_power=1, mining_speed=70),
    Pickaxe('stone_pickaxe', rarity='common',
            breaking_power=2, mining_speed=110),
    Pickaxe('iron_pickaxe', rarity='common',
            breaking_power=3, mining_speed=160),
    Pickaxe('diamond_pickaxe', rarity='uncommon',
            breaking_power=4, mining_speed=230),
    # Pickaxe('rookie_pickaxe', rarity='common',
    #         breaking_power=2, mining_speed=150),
    # Pickaxe('promising_pickaxe', rarity='uncommon',
    #         breaking_power=3, mining_speed=190),
]

ALL_ITEM = ITEMS + MINERALS + WEAPONS + TOOLS
