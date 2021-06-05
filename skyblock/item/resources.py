from typing import Any

from .object import ItemType, Mineral, Tree

__all__ = ['RESOURCES', 'get_resource']


RESOURCES = [
    Mineral('stone', 'cobblestone', 1, 1, 0, 1.5, 1),
    Mineral('coal_ore', 'coal', 1, 1, 1, 3, 5),

    Tree('oak', 'oak_wood', 2, 6),
    Tree('birch', 'birch_wood', 2, 6),
    Tree('spruce', 'spruce_wood', 2, 6),
    Tree('dark_oak', 'dark_oak_wood', 2, 6),
    Tree('acacia', 'acacia_wood', 2, 6),
    Tree('jungle', 'jungle_wood', 2, 6),
]


def get_resource(name: str, default: Any = None, **kwargs) -> ItemType:
    for resource in RESOURCES:
        if resource.name == name:
            for kwarg in kwargs:
                if getattr(resource, kwarg, None) != kwargs[kwarg]:
                    break
            else:
                return resource.copy()
    return default.copy() if hasattr(default, 'copy') else default
