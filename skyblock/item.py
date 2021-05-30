from typing import Any, Dict, Optional

from .constant import RARITY_COLORS
from .function import Number, roman, get

__all__ = [
    'item_type', 'ItemType', 'from_obj',
    'Item', 'Empty',
    'Pickaxe', 'Axe', 'Sword', 'Bow', 'Armor',
    'Potion', 'Pet', 'Resource', 'Mineral', 'TreeType',
    'COLLECTIONS', 'MINERALS', 'TREES', 'RESOURCES',
    'WEAPONS', 'TOOLS', 'ALL_ITEM', 'SELL_PRICE',
]

ITEM_OBJS = []


def item_type(cls: type, /) -> type:
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
    setattr(cls, '__init__', eval(init_str))

    if cls.__name__ == 'Empty':
        to_obj_str = 'lambda self: {}'
    else:
        to_obj_str = 'lambda self: {'
        for key in anno:
            to_obj_str += f'{key!r}: self.{key}, '
        to_obj_str += f"'type': {cls.__name__.lower()!r}}}"
    setattr(cls, 'to_obj', eval(to_obj_str))

    from_obj_str = 'lambda cls, obj: cls('
    from_obj_str += ', '.join(
        f'obj.get({key!r}, {default[key]!r})' if key in default
        else f'obj[{key!r}]' for key in anno
    )
    from_obj_str += ')'
    setattr(cls, 'from_obj', classmethod(eval(from_obj_str)))

    copy_str = 'lambda self: self.__class__('
    copy_str += ', '.join(f'self.{key}' for key in anno)
    copy_str += ')'
    setattr(cls, 'copy', eval(copy_str))

    display_str = """
    lambda self: (
        rarity_color := RARITY_COLORS[self.rarity],
        name := ' '.join(word.capitalize() for word in self.name.split('_')),
        count := f' x {self.count}' if getattr(self, 'count', 1) != 1 else '',
        (
            stars := '',
        ) if (not hasattr(self, 'dungeon_stars')
              or self.dungeon_stars is None) else (
            stars := (' \\x1b[38;2;255;170;0m'
                      + self.dungeon_stars * '✪' + rarity_color),
        ) if (self.dungeon_stars <= 5) else (
            stars := (' \\x1b[38;2;255;85;850m' + (self.dungeon_stars - 5) * '✪'
                      + '\\x1b[38;2;255;170;0m' + (10 - self.dungeon_stars) * '✪'
                      + rarity_color),
        ),
        display := f'{rarity_color}{name}{stars}{count}\\x1b[0m'
    )[-1] if (not isinstance(self, Empty)) else (
        '\x1b[1;38;2;255;255;255mEmpty\x1b[0m'
    )
    """.replace('\n', '')
    setattr(cls, 'display', eval(display_str))

    # 0;0;170 for enchantments
    info_str = """
    lambda self: (
        rarity_color := RARITY_COLORS[self.rarity],
        display_name := ' '.join(word.capitalize()
                                 for word in self.name.split('_')),
        info := f'{rarity_color}{display_name}',
        (
            info := info + '\\x1b[0m',
        ) if (not hasattr(self, 'dungeon_stars')
              or self.dungeon_stars is None) else (
            info := (info + ' \\x1b[38;2;255;170;0m'
                     + self.dungeon_stars * '✪' + '\\x1b[0m'),
        ) if (self.dungeon_stars <= 5) else (
            info := (info + ' \\x1b[38;2;255;85;850m'
                     + (self.dungeon_stars - 5) * '✪' + '\\x1b[38;2;255;170;0m'
                     + (10 - self.dungeon_stars) * '✪' + '\\x1b[0m'),
        ),
        type_name := self.__class__.__name__.upper(),
        (
            info := (info + f'\\n\\x1b[38;2;85;85;85m'
                     f'Breaking Power: \\x1b[38;2;255;85;85m+'
                     f'{self.breaking_power}\\x1b[0m\\n'),
        ) if (hasattr(self, 'breaking_power')) else (),
        (
            info := (info + f'\\n\\n\\x1b[38;2;170;170;170m'
                     f'Mining Speed: \\x1b[38;2;255;85;85m+'
                     f'{self.mining_speed}\\x1b[0m\\n'),
        ) if (hasattr(self, 'mining_speed')) else (),
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
              self.combat_skill_req is not None) else (
            info := (info + f'\\n\\x1b[38;2;170;0;0m❣ '
                     f'\\x1b[38;2;255;85;85mRequires '
                     f'\\x1b[38;2;85;255;85mCatacombs Skill '
                     f'{self.dungeon_skill_req}\\x1b[0m'),
        ) if (hasattr(self, 'dungeon_skill_req') and
              self.dungeon_skill_req is not None) else (
            info := (info + f'\\n\\x1b[38;2;170;0;0m❣ '
                     f'\\x1b[38;2;255;85;85mRequires '
                     f'\\x1b[38;2;85;255;85mCatacombs Floor '
                     f'{roman(self.dungeon_completion_req)} Completion\\x1b[0m'),
        ) if (hasattr(self, 'dungeon_completion_req') and
              self.dungeon_completion_req is not None) else (),
        info := (info + f'\\n{rarity_color}{self.rarity.upper()} '
                 f'{type_name}\\x1b[0m'),
        info := info.replace('\\n\\n', '\\n'),
        info,
    )[-1]
    """.replace('\n', '')
    setattr(cls, 'info', eval(info_str))

    ITEM_OBJS.append(cls)

    return cls


class ItemType:
    pass


@item_type
class Item(ItemType):
    name: str
    count: int = 1
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
class Axe(ItemType):
    name: str
    rarity: str
    tool_speed: int
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


@item_type
class TreeType(Resource):
    name: str
    drop: str
    hardness: int = 2
    foraging_exp: Number = 1


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


COLLECTIONS = [
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

    Item('oak_wood', 64, 'common'),
    Item('birch_wood', 64, 'common'),
    Item('spruce_wood', 64, 'common'),
    Item('dark_oak_wood', 64, 'common'),
    Item('acacia_wood', 64, 'common'),
    Item('jungle_wood', 64, 'common'),
]

MINERALS = [
    Mineral('stone', 'cobblestone', 1, 1, 0, 1.5, 1),
    Mineral('coal_ore', 'coal', 1, 1, 1, 3, 5),
]

TREES = [
    TreeType('oak', 'oak_wood', 2, 6),
    TreeType('birch', 'birch_wood', 2, 6),
    TreeType('spruce', 'spruce_wood', 2, 6),
    TreeType('dark_oak', 'dark_oak_wood', 2, 6),
    TreeType('acacia', 'acacia_wood', 2, 6),
    TreeType('jungle', 'jungle_wood', 2, 6),
]

RESOURCES = MINERALS + TREES

WEAPONS = [
    Sword('aspect_of_the_dragons', 'legendary', damage=225,
          combat_skill_req=18),
    Sword('dreadlord_sword', 'rare', damage=120,
          dungeon_skill_req=5),
    Sword('livid_dagger', 'legendary', damage=210,
          dungeon_completion_req=5),
]

TOOLS = [
    Pickaxe('wooden_pickaxe', rarity='common',
            breaking_power=1, mining_speed=70),
    Pickaxe('golden_pickaxe', rarity='common',
            breaking_power=1, mining_speed=250),
    Pickaxe('stone_pickaxe', rarity='common',
            breaking_power=2, mining_speed=110),
    Pickaxe('iron_pickaxe', rarity='common',
            breaking_power=3, mining_speed=160),
    Pickaxe('diamond_pickaxe', rarity='uncommon',
            breaking_power=4, mining_speed=230),

    Axe('wooden_axe', rarity='common', tool_speed=2),
    Axe('stone_axe', rarity='common', tool_speed=4),
    Axe('golden_axe', rarity='common', tool_speed=12),
    Axe('iron_axe', rarity='common', tool_speed=6),
    Axe('wooden_axe', rarity='uncommon', tool_speed=8),
]

ALL_ITEM = COLLECTIONS + RESOURCES + WEAPONS + TOOLS


def get_item(name: str, *, default: Any = None) -> ItemType:
    return get(ALL_ITEM, name, default=default).copy()


SELL_PRICE = {
    'cobblestone': 1,
    'coal': 2,

    'oak_wood': 2,
    'birch_wood': 2,
    'spruce_wood': 2,
    'dark_oak_wood': 2,
    'acacia_wood': 2,
    'jungle_wood': 2,
}
