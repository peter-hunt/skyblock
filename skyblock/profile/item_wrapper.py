from math import ceil
from typing import Union

from ..constant.color import DARK_GRAY, WHITE
from ..function.io import gray, red, green, yellow
from ..function.util import display_int, display_name, includes
from ..object.item import ITEMS, get_item, get_stack_size, validify_item
from ..object.object import ItemType, Item, Empty, Pet


__all__ = ['profile_item_wrapper']


def profile_item_wrapper(cls):
    def clearstash(self, /):
        self.stash.clear()
        green('You have cleared your stash!')

    cls.clearstash = clearstash

    def get_active_pet(self, /) -> Union[Pet, Empty]:
        for pet in self.pets:
            if pet.active:
                return pet
        return Empty()

    cls.get_active_pet = get_active_pet

    def has_item(self, name: str, count: int = 1, /, **kwargs):
        counter = 0

        for _item in self.inventory:
            if not hasattr(_item, 'name') or _item.name != name:
                continue
            for key in kwargs:
                if (not hasattr(_item, key)
                        or getattr(_item, key) != kwargs[key]):
                    break
            else:
                counter += getattr(_item, 'count', 1)
                if counter >= count:
                    return True

        return False

    cls.has_item = has_item

    def merge(self, index_1: int, index_2: int, /):
        item_from = self.inventory[index_1]
        item_to = self.inventory[index_2]
        if not hasattr(item_from, 'count') or not hasattr(item_to, 'count'):
            red('Cannot merge unstackable items.')
            return
        if item_from.name != item_to.name:
            red('Cannot merge different items.')
            return
        if getattr(item_from, 'enchantments', {}):
            red('Cannot merge enchanted items.')
            return
        if getattr(item_to, 'enchantments', {}):
            red('Cannot merge enchanted items.')
            return

        item_type = get_item(item_from.name)
        if item_to.count == item_type.count:
            red('Target item is already full as a stack.')
            return

        delta = max(item_from.count, item_to.count - item_type.count)
        self.inventory[index_1].count -= delta
        if self.inventory[index_1].count == 0:
            self.inventory[index_1] = Empty()
        self.inventory[index_2].count += delta

        green(f'Merged {item_type.display()}')

    cls.merge = merge

    def pickupstash(self, /):
        if len(self.stash) == 0:
            red("Your stash isn't holding any item!")
            return
        stash = [item.copy() for item in self.stash]
        self.stash = []
        for item in stash:
            self.recieve_item(item, getattr(item, 'count', 1))

    cls.pickupstash = pickupstash

    def put_stash(self, item: ItemType, count: int, /):
        stack_count = get_stack_size(item.name)

        if stack_count != 0:
            for index, slot in enumerate(self.stash):
                if not isinstance(slot, Item):
                    continue
                if slot.name != item.name or slot.rarity != item.rarity:
                    continue
                self.stash[index].count += count
                break
            else:
                item_copy = item.copy()
                item_copy.count = count
                self.stash.append(item_copy)
        else:
            for _ in range(count):
                self.stash.append(item)

        materials = sum(getattr(item, 'count', 1) for item in self.stash)
        items = 0
        for item in self.stash:
            stack_count = get_stack_size(item.name)
            items += ceil(getattr(item, 'count', 1) / stack_count)
        red("An item didn't fit in your inventory and was added to your item\n"
            " stash! Use `pickupstash` to get it back!")

    cls.put_stash = put_stash

    def recieve_item(self, item: ItemType, count: int = 1, /):
        if isinstance(item, Empty):
            return

        item_copy = validify_item(item)
        stack_count = get_stack_size(item.name)
        counter = count

        for index, slot in enumerate(self.inventory):
            if isinstance(slot, Empty):
                delta = min(counter, stack_count)
                if stack_count != 1:
                    item_copy.count = delta
                self.inventory[index] = item_copy.copy()
                counter -= delta

            elif not isinstance(slot, Item) or not isinstance(item, Item):
                continue

            elif (item.name != slot.name or
                  getattr(item, 'rarity', '') != getattr(slot, 'rarity', '')):
                continue

            elif slot.count < stack_count:
                delta = min(counter, stack_count - slot.count)
                counter -= delta
                self.inventory[index].count += delta

            if counter == 0:
                break
        else:
            item_copy.count = 1
            self.put_stash(item_copy, counter)
            return

        if getattr(item_copy, 'count', 1) != 1:
            item_copy.count = 1
        count_str = ('' if count <= 1 else
                     f' {DARK_GRAY}x {display_int(count)}')
        gray(f'+ {item_copy.display()}{count_str}')

    cls.recieve_item = recieve_item

    def remove_item(self, name: str, count: int = 1, /, **kwargs):
        counter = count

        for index, _item in enumerate(self.inventory):
            if not hasattr(_item, 'name') or _item.name != name:
                continue
            for key in kwargs:
                if (not hasattr(_item, key)
                        or getattr(_item, key) != kwargs[key]):
                    break
            else:
                if not hasattr(_item, 'count'):
                    counter -= 1
                    self.inventory[index] = Empty()
                else:
                    delta = min(counter, _item.count)
                    if delta == _item.count:
                        self.inventory[index] = Empty()
                    else:
                        self.inventory[index].count -= delta
                    counter -= delta

                if counter == 0:
                    break

        count_str = ('' if count <= 1
                     else f' {DARK_GRAY}x {display_int(count)}')
        if includes(ITEMS, name):
            item = get_item(name)
            if getattr(item, 'count', 1) != 1:
                item.count = 1
            gray(f'- {item.display()}{count_str}')
        else:
            gray(f'- {WHITE}{display_name(name)}{count_str}')

    cls.remove_item = remove_item

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
            self.inventory[index_2] = item_1
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

    cls.split = split

    return cls
