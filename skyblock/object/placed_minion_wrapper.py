from ..constant.colors import *
from ..constant.util import ItemPointer
from ..function.io import *
from ..function.util import format_name, format_roman

from .items import get_item, get_stack_size
from .object import *


__all__ = ['placed_minion_type']


def placed_minion_type(cls: type, /) -> type:
    anno = getattr(cls, '__annotations__', {})
    default = {}
    for name in anno:
        if hasattr(cls, name):
            default[name] = getattr(cls, name)

    init_str = 'lambda self'
    for key in anno:
        if key in default:
            init_str += f', {key}={default[key]!r}'
        else:
            init_str += f', {key}'

    init_str += ': ('
    for key in anno:
        init_str += f'setattr(self, {key!r}, {key}), '
    init_str += 'None,)[-1]'

    cls.__init__ = eval(init_str)

    def to_obj(self, /) -> dict[str, any]:
        result = {}
        result['name'] = self.name
        result['tier'] = self.tier
        result['cooldown'] = self.cooldown
        result['last_action'] = self.last_action
        result['inventory'] = [obj.to_obj() for obj in self.inventory]
        return result

    cls.to_obj = to_obj

    @classmethod
    def load(cls, obj: dict[str, any], /):
        inventory = [load_item(item) for item in obj['inventory']]
        return cls(obj['name'], obj['tier'],
                   obj['cooldown'], obj['last_action'], inventory)

    cls.load = load

    def display(self, /):
        return f'{BLUE}{format_name(self.name)} {format_roman(self.tier)}'

    cls.display = display

    def recieve_item(self, pointer: ItemPointer, /):
        stack_count = get_stack_size(pointer['name'])
        count = pointer.get('count', 1)
        counter = count
        name = pointer['name']

        for index, slot in enumerate(self.inventory):
            if isinstance(slot, Empty):
                delta = min(counter, stack_count)
                item = get_item(name)
                item.count = delta
                self.inventory[index] = item
                counter -= delta

            elif name != slot.name:
                continue

            elif slot.count < stack_count:
                delta = min(counter, stack_count - slot.count)
                counter -= delta
                self.inventory[index].count += delta

            if counter == 0:
                break

    cls.recieve_item = recieve_item

    return cls
