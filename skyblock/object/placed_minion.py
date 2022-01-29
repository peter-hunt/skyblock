from ..constant.util import Number

from .placed_minion_wrapper import placed_minion_type


__all__ = ['PlacedMinion', 'load_minion']


@placed_minion_type
class PlacedMinion:
    name: str
    tier: str
    cooldown: Number
    last_action: int
    inventory: list


def load_minion(obj, /):
    if obj.__class__.__name__ in {'Empty', 'PlacedMinion'}:
        return obj
    elif isinstance(obj, dict) and len(obj) == 0:
        return {}
    else:
        return PlacedMinion.load(obj)

