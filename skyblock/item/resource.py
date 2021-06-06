from typing import Any

from ..function.util import get

from .object import ItemType, Crop, Mineral, Tree

__all__ = ['RESOURCES', 'get_resource']


RESOURCES = [
    Crop('wheat', drop='wheat', amount=1, farming_exp=4),
    Crop('potato', drop='potato', amount=1, farming_exp=4),
    Crop('carrot', drop='carrot', amount=1, farming_exp=4),
    Crop('melon', drop='melon', amount=(3, 7), farming_exp=4),
    Crop('pumpkin', drop='pumpkin', amount=1, farming_exp=4.5),

    Mineral('stone', drop='cobblestone', amount=1, breaking_power=0,
            hardness=1, exp=0, mining_exp=1),
    Mineral('coal_ore', drop='coal', amount=1, breaking_power=1,
            hardness=3,
            exp=1, mining_exp=5),
    Mineral('iron_ore', drop='iron_ingot', amount=1, breaking_power=2,
            hardness=3, exp=0, mining_exp=5),
    Mineral('gold_ore', drop='gold_ingot', amount=1, breaking_power=3,
            hardness=3, exp=0, mining_exp=6),

    Tree('oak', 'oak_wood',
         hardness=2, foraging_exp=6),
    Tree('birch', 'birch_wood',
         hardness=2, foraging_exp=6),
    Tree('spruce', 'spruce_wood',
         hardness=2, foraging_exp=6),
    Tree('dark_oak', 'dark_oak_wood',
         hardness=2, foraging_exp=6),
    Tree('acacia', 'acacia_wood',
         hardness=2, foraging_exp=6),
    Tree('jungle', 'jungle_wood',
         hardness=2, foraging_exp=6),
]


def get_resource(name: str, default: Any = None, **kwargs) -> ItemType:
    return get(RESOURCES, name, default, **kwargs)
