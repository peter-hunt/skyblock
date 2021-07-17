from typing import Union

from ...constant.color import *
from ...constant.util import ItemPointer
from ...function.io import *
from ...function.util import format_number
from ...object.item import get_item, get_stack_size
from ...object.object import *


__all__ = [
    'clearstash', 'get_active_pet', 'has_item', 'merge', 'pickupstash',
    'put_stash', 'recieve_item', 'remove_item', 'split',
]


def clearstash(self, /):
    self.stash.clear()
    green('You have cleared your stash!')


def get_active_pet(self, /) -> Union[Pet, Empty]:
    for pet in self.pets:
        if pet.active:
            return pet
    return Empty()


def has_item(self, pointer: ItemPointer, /):
    counter = 0

    for item in self.inventory:
        if not hasattr(item, 'name') or item.name != pointer['name']:
            continue
        for key in pointer:
            if key in {'name', 'count'}:
                continue
            if (not hasattr(item, key) or getattr(item, key) != pointer[key]):
                break
        else:
            counter += getattr(item, 'count', 1)
            if counter >= pointer.get('count', 1):
                return True

    return False


def merge(self, index_1: int, index_2: int, /):
    item_from = self.inventory[index_1]
    item_to = self.inventory[index_2]

    if isinstance(item_from, Empty) or isinstance(item_from, Empty):
        red('Cannot merge Empty.')
        yellow('Use `move` instead.')
        return
    if not hasattr(item_from, 'count') or not hasattr(item_to, 'count'):
        red('Cannot merge unstackable items.')
        return
    if item_from.name != item_to.name:
        red('Cannot merge different items.')
        return
    if len(getattr(item_from, 'enchantments', {})) != 0:
        red('Cannot merge enchanted items.')
        return
    if len(getattr(item_to, 'enchantments', {})) != 0:
        red('Cannot merge enchanted items.')
        return

    item_type = get_item(item_from.name)
    if item_to.count == item_type.count:
        red('Target item is already full as a stack.')
        return

    delta = min(item_from.count, item_type.count - item_to.count)
    self.inventory[index_1].count -= delta
    if self.inventory[index_1].count == 0:
        self.inventory[index_1] = Empty()
    self.inventory[index_2].count += delta

    item_type.count = 1
    green(f'Merged {item_type.display()}')


def pickupstash(self, /):
    if len(self.stash) == 0:
        red("Your stash isn't holding any item!")
        return

    stash = [pointer.copy() for pointer in self.stash]
    self.stash = []
    for pointer in stash:
        self.recieve_pointer(pointer)


def put_stash(self, pointer: ItemPointer, /):
    name = pointer['name']
    count = pointer.get('count', 1)
    kwargs = {key: pointer[key] for key in pointer
              if key not in {'count', 'name'}}
    item = get_item(name, **kwargs)
    stack_count = get_stack_size(name)

    if stack_count != 1:
        for index, slot in enumerate(self.stash):
            if not isinstance(slot, Item):
                continue
            if slot.name != name:
                continue
            if getattr(slot, 'rarity', '') != pointer.get('rarity', ''):
                continue
            self.stash[index].count += count
            break
        else:
            item_copy = get_item(name, **kwargs)
            item_copy.count = count
            self.stash.append(item_copy)
    else:
        for _ in range(count):
            self.stash.append(item)

    red("An item didn't fit in your inventory and was added to your"
        " item stash! Use `pickupstash` to get it back!")


def recieve_item(self, pointer: ItemPointer, /):
    stack_count = get_stack_size(pointer['name'])
    count = pointer.get('count', 1)
    counter = count
    name = pointer['name']
    kwargs = {key: pointer[key] for key in pointer
              if key not in {'name', 'count'}}

    for index, slot in enumerate(self.inventory):
        if isinstance(slot, Empty):
            delta = min(counter, stack_count)
            item = get_item(name, **kwargs)
            item.count = delta
            self.inventory[index] = item
            counter -= delta

        elif (name != slot.name or
              kwargs.get('rarity', '') != getattr(slot, 'rarity', '')):
            continue

        elif len(kwargs.get('enchantments', {})) != 0:
            continue

        elif slot.count < stack_count:
            delta = min(counter, stack_count - slot.count)
            counter -= delta
            self.inventory[index].count += delta

        if counter == 0:
            break
    else:
        item = get_item(name, **kwargs)
        item.count = counter
        self.put_stash(item, counter)
        return

    item = get_item(name, **kwargs)
    item.count = counter
    if getattr(item, 'count', 1) != 1:
        item.count = 1
    count_str = '' if count <= 1 else f' {DARK_GRAY}x {format_number(count)}'
    gray(f'+ {item.display()}{count_str}')


def remove_item(self, pointer: ItemPointer, /):
    name = pointer['name']
    count = pointer.get('count', 1)
    counter = count
    kwargs = {key: pointer[key] for key in pointer
              if key not in {'name', 'count'}}

    for index, item in enumerate(self.inventory):
        if not hasattr(item, 'name') or item.name != name:
            continue
        for key in kwargs:
            if (not hasattr(item, key)
                    or getattr(item, key) != kwargs[key]):
                break
        else:
            if not hasattr(item, 'count'):
                counter -= 1
                self.inventory[index] = Empty()
            else:
                delta = min(counter, item.count)
                if delta == item.count:
                    self.inventory[index] = Empty()
                else:
                    self.inventory[index].count -= delta
                counter -= delta

            if counter == 0:
                break

    item = get_item(name, **kwargs)
    if getattr(item, 'count', 1) != 1:
        item.count = 1
    count_str = '' if count <= 1 else f' {DARK_GRAY}x {format_number(count)}'
    gray(f'- {item.display()}{count_str}')


def split(self, index_1: int, index_2: int, amount: int, /):
    item_1 = self.inventory[index_1]
    item_2 = self.inventory[index_2]

    stack_size = get_stack_size(item_1.name)

    if stack_size == 1:
        red('Cannot split unstackable items.')
        return

    if item_1.count < amount:
        red('Cannot split more than the original amount.')
        return

    if isinstance(item_2, Empty):
        self.inventory[index_1].count -= amount
        self.inventory[index_2] = item_1.copy()
        self.inventory[index_2].count = amount
        gray(f'Splitted {amount} item from '
             f'slot {index_1 + 1} to slot {index_2 + 1}.')
        return

    if item_1.name != item_2.name:
        red('Cannot split to a slot with different item.')
        return

    item_type = get_item(item_1.name)
    if item_2.count == item_type.count:
        red('Targeted slot is already full as a stack.')
        return

    delta = min(amount, item_type.count - item_2.count)
    if amount > delta:
        yellow(f'Splitting {delta} istead of {amount} item.')

    self.inventory[index_1].count -= delta
    self.inventory[index_2].count += delta
    gray(f'Splitted {delta} item from '
         f'slot {index_1 + 1} to slot {index_2 + 1}.')


item_functions = {
    name: globals()[name] for name in __all__
}
