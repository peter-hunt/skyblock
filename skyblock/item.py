from dataclasses import dataclass, field
from typing import Any, Dict, Optional


class Item:
    # common | uncommon | rare | epic | legendary |
    # mythic | supreme | special | very_special
    def __init__(self, name: str, count: int, rarity: str):
        self.name = name
        self.count = count
        self.rarity = rarity

    def to_obj(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'count': self.count,
            'rarity': self.rarity,
            'type': 'item',
        }

    @classmethod
    def from_obj(cls, obj: Dict[str, Any]):
        return cls(obj['name'], obj['count'], obj['rarity'])


class Empty(Item):
    def __init__(self):
        pass

    def to_obj(self) -> Dict[str, Any]:
        return {'type': 'empty'}


class Tool(Item):
    def __init__(self, name: str, rarity: str,
                 modifier: Optional[str] = None,
                 enchantments: Dict[str, int] = {}):
        self.name = name
        self.rarity = rarity
        self.modifier = modifier
        self.enchantments = enchantments


class Pickaxe(Tool):
    def __init__(self, name: str, rarity: str, breaking_power: int,
                 mining_speed: int, modifier: Optional[str] = None,
                 enchantments: Dict[str, int] = {}):
        self.name = name
        self.rarity = rarity
        self.breaking_power = breaking_power
        self.mining_speed = mining_speed
        self.modifier = modifier
        self.enchantments = enchantments

    def to_obj(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'rarity': self.rarity,
            'breaking_power': self.breaking_power,
            'mining_speed': self.mining_speed,
            'modifier': self.modifier,
            'enchantments': self.enchantments,
            'type': 'pickaxe',
        }

    @classmethod
    def from_obj(cls, obj: Dict[str, Any]):
        return cls(obj['name'], obj['rarity'],
                   obj['breaking_power'], obj['mining_speed'],
                   obj.get('modifier', None),
                   obj.get('enchantments', {}))


class Weapon(Item):
    def __init__(self, name: str, rarity: str, damage: int,
                 modifier: Optional[str] = None,
                 enchantments: Dict[str, int] = {},
                 dungeon_stars: Optional[int] = None,
                 combat_skill_req: Optional[int] = None,
                 dungeon_skill_req: Optional[int] = None):
        self.name = name
        self.rarity = rarity
        self.damage = damage
        self.modifier = modifier
        self.enchantments = enchantments
        self.dungeon_stars = dungeon_stars
        self.combat_skill_req = combat_skill_req
        self.dungeon_skill_req = dungeon_skill_req

    def to_obj(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'rarity': self.rarity,
            'damage': self.damage,
            'modifier': self.modifier,
            'enchantments': self.enchantments,
            'dungeon_stars': self.dungeon_stars,
            'combat_skill_req': self.combat_skill_req,
            'dungeon_skill_req': self.dungeon_skill_req,
            'type': 'weapon',
        }

    @classmethod
    def from_obj(cls, obj: Dict[str, Any]):
        return cls(obj['name'], obj['rarity'], obj['damage'],
                   obj.get('modifier', None),
                   obj.get('enchantments', {}),
                   obj.get('dungeon_stars', None),
                   obj.get('combat_skill_req', None),
                   obj.get('dungeon_skill_req', None))


class Armor(Item):
    # helmet | chestplate | leggings | boots
    def __init__(self, name: str, rarity: str, part: str,
                 modifier: Optional[str] = None,
                 enchantments: Dict[str, int] = {},
                 dungeon_stars: Optional[int] = None,
                 combat_skill_req: Optional[int] = None,
                 dungeon_skill_req: Optional[int] = None):
        self.name = name
        self.rarity = rarity
        self.part = part
        self.modifier = modifier
        self.enchantments = enchantments
        self.dungeon_stars = dungeon_stars
        self.combat_skill_req = combat_skill_req
        self.dungeon_skill_req = dungeon_skill_req

    def to_obj(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'rarity': self.rarity,
            'modifier': self.modifier,
            'enchantments': self.enchantments,
            'dungeon_stars': self.dungeon_stars,
            'combat_skill_req': self.combat_skill_req,
            'dungeon_skill_req': self.dungeon_skill_req,
            'type': 'armor',
        }

    @classmethod
    def from_obj(cls, obj: Dict[str, Any]):
        return cls(obj['name'], obj['rarity'],
                   obj.get('modifier', None),
                   obj.get('enchantments', {}),
                   obj.get('dungeon_stars', None),
                   obj.get('combat_skill_req', None),
                   obj.get('dungeon_skill_req', None))


class Potion(Item):
    def __init__(self, name: str, rarity: str,
                 potion: str, duration: int, level: int):
        self.name = name
        self.rarity = rarity
        self.potion = potion
        self.duration = duration
        self.level = level

    def to_obj(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'rarity': self.rarity,
            'potion': self.potion,
            'duration': self.duration,
            'level': self.level,
            'type': 'potion',
        }

    @classmethod
    def from_obj(cls, obj: Dict[str, Any]):
        return cls(obj['name'], obj['rarity'], obj['potion'],
                   obj['duration'], obj['level'])


class Pet:
    def __init__(self, name: str, rarity: str,
                 active: bool = False, exp: float = 0.0, candy_used: int = 0):
        self.name = name
        self.rarity = rarity
        self.active = active
        self.exp = exp
        self.candy_used = candy_used

    def to_obj(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'rarity': self.rarity,
            'active': self.active,
            'exp': self.exp,
            'candy_used': self.candy_used,
        }

    @classmethod
    def from_obj(cls, obj: Dict[str, Any]):
        return cls(obj['name'], obj['rarity'], obj['active'],
                   obj['exp'], obj['candy_used'])


def from_obj(obj):
    if isinstance(obj, Item):
        return obj
    elif obj['type'] == 'empty':
        return Empty()
    elif obj['type'] == 'item':
        return Item.from_obj(obj)
    elif obj['type'] == 'pickaxe':
        return Pickaxe.from_obj(obj)
    elif obj['type'] == 'weapon':
        return Weapon.from_obj(obj)
    elif obj['type'] == 'armor':
        return Armor.from_obj(obj)
    elif obj['type'] == 'potion':
        return Potion.from_obj(obj)
    elif obj['type'] == 'pet':
        return Pet.from_obj(obj)
    else:
        raise ValueError(f"invalid item obj type: {obj['type']!r}")


MATERIALS = [
    # name, stack_size, rarity
    ('wheat', 64, 'common'),
    ('carrot', 64, 'common'),
    ('potato', 64, 'common'),
    ('melon', 64, 'common'),
    ('sugar_cane', 64, 'common'),
    ('pumpkin', 64, 'common'),
    ('cocoa_beans', 64, 'common'),
    ('red_mushroom', 64, 'common'),
    ('brown_mushroom', 64, 'common'),
    ('sand', 64, 'common'),
]

ITEMS = [
    Pickaxe('rookie_pickaxe', rarity='common',
            breaking_power=2, mining_speed=150),
    Pickaxe('promising_pickaxe', rarity='uncommon',
            breaking_power=3, mining_speed=190),
]
