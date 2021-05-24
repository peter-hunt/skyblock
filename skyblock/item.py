from dataclasses import dataclass, field
from typing import Dict, Optional


@dataclass
class Item:
    name: str
    count: int = 1
    # common | uncommon | rare | epic | legendary |
    # mythic | supreme | special | very_special
    rarity: str = 'common'


@dataclass
class Tool:
    name: str
    rarity: str = 'common'
    modifier: Optional[str] = None
    ench: Dict[str, int] = field(default_factory=dict)


@dataclass
class Weapon:
    name: str
    damage: int = 0
    rarity: str = 'common'
    modifier: Optional[str] = None
    ench: Dict[str, int] = field(default_factory=dict)
    dungeon_item_level: Optional[int] = 0
    combat_skill_req: int = 0
    dungeon_skill_req: int = 0


@dataclass
class Armor:
    name: str
    rarity: str = 'common'
    modifier: Optional[str] = None
    ench: Dict[str, int] = field(default_factory=dict)
    dungeon_item_level: Optional[int] = 0
    combat_skill_req: int = 0
    dungeon_skill_req: int = 0


@dataclass
class Potion:
    name: str
    potion: str
    duration: int = 0
    level: int = 1
    rarity: str = 'uncommon'


@dataclass
class Pet:
    name: str
    active: bool = False
    exp: float = 0.0
    candy_used: int = 0
    rarity: str = 'common'


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
    Tool('rookie_hoe')
]
