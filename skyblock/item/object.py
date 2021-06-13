from typing import Dict, List, Optional, Tuple

from ..constant.util import Amount, Number

from .wrapper import item_type, mob_type

__all__ = [
    'ItemType', 'Item', 'Empty', 'Bow', 'Sword', 'Axe', 'Pickaxe', 'Hoe',
    'Armor', 'Potion', 'Pet', 'Resource', 'Mineral', 'Tree', 'ITEM_OBJS', 'Mob',
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

    damage: int = 0
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


class Resource:
    def type(self):
        return type(self).__name__


@item_type
class Crop(Resource):
    name: str
    drop: str
    amount: int = 1
    farming_exp: Number = 1


@item_type
class Mineral(Resource):
    name: str
    drop: str
    amount: int = 1
    breaking_power: int = 0
    hardness: int = 2
    exp: Amount = 1
    mining_exp: Number = 1


@item_type
class Tree(Resource):
    name: str
    drop: str
    hardness: int = 2
    foraging_exp: Number = 1


ITEM_OBJS = [
    Item, Empty, Sword, Bow, Axe, Hoe, Pickaxe, Armor,
    Potion, Pet, Crop, Mineral, Tree,
]


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
