from typing import Any

from ..item.object import ItemType, Empty, ITEM_OBJS
from ..item.items import ALL_ITEM

from .util import get

__all__ = ['get_item', 'load_item']


def get_item(name: str, *, default: Any = None) -> ItemType:
    return get(ALL_ITEM, name, default=default).copy()


def load_item(obj):
    if isinstance(obj, ItemType):
        return obj
    elif 'type' not in obj:
        return Empty()
    for cls in ITEM_OBJS:
        if obj['type'] == cls.__name__.lower():
            return cls.from_obj(obj)
    else:
        raise ValueError(f"invalid item obj type: {obj['type']!r}")
