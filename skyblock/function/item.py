from ..item.object import ItemType, Empty, OBJECTS

__all__ = ['load_item']


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
