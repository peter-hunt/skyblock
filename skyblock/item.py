from typing import Any, Dict, Optional

from .constant import (
    RARITY_COLORS,
    CLN, BOLD, F_DARK_RED, F_GOLD, F_GRAY, F_DARK_GRAY, F_GREEN, F_RED, F_WHITE,
)
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

    cls.__init__ = eval(init_str)

    if cls.__name__ == 'Empty':
        to_obj_str = 'lambda self: {}'
    else:
        to_obj_str = 'lambda self: {'
        for key in anno:
            to_obj_str += f'{key!r}: self.{key}, '
        to_obj_str += f"'type': {cls.__name__.lower()!r}}}"

    cls.to_obj = eval(to_obj_str)

    from_obj_str = 'lambda cls, obj: cls('
    from_obj_str += ', '.join(
        f'obj.get({key!r}, {default[key]!r})' if key in default
        else f'obj[{key!r}]' for key in anno
    )
    from_obj_str += ')'

    cls.from_obj = classmethod(eval(from_obj_str))

    copy_str = 'lambda self: self.__class__('
    copy_str += ', '.join(f'self.{key}' for key in anno)
    copy_str += ')'

    cls.copy = eval(copy_str)

    def display(self):
        if isinstance(self, Empty):
            return f'{BOLD}{F_WHITE}Empty{CLN}'

        color = RARITY_COLORS[self.rarity]

        if getattr(self, 'modifer', None) is not None:
            modifier = f'{self.modifier.capitalize()} '
        else:
            modifier = ''

        name = ' '.join(word.capitalize() for word in self.name.split('_'))
        count = f' x {self.count}' if getattr(self, 'count', 1) != 1 else ''

        if getattr(self, 'stars', None) is None:
            stars = ''
        elif self.stars <= 5:
            stars = f' {F_GOLD}' + self.stars * '✪'
        else:
            stars = (f' {F_RED}' + (self.stars - 5) * '✪'
                     + F_GOLD + (10 - self.stars) * '✪')

        return f'{color}{modifier}{name}{stars}{color}{count}{CLN}'

    cls.display = display

    # 0;0;170 for enchantments

    def info(self):
        color = RARITY_COLORS[self.rarity]

        if getattr(self, 'modifer', None) is not None:
            modifier = f'{self.modifier.capitalize()} '
        else:
            modifier = ''

        display_name = ' '.join(word.capitalize()
                                for word in self.name.split('_'))

        if getattr(self, 'stars', None) is None:
            stars = ''
        elif self.stars <= 5:
            stars = f' {F_GOLD}' + self.stars * '✪'
        else:
            stars = (f' {F_RED}' + (self.stars - 5) * '✪'
                     + F_GOLD + (10 - self.stars) * '✪')

        info = f'{color}{modifier}{display_name}{stars}{color}'

        if hasattr(self, 'breaking_power'):
            info += (f'\n{F_DARK_GRAY}Breaking Power: {F_RED}+'
                     f'{self.breaking_power}{CLN}\n')

        if hasattr(self, 'mining_speed'):
            info += (f'\n\n{F_GRAY}'
                     f'Mining Speed: {F_GREEN}+{self.mining_speed}{CLN}\n')

        if hasattr(self, 'damage'):
            info += (f'\n{F_GRAY}Damage: {F_RED}+{self.damage}{CLN}')

        if hasattr(self, 'modifier'):
            info += (f'\n\n{F_DARK_GRAY}'
                     f'This item can be reforged!{CLN}')

        if getattr(self, 'combat_skill_req', None) is not None:
            info += (f'\n{F_DARK_RED}❣ {F_RED}Requires '
                     f'{F_GREEN}Combat Skill {self.combat_skill_req}{CLN}')
        if getattr(self, 'dungeon_skill_req', None) is not None:
            info += (f'\n{F_DARK_RED}❣ {F_RED}Requires '
                     f'{F_GREEN}Catacombs Skill {self.dungeon_skill_req}{CLN}')
        if getattr(self, 'dungeon_completion_req', None) is not None:
            info += (f'\n{F_DARK_RED}❣ {F_RED}Requires {F_GREEN}Catacombs Floor '
                     f'{roman(self.dungeon_completion_req)} Completion{CLN}')

        type_name = self.__class__.__name__.upper()
        if getattr(self, 'stars', None) is not None:
            type_name = f'DUNGEON {type_name}'
        info += f'\n{color}{self.rarity.upper()} {type_name}{CLN}'
        return info.replace('\n\n', '\n')

    cls.info = info

    ITEM_OBJS.append(cls)

    return cls


class ItemType:
    pass


@ item_type
class Item(ItemType):
    name: str
    count: int = 1
    # common | uncommon | rare | epic | legendary |
    # mythic | supreme | special | very_special
    rarity: str = 'common'


@ item_type
class Empty(ItemType):
    pass


@ item_type
class Pickaxe(ItemType):
    name: str
    rarity: str
    breaking_power: int
    mining_speed: int
    modifier: Optional[str] = None
    enchantments: Dict[str, int] = {}


@ item_type
class Axe(ItemType):
    name: str
    rarity: str
    tool_speed: int
    modifier: Optional[str] = None
    enchantments: Dict[str, int] = {}


@ item_type
class Sword(ItemType):
    name: str
    rarity: str
    damage: int
    modifier: Optional[str] = None
    enchantments: Dict[str, int] = {}
    stars: Optional[int] = None
    combat_skill_req: Optional[int] = None
    dungeon_skill_req: Optional[int] = None
    dungeon_completion_req: Optional[int] = None


@ item_type
class Bow(ItemType):
    name: str
    rarity: str
    damage: int
    modifier: Optional[str] = None
    enchantments: Dict[str, int] = {}
    stars: Optional[int] = None
    combat_skill_req: Optional[int] = None
    dungeon_skill_req: Optional[int] = None
    dungeon_completion_req: Optional[int] = None


@ item_type
class Armor(ItemType):
    name: str
    rarity: str
    # helmet | chestplate | leggings | boots
    part: str
    modifier: Optional[str] = None
    enchantments: Dict[str, int] = {}
    stars: Optional[int] = None
    combat_skill_req: Optional[int] = None
    dungeon_skill_req: Optional[int] = None


@ item_type
class Potion(ItemType):
    name: str
    rarity: str
    potion: str
    duration: int
    level: int


@ item_type
class Pet(ItemType):
    name: str
    rarity: str
    active: bool = False
    exp: float = 0.0
    candy_used: int = 0


class Resource:
    def type(self):
        return type(self).__name__


@ item_type
class Mineral(Resource):
    name: str
    drop: str
    amount: int = 1
    breaking_power: int = 0
    exp: Number = 1
    hardness: int = 2
    mining_exp: Number = 1


@ item_type
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
