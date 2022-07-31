from typing import Iterator

from ..constant.util import Amount, ItemPointer, Number

from .item_wrapper import item_type
from .other_wrapper import *


__all__ = [
    'ItemType', 'Item', 'Empty',
    'Accessory', 'EnchantedBook', 'ReforgeStone', 'TravelScroll',
    'Bow', 'Sword',
    'Axe', 'Pickaxe', 'Drill', 'Hoe', 'FishingRod', 'Armor', 'Pet', 'Minion',
    'Resource',
    'Crop', 'Mineral', 'Log', 'Mob',
    'Recipe', 'RecipeGroup', 'Collection',
    'load_item',
]


class ItemType:
    pass


@item_type
class Item(ItemType):
    name: str
    count: int = 1
    # common | uncommon | rare | epic | legendary |
    # mythic | divine | special | very_special
    rarity: str = 'common'

    abilities: list[str] = []


@item_type
class Empty(ItemType):
    def __repr__(self):
        return '{}'


@item_type
class Accessory(ItemType):
    name: str
    rarity: str = 'common'
    modifier: str | None = None

    slayer_req: tuple[str, int] | None = None

    abilities: list[str] = []


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
    true_defense: int = 0
    ferocity: int = 0
    sea_creature_chance: int = 0
    pristine: int = 0

    modifier: str | None = None
    enchantments: dict[str, int] = {}
    hot_potato: int = 0
    stars: int | None = None
    collection_req: tuple[str, int] | None = None
    combat_skill_req: int | None = None
    dungeon_skill_req: int | None = None
    dungeon_completion_req: int | None = None

    abilities: list[str] = []


@item_type
class Axe(ItemType):
    name: str
    rarity: str
    tool_speed: int
    modifier: str | None = None
    enchantments: dict[str, int] = {}

    abilities: list[str] = []


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

    modifier: str | None = None
    enchantments: dict[str, int] = {}
    hot_potato: int = 0
    stars: int | None = None
    combat_skill_req: int | None = None
    dungeon_skill_req: int | None = None
    dungeon_completion_req: int | None = None

    abilities: list[str] = []


@item_type
class Drill(ItemType):
    name: str
    rarity: str

    breaking_power: int
    mining_speed: int
    mining_fortune: int = 0
    pristine: Number = 0

    gemstone_mining_speed: int = 0
    gemstone_mining_fortune: int = 0

    damage: int = 0
    defense: int = 0
    intelligence: int = 0

    modifier: str | None = None
    enchantments: dict[str, int] = {}

    abilities: list[str] = []


@enchanted_book_type
@item_type
class EnchantedBook(ItemType):
    enchantments: dict[str, int] = {}
    name: str = 'enchanted_book'
    rarity: str = 'common'


@item_type
class FishingRod(ItemType):
    name: str
    rarity: str

    damage: int = 0
    strength: int = 0
    ferocity: int = 0

    fishing_speed: int = 0
    sea_creature_chance: int = 0

    modifier: str | None = None
    enchantments: dict[str, int] = {}
    expertise_count: int = 0
    hot_potato: int = 0
    stars: int | None = None
    fishing_skill_req: int | None = None

    abilities: list[str] = []


@item_type
class Hoe(ItemType):
    name: str
    rarity: str
    modifier: str | None = None
    enchantments: dict[str, int] = {}
    cultivating_count: int = 0


@item_type
class Minion(ItemType):
    name: str
    tier: str
    cooldown: Number
    slots: int


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
    damage: int = 0
    magic_find: int = 0
    attack_speed: int = 0
    ferocity: int = 0
    sea_creature_chance: int = 0

    abilities: list = []


@item_type
class Pickaxe(ItemType):
    name: str
    rarity: str

    breaking_power: int
    mining_speed: int
    pristine: Number = 0

    damage: int = 0
    defense: int = 0

    modifier: str | None = None
    enchantments: dict[str, int] = {}
    compact_count: int = 0

    abilities: list[str] = []


@item_type
class ReforgeStone(ItemType):
    name: str
    modifier: str | None = None
    category: str | None = None
    rarity: str = 'common'
    cost: tuple[int] = (0, 0, 0, 0, 0, 0)

    mining_skill_req: int | None = None


@item_type
class Sword(ItemType):
    name: str
    rarity: str
    count: int = 1

    damage: int = 0

    strength: int = 0
    crit_chance: int = 0
    crit_damage: int = 0
    attack_speed: int = 0

    defense: int = 0
    intelligence: int = 0
    true_defense: int = 0
    ferocity: int = 0
    speed: int = 0

    modifier: str | None = None
    enchantments: dict[str, int] = {}
    hot_potato: int = 0
    stars: int | None = None
    combat_skill_req: int | None = None
    slayer_req: tuple[str, int] | None = None
    dungeon_skill_req: int | None = None
    dungeon_completion_req: int | None = None

    kill_count: int = 0

    abilities: list[str] = []


@item_type
class TravelScroll(ItemType):
    name: str
    island: str
    zone: str | None = None
    rarity: str = 'rare'


OBJECT_NAMES = {
    'item': Item,
    'empty': Empty,
    'accessory': Accessory,
    'armor': Armor,
    'axe': Axe,
    'bow': Bow,
    'drill': Drill,
    'enchanted_book': EnchantedBook,
    'fishing_rod': FishingRod,
    'hoe': Hoe,
    'minion': Minion,
    'pet': Pet,
    'pickaxe': Pickaxe,
    'reforge_stone': ReforgeStone,
    'sword': Sword,
    'travel_scroll': TravelScroll,
}


class Resource:
    def type(self):
        return type(self).__name__


@resource_type
class Crop(Resource):
    name: str
    amount: int = 1
    farming_exp: Number = 1


@resource_type
class Log(Resource):
    name: str
    hardness: int = 2
    foraging_exp: Number = 1


@resource_type
class Mineral(Resource):
    name: str
    drop: str
    amount: Amount = 1
    breaking_power: int = 0
    hardness: Number = 2
    exp: Amount = 1
    mining_exp: Number = 1
    mithril_powder: Amount = 0


@mob_type
class Mob:
    name: str
    level: int
    health: int
    defense: int = 0
    damage: int = 0
    true_damage: int = 0

    coins: int = 0
    exp: int = 0
    farming_exp: int = 0
    combat_exp: int = 0
    fishing_exp: int = 0
    drops: list[tuple[ItemPointer, Amount, str, Number]] = []


@recipe_type
class Recipe:
    name: str
    category: str
    ingredients: list[ItemPointer | int]
    result: ItemPointer
    collection_req: tuple[str, int] | None = None
    slayer_req: tuple[str, int] | None = None


@recipe_group_type
class RecipeGroup:
    name: str
    category: str
    recipes: list[str]
    collection_req: tuple[str, int] | None = None
    slayer_req: tuple[str, int] | None = None


@collection_type
class Collection:
    name: str
    category: str
    levels: list[tuple[int, str | tuple[str] | Number]]

    def __iter__(self, /) -> Iterator:
        return iter(self.levels)


def load_item(obj, /):
    if isinstance(obj, ItemType):
        return obj
    elif 'type' not in obj:
        return Empty()
    for name, cls in OBJECT_NAMES.items():
        if obj['type'] == name:
            return cls.from_obj(obj)
    else:
        raise ValueError(f"invalid item obj type: {obj['type']!r}")
