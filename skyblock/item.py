from typing import Any, Dict, Optional

from .item_wrapper import item_type
from .function import Number, get

__all__ = [
    'ItemType', 'from_obj',
    'Item', 'Empty',
    'Pickaxe', 'Axe', 'Sword', 'Bow', 'Armor',
    'Potion', 'Pet', 'Resource', 'Mineral', 'Tree',
    'COLLECTIONS', 'MINERALS', 'TREES', 'RESOURCES',
    'WEAPONS', 'TOOLS', 'ALL_ITEM', 'SELL_PRICE',
]

ITEM_OBJS = []


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


@item_type
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


@item_type
class Axe(ItemType):
    name: str
    rarity: str
    tool_speed: int
    modifier: Optional[str] = None
    enchantments: Dict[str, int] = {}


@item_type
class Pickaxe(ItemType):
    name: str
    rarity: str
    breaking_power: int
    mining_speed: int
    modifier: Optional[str] = None
    enchantments: Dict[str, int] = {}


@item_type
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
class Tree(Resource):
    name: str
    drop: str
    hardness: int = 2
    foraging_exp: Number = 1


ITEM_OBJS = [
    Item, Empty, Sword, Bow, Axe, Pickaxe, Armor,
    Potion, Pet, Mineral, Tree,
]


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
    Tree('oak', 'oak_wood', 2, 6),
    Tree('birch', 'birch_wood', 2, 6),
    Tree('spruce', 'spruce_wood', 2, 6),
    Tree('dark_oak', 'dark_oak_wood', 2, 6),
    Tree('acacia', 'acacia_wood', 2, 6),
    Tree('jungle', 'jungle_wood', 2, 6),
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
