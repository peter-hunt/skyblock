from math import ceil

from ..constant.color import GOLD, DARK_GRAY, GREEN, AQUA, YELLOW
from ..function.io import gray, red, green, yellow
from ..function.util import display_int
from ..item.item import get_item, get_stack_size
from ..item.object import (
    ItemType, Item, Empty, Bow, Sword, Armor, Axe, Hoe, Pickaxe, Pet,
)

__all__ = ['profile_item']


def profile_item(cls):
    def clearstash(self, /):
        self.stash.clear()
        green('You have cleared your stash!')

    cls.clearstash = clearstash

    def collect(self, name: str, amount: int, /):
        if name not in self.collection:
            self.collection[name] = 0
        self.collection[name] += amount

    cls.collect = collect

    def merge(self, index_1: int, index_2: int, /):
        item_from = self.inventory[index_1]
        item_to = self.inventory[index_2]
        if not hasattr(item_from, 'count') or not hasattr(item_to, 'count'):
            red('Cannot merge unstackable items.')
            return
        if item_from.name != item_to.name:
            red('Cannot merge different items.')
            return

        item_type = get_item(item_from.name)
        if item_to.count == item_type.count:
            yellow('Target item is already full as a stack.')
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
            red('Your stash is already empty!')
            return
        stash = [item.copy() for item in self.stash]
        self.stash.clear()
        for item in stash:
            self.recieve_item(item)

    cls.pickupstash = pickupstash

    def put_stash(self, item: ItemType, count: int, /):
        if isinstance(item, Item):
            for index, slot in enumerate(self.stash):
                if not isinstance(slot, Item):
                    continue
                if slot.name != item.name or slot.rarity != item.rarity:
                    continue
                self.stash[index].count += count
                break
        else:
            for _ in range(count):
                self.stash.append(item)

        materials = sum(getattr(item, 'count', 1) for item in self.stash)
        items = 0
        for item in self.stash:
            stack_count = get_stack_size(item.name)
            items += ceil(getattr(item, 'count', 1) / stack_count)
        yellow(f'You have {GREEN}{display_int(materials)} materials{YELLOW}'
               f' totalling {AQUA}{display_int(items)} items{YELLOW}'
               f' stashed away!!')
        yellow(f'Use {GOLD}`pickupstash`{YELLOW} to pick it all up!')

    cls.put_stash = put_stash

    def recieve_item(self, item: ItemType, count: int = 1,
                     /, *, log: bool = True):
        item_copy = item.copy()
        stack_count = get_stack_size(item_copy.name)
        counter = count

        for index, slot in enumerate(self.inventory):
            if isinstance(slot, Empty):
                delta = min(counter, stack_count)
                if stack_count != 1:
                    item_copy.count = delta
                self.inventory[index] = item_copy
                counter -= delta
            elif not isinstance(slot, Item) or not isinstance(item, Item):
                continue
            elif slot.name != item.name or slot.rarity != item.rarity:
                continue
            else:
                delta = min(counter, stack_count - slot.count)
                counter -= delta
                self.inventory[index].count += delta
            if counter == 0:
                break
        else:
            self.put_stash(item_copy, counter)
            return

        if log:
            if hasattr(item_copy, 'count') and item_copy.count != 1:
                item_copy.count = 1
            count_str = ('' if count <= 1
                         else f' {DARK_GRAY}x {display_int(count)}')
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
                    return

    cls.remove_item = remove_item

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

    def split(self, index_1: int, index_2: int, amount: int, /):
        item_1 = self.inventory[index_1]
        item_2 = self.inventory[index_2]

        if (not hasattr(item_1, 'count')
                or isinstance(item_1, (Bow, Sword, Armor,
                                       Axe, Hoe, Pickaxe, Pet))):
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
