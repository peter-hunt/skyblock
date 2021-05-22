from dataclasses import dataclass


@dataclass
class Item:
    name: str
    damage: int = 0
