from typing import Optional

from ..function.io import red
from ..function.util import get, includes

from .object import ItemType, Crop, Mineral, Wood


__all__ = ['RESOURCES', 'get_resource']

RESOURCES = [
    Crop('wheat', amount=1, farming_exp=4),
    Crop('potato', amount=1, farming_exp=4),
    Crop('carrot', amount=1, farming_exp=4),
    Crop('melon', amount=(3, 7), farming_exp=4),
    Crop('pumpkin', amount=1, farming_exp=4.5),
    Crop('cactus', amount=(5, 15), farming_exp=2),
    Crop('sugar_cane', amount=(3, 5), farming_exp=2),
    Crop('cocoa', amount=(2, 3), farming_exp=4),
    Crop('mushroom', amount=1, farming_exp=3),
    Crop('nether_wart', amount=(2, 4), farming_exp=2),

    Mineral('stone', drop='cobblestone', amount=1, breaking_power=1,
            hardness=1, exp=0, mining_exp=1),
    Mineral('gravel', drop='gravel', amount=1, breaking_power=0,
            hardness=0.6, exp=0, mining_exp=4),
    Mineral('coal_ore', drop='coal', amount=1, breaking_power=1,
            hardness=3, exp=1, mining_exp=5),
    Mineral('iron_ore', drop='iron', amount=1, breaking_power=2,
            hardness=3, exp=0, mining_exp=5),
    Mineral('gold_ore', drop='gold', amount=1, breaking_power=3,
            hardness=3, exp=0, mining_exp=6),
    Mineral('lapis_ore', drop='lapis', amount=(4, 9), breaking_power=2,
            hardness=3, exp=(2, 5), mining_exp=7),
    Mineral('redstone_ore', drop='redstone', amount=(4, 5), breaking_power=3,
            hardness=3, exp=(1, 5), mining_exp=7),
    Mineral('emerald_ore', drop='emerald', amount=1, breaking_power=3,
            hardness=3, exp=(3, 7), mining_exp=9),
    Mineral('diamond_ore', drop='diamond', amount=1, breaking_power=3,
            hardness=3, exp=(3, 7), mining_exp=10),
    Mineral('diamond_block', drop='diamond', amount=9, breaking_power=3,
            hardness=5, exp=0, mining_exp=15),
    Mineral('obsidian', drop='obsidian', amount=1, breaking_power=4,
            hardness=50, exp=0, mining_exp=20),
    Mineral('end_stone', drop='end_stone', amount=1, breaking_power=1,
            hardness=3, exp=0, mining_exp=3),
    Mineral('sand', drop='sand', amount=1, breaking_power=0,
            hardness=0.5, exp=0, mining_exp=3),

    Mineral('gray_mithril', drop='mithril', amount=1, breaking_power=4,
            hardness=30, exp=15, mining_exp=45),
    Mineral('dark_mithril', drop='mithril', amount=2, breaking_power=4,
            hardness=60, exp=30, mining_exp=45),
    Mineral('light_mithril', drop='mithril', amount=5, breaking_power=4,
            hardness=100, exp=50, mining_exp=45),
    Mineral('titanium', drop='titanium', amount=1, breaking_power=5,
            hardness=150, exp=75, mining_exp=100),
    Mineral('gold_block', drop='gold', amount=9, breaking_power=3,
            hardness=30, exp=20, mining_exp=20),

    Mineral('glowstone', drop='glowstone', amount=4, breaking_power=1,
            hardness=0.3, exp=0, mining_exp=7),
    Mineral('netherrack', drop='netherrack', amount=1, breaking_power=1,
            hardness=0.4, exp=0, mining_exp=0.5),
    Mineral('quartz_ore', drop='quartz', amount=1, breaking_power=1,
            hardness=3, exp=(2, 5), mining_exp=5),

    Wood('oak_wood', hardness=2, foraging_exp=6),
    Wood('birch_wood', hardness=2, foraging_exp=6),
    Wood('spruce_wood', hardness=2, foraging_exp=6),
    Wood('dark_oak_wood', hardness=2, foraging_exp=6),
    Wood('acacia_wood', hardness=2, foraging_exp=6),
    Wood('jungle_wood', hardness=2, foraging_exp=6),

    Wood('dandelion', hardness=0, foraging_exp=1),
    Wood('poppy', hardness=0, foraging_exp=1)]


def get_resource(name: str, **kwargs) -> Optional[ItemType]:
    if not includes(RESOURCES, name):
        red(f'Invalid resource: {name!r}')
        return
    return get(RESOURCES, name, **kwargs)
