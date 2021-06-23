from typing import Dict, Iterator, List, Optional, Tuple, Union

from ..constant.util import Amount, Number

from .collection_wrapper import collection_type
from .item_wrapper import item_type
from .mob_wrapper import mob_type
from .recipe_wrapper import recipe_type

__all__ = [
    'ItemType', 'Item', 'Empty', 'Bow', 'Sword', 'Axe', 'Pickaxe', 'Hoe',
    'Armor', 'TravelScroll', 'Pet', 'OBJECTS',
    'Resource', 'Mineral', 'Tree', 'Mob', 'Recipe', 'Collection',
    'load_item',
]


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
    def __repr__(self):
        return '{}'


@item_type
class Bow(ItemType):
    name: str
    rarity: str
    damage: int
    count: int = 1

    strength: int = 0
    crit_chance: int = 0
    crit_damage: int = 0
    attack_speed: int = 0

    intelligence: int = 0

    modifier: Optional[str] = None
    enchantments: Dict[str, int] = {}
    hot_potato: int = 0
    stars: Optional[int] = None
    combat_skill_req: Optional[int] = None
    dungeon_skill_req: Optional[int] = None
    dungeon_completion_req: Optional[int] = None


@item_type
class Sword(ItemType):
    name: str
    rarity: str
    damage: int
    count: int = 1

    strength: int = 0
    crit_chance: int = 0
    crit_damage: int = 0
    attack_speed: int = 0

    defense: int = 0
    intelligence: int = 0
    true_denfense: int = 0
    ferocity: int = 0
    speed: int = 0

    modifier: Optional[str] = None
    enchantments: Dict[str, int] = {}
    hot_potato: int = 0
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
class Hoe(ItemType):
    name: str
    rarity: str
    modifier: Optional[str] = None
    enchantments: Dict[str, int] = {}


@item_type
class Armor(ItemType):
    name: str
    rarity: str
    # helmet | chestplate | leggings | boots
    part: str

    strength: int = 0
    crit_chance: int = 0
    crit_damage: int = 0

    health: int = 0
    defense: int = 0
    intelligence: int = 0
    speed: int = 0
    magic_find: int = 0
    mining_speed: int = 0
    mining_fortune: int = 0
    true_denfense: int = 0
    ferocity: int = 0
    sea_creature_chance: int = 0

    modifier: Optional[str] = None
    enchantments: Dict[str, int] = {}
    hot_potato: int = 0
    stars: Optional[int] = None
    combat_skill_req: Optional[int] = None
    dungeon_skill_req: Optional[int] = None
    dungeon_completion_req: Optional[int] = None


@item_type
class TravelScroll(ItemType):
    island: str
    region: Optional[str] = None
    rarity: str = 'rare'
    name: str = 'travel_scroll'


@item_type
class Pet(ItemType):
    name: str
    rarity: str
    category: str = None
    exp: float = 0.0
    candy_used: int = 0
    active: bool = False

    health: int = 0
    defense: int = 0
    speed: int = 0
    true_defense: int = 0
    intelligence: int = 0
    strength: int = 0
    crit_chance: int = 0
    crit_damage: int = 0
    magic_find: int = 0
    attack_speed: int = 0
    ferocity: int = 0

    abilities: List = []


@item_type
class Pet(ItemType):
    name: str
    rarity: str
    category: str = None
    exp: float = 0.0
    candy_used: int = 0
    active: bool = False

    health: int = 0
    defense: int = 0
    speed: int = 0
    true_defense: int = 0
    intelligence: int = 0
    strength: int = 0
    crit_chance: int = 0
    crit_damage: int = 0
    magic_find: int = 0
    attack_speed: int = 0
    ferocity: int = 0

    abilities: List = []


OBJECTS = [
    Item, Empty, Sword, Bow, Axe, Hoe, Pickaxe, Armor, TravelScroll, Pet,
]


class Resource:
    def type(self):
        return type(self).__name__


@item_type
class Crop(Resource):
    name: str
    amount: int = 1
    farming_exp: Number = 1


@item_type
class Mineral(Resource):
    name: str
    drop: str
    amount: int = 1
    breaking_power: int = 0
    hardness: Number = 2
    exp: Amount = 1
    mining_exp: Number = 1


@item_type
class Tree(Resource):
    name: str
    drop: str
    hardness: int = 2
    foraging_exp: Number = 1


@mob_type
class Mob:
    name: str
    level: int
    health: int
    damage: int
    coins: int
    combat_xp: int
    exp: int
    drops: List[Tuple[ItemType, Amount, str, Number]]


@mob_type
class Mob:
    name: str
    level: int
    health: int
    damage: int
    coins: int
    combat_xp: int
    exp: int
    drops: List[Tuple[ItemType, Amount, str, Number]]


@recipe_type
class Recipe:
    name: str
    category: str
    ingredients: List[Tuple[ItemType, Amount]]
    result: Tuple[ItemType, Amount]
    collection_req: Optional[Tuple[str, int]] = None
    # slayer_req: Optional[Tuple[str, int]] = None


@collection_type
class Collection:
    name: str
    category: str
    levels: List[Tuple[int, Union[Recipe, Tuple[Recipe], Number]]]

    def __iter__(self, /) -> Iterator:
        return iter(self.levels)


def load_item(obj):
    if isinstance(obj, ItemType):
        return obj
    elif 'type' not in obj:
        return Empty()
    for cls in OBJECTS:
        if obj['type'] == cls.__name__.lower():
            return cls.from_obj(obj)
    else:
        raise ValueError(f"invalid item obj type: {obj['type']!r}")
