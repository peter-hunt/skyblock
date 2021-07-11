from random import choice

from ....constant.color import GOLD, GREEN
from ....constant.reforging import (
    ARMOR_REFORGES, BOW_REFORGES, MELEE_REFORGES, REFORGE_COST,
)
from ....function.io import gray, dark_gray, green, red
from ....function.util import checkpoint, format_number
from ....object.object import Armor, Bow, Sword, FishingRod

__all__ = ['reforge']


@checkpoint
def reforge(player, /):
    while True:
        green('Please enter the index of item to reforge.')
        cmd = input(']> ').split()

        if len(cmd) != 1:
            red('Invalid format. Please try again.')
            continue

        index = player.parse_index(cmd[0])
        if index is None:
            continue

        item = player.inventory[index]
        if isinstance(item, Armor):
            modifiers = ARMOR_REFORGES
        elif isinstance(item, Bow):
            modifiers = BOW_REFORGES
        elif isinstance(item, (Sword, FishingRod)):
            modifiers = MELEE_REFORGES
        else:
            red('This item is not reforgable!')
            continue

        break

    cost = REFORGE_COST['curelm'.index(item.rarity[0])]

    while True:
        original_display = item.display()
        gray(f'{original_display}')
        gray(f'Cost:\n{GOLD}{format_number(cost)} Coins')
        dark_gray('Press enter to reforge and type anything to exit.')
        cmd = input(']> ').strip()
        if cmd != '':
            gray('Ended.')
            break

        if player.purse < cost:
            red("You don't have enough coins to do that!")
            break

        avaliable_modifiers = {*modifiers} - {item.modifier}
        item.modifier = choice([*avaliable_modifiers])
        player.inventory[index] = item
        player.purse -= cost
        current_display = item.display()

        green(f'You reforged your {original_display}{GREEN} into a'
              f' {current_display}{GREEN}!')
