from math import floor
from random import choice, random
from time import sleep, time
from typing import List, Optional, Tuple

from ...constant.colors import *
from ...constant.enchanting import *
from ...constant.main import INTEREST_TABLE, SELL_PRICE
from ...function.enchanting import get_enchantments
from ...function.io import *
from ...function.math import calc_exp_level, calc_exp
from ...function.minions import get_minion_cap, get_minion_cap_info
from ...function.random import random_amount, random_int
from ...function.reforging import combine_enchant
from ...function.util import (
    checkpoint, format_name, format_number, format_roman, format_short,
    format_zone, get, get_ench, includes,
)
from ...install import install_data
from ...map.islands import ISLANDS
from ...map.object import *
from ...object.items import get_item
from ...object.minions import MINION_LOOT
from ...object.object import *
from ...object.placed_minion import PlacedMinion


__all__ = [
    'add_pet', 'buy', 'claim_minion', 'combine', 'consume', 'craft',
    'despawn_pet', 'die', 'enchant', 'goto', 'place_minion', 'remove_minion',
    'remove_pet', 'sell', 'summon_pet', 'talkto_npc', 'update', 'warp',
]


def add_pet(self, index: int, /):
    item = self.inventory[index]

    if not isinstance(item, Pet):
        red('Invalid pet.')

    self.pets.append(item)
    self.inventory[index] = Empty()

    green(f'Successfully added {item.display()} {GREEN}to your pet menu!')


def buy(self, trade: Tuple, amount: int, /):
    cost = trade[0]

    if isinstance(cost, (int, float)):
        cost = [cost]

    for pointer in cost:
        if isinstance(pointer, (int, float)):
            if self.purse < pointer * amount:
                red("You don't have enough Coins!")
                return
            continue
        if not self.has_item(pointer):
            red("You don't have the required items.")
            return

    for pointer in cost:
        if isinstance(pointer, (int, float)):
            self.purse -= pointer * amount
            continue
        self.remove_item(pointer)

    good = trade[1]
    if not isinstance(good, list):
        good = [good]

    display = []

    for pointer in good:
        self.recieve_item(pointer)
        name = pointer['name']
        count = pointer.get('count', 1)
        kwargs = {key: pointer[key] for key in pointer
                  if key not in {'count', 'name'}}
        item = get_item(name, kwargs)
        if getattr(item, 'count', 1) != 1:
            item.count = 1
        count_str = '' if count == 1 else f'{GRAY} x {count}'
        display.append(f'{load_item.display()}{count_str}')

    display_str = f'{GREEN}, '.join(display)

    if len(cost) == 1 and isinstance(cost[0], (float, int)):
        green(f'You bought {display_str}{GREEN} for '
              f'{GOLD}{format_short(cost[0])} Coins{GREEN}!')
    else:
        green(f'You bought {display_str}{GREEN}!')


def claim_minion(self, slot: int, /) -> bool:
    if isinstance(self.placed_minions[slot], Empty):
        red('This slot is empty!')
        return

    items_left = []

    minion = self.placed_minions[slot]
    for index, item in enumerate(minion.inventory):
        if isinstance(item, Empty):
            continue

        pointer = item.to_obj()
        item_left = self._recieve_item(pointer)
        if len(item_left) != 0:
            items_left.append(item_left)
        self.collect(pointer['name'], pointer.get('count', 1))
        minion.inventory[index] = Empty()

    if len(items_left) != 0:
        red('Your inventory does not have enough space to add all items!')
        for pointer in items_left:
            minion.recieve_item(pointer)
    else:
        aqua(f"You claimed the {minion.display()}{AQUA}'s inventory!")
    self.placed_minions[slot] = minion


def combine(self, index_1: int, index_2: int, /):
    item_1 = self.inventory[index_1]
    item_2 = self.inventory[index_2]

    if isinstance(item_1, Empty) or isinstance(item_2, Empty):
        red('These items cannot be combined!')
        return

    if isinstance(item_1, EnchantedBook) and isinstance(item_2, EnchantedBook):
        result_enchants = combine_enchant(item_1.enchantments,
                                          item_2.enchantments)

        self.inventory[index_1] = Empty()
        self.inventory[index_2] = Empty()
        self.recieve_item({'name': 'enchanted_book',
                           'enchantments': result_enchants})

        return

    if (isinstance(item_2, (Axe, Drill, Pickaxe, Hoe,
                            Armor, Bow, Sword, FishingRod))
            and isinstance(item_1, EnchantedBook)):
        index_1, index_2 = index_2, index_1
        item_1, item_2 = item_2, item_1

    if (isinstance(item_1, (Axe, Drill, Pickaxe, Hoe,
                            Armor, Bow, Sword, FishingRod))
            and isinstance(item_2, EnchantedBook)):
        result_enchants = combine_enchant(item_1.enchantments,
                                          item_2.enchantments)
        enchant_table = get_enchantments(item_1)
        pointer = item_1.to_obj()
        pointer['enchantments'] = {
            name: value
            for name, value in result_enchants.items()
            if name in enchant_table
        }
        self.inventory[index_1] = Empty()
        self.inventory[index_2] = Empty()
        self.recieve_item(pointer)
        return

    if (isinstance(item_2, (Accessory, Armor, Bow, Sword, FishingRod))
            and isinstance(item_1, ReforgeStone)):
        index_1, index_2 = index_2, index_1
        item_1, item_2 = item_2, item_1

    if (isinstance(item_1, (Accessory, Armor, Bow, Sword, FishingRod))
            and isinstance(item_2, ReforgeStone)):
        cost = item_2.cost['curelm'.index(item_1.rarity[0])]

        combinable = True
        if item_2.category == 'accessory':
            if not isinstance(item_1, Accessory):
                combinable = False
        elif item_2.category == 'armor':
            if not isinstance(item_1, Armor):
                combinable = False
        elif item_2.category == 'bow':
            if not isinstance(item_1, Bow):
                combinable = False
        elif item_2.category == 'melee':
            if not (isinstance(item_1, (Sword, FishingRod))
                    and getattr(item_1, 'damage', 0) != 0):
                combinable = False

        if not combinable:
            red('These items cannot be combined!')
            return

        if self.purse < cost:
            red("You don't have enough Coins!")
            return

        self.purse -= cost

        pointer = item_1.to_obj()
        pointer['modifier'] = item_2.modifier
        self.inventory[index_1] = Empty()
        self.inventory[index_2] = Empty()
        gray(f'- {GOLD}{format_number(cost)} Coins')
        self.recieve_item(pointer)
        return

    if (item_1.name in {'hot_potato_book', 'fuming_potato_book'} and
            isinstance(item_2, (Armor, Bow, Sword, FishingRod))):
        index_1, index_2 = index_2, index_1
        item_1, item_2 = item_2, item_1

    if (isinstance(item_1, (Armor, Bow, Sword, FishingRod))
            and item_2.name == 'hot_potato_book'):
        if 10 <= item_1.hot_potato < 15:
            red('Error!')
            gray(f'You have already applied the maximum number of'
                 f' Hot Potato books to this item!')
            yellow(f'Use Fuming Potato Books to continue to upgrade this item.')
        elif item_1.hot_potato >= 15:
            red('Error!')
            gray('You have already applied the maximum number of'
                 ' Hot Potato books to this item!')
        else:
            pointer = item_1.to_obj()
            pointer['hot_potato'] = pointer.get('hot_potato', 0) + 1
            self.inventory[index_1] = Empty()
            self.inventory[index_2] = Empty()
            self.recieve_item(pointer)
        return

    if (isinstance(item_1, (Armor, Bow, Sword, FishingRod))
            and item_2.name == 'fuming_potato_book'):
        if item_1.hot_potato >= 15:
            red('Error!')
            gray('You have already applied the maximum number of'
                 ' Hot Potato books to this item!')
        else:
            pointer = item_1.to_obj()
            pointer['hot_potato'] = pointer.get('hot_potato', 0) + 1
            self.inventory[index_1] = Empty()
            self.inventory[index_2] = Empty()
            self.recieve_item(pointer)
        return

    red('These items cannot be combined!')
    return


def consume(self, index: int, amount: int = 1, /):
    item = self.inventory[index]

    if isinstance(item, TravelScroll):
        if [item.island, item.zone] in self.fast_travel:
            red('You already unlocked this fast travel!')
            return

        self.fast_travel.append([item.island, item.zone])
        self.inventory[index] = Empty()
        name = format_name(item.island)
        if item.zone is not None:
            name += f' {GRAY}- {AQUA}{format_name(item.zone)}'
        yellow('You consumed the scroll!')
        yellow(f'You may now fast travel to {GREEN}{name}{YELLOW}!')

    elif item.name in {'experience_bottle', 'grand_experience_bottle',
                       'tiantium_experience_bottle'}:
        if amount > item.count:
            red("You don't have enough item to do that!")
            return

        if item.name == 'experience_bottle':
            exp_amount = 8
        elif item.name == 'grand_experience_bottle':
            exp_amount = 1_500
        elif item.name == 'tiantium_experience_bottle':
            exp_amount = 250_000

        if self.has_item({'name': 'experience_artifact'}):
            exp_amount *= 1.25

        item_copy = item.copy()
        item_copy.count = amount

        gray(f'You consumed {item_copy.display()}{GRAY}!')
        self.add_exp(exp_amount * amount)

        self.inventory[index].count -= amount
        if self.inventory[index].count == 0:
            self.inventory[index] = Empty()

    else:
        red('This item is not consumable!')


def craft(self, recipes: List[Recipe], amount: int = 1, /):
    for recipe in recipes:
        if recipe.collection_req is not None:
            coll_name, lvl = recipe.collection_req
            if self.get_collection_level(coll_name) < lvl:
                red("You haven't reached the required collection yet!")
                return

        for ingr_pointer in recipe.ingredients:
            _ingr_pointer = ingr_pointer.copy()
            _ingr_pointer['count'] = ingr_pointer.get('count', 1) * amount
            if not self.has_item(_ingr_pointer):
                red("You don't have the required items!")
                return

        for ingr_pointer in recipe.ingredients:
            _ingr_pointer = ingr_pointer.copy()
            _ingr_pointer['count'] = ingr_pointer.get('count', 1) * amount
            self.remove_item(_ingr_pointer)

        result_pointer = recipe.result
        name = result_pointer['name']

        if name.endswith('_pet'):
            keep_weight = 80
            upgrade_weight = 20 + 0.2 * self.get_stat('pet_luck')
            total = keep_weight + upgrade_weight
            if random() > (keep_weight / total):
                result_pointer['rarity'] = {
                    'common': 'uncommon',
                    'uncommon': 'rare',
                    'rare': 'epic',
                    'epic': 'legendary',
                }[result_pointer['rarity']]

        _result_pointer = result_pointer.copy()
        _result_pointer['count'] = result_pointer.get('count', 1) * amount
        self.recieve_item(_result_pointer)

        if name.endswith('_minion'):
            tier = result_pointer['tier']

            minion_name = name.replace('_minion', f'_{tier}')
            if minion_name not in self.crafted_minions:
                self.crafted_minions.append(minion_name)
                self.crafted_minions.sort()

                tier_str = format_roman(tier)
                green(f"You crafted a {YELLOW}Tier {tier_str}"
                      f" {format_name(name)}{GREEN}! That's a new one!")
                cap, to_next = get_minion_cap_info(len(self.crafted_minions))
                if to_next > 0:
                    green(f' Craft {to_next} more unique Minions'
                          f' to unlock your {cap + 1}th Minion slot!')
                elif to_next == 0:
                    gold(f' You have now unlocked your {cap}th Minion slot!')
                    self.placed_minions.append(Empty())


def despawn_pet(self, /):
    for i, pet in enumerate(self.pets):
        if pet.active:
            self.pets[i].active = False
            break
    else:
        red("You don't have a pet spawned!")
        return

    green(f'You despawned your {pet.display()}{GREEN}!')


def die(self, killer: Optional[str] = None, /) -> bool:
    if self.has_item({'name': 'saving_grace'}):
        self.remove_item({'name': 'saving_grace'})
        self.island = 'hub'
        self.zone = 'village'
        green('Saving Grace has activated! '
              'You have been revived safely.')
        return False

    perc_lost = 1

    for piece in self.armor:
        if not isinstance(piece, Armor):
            continue

        ench = getattr(piece, 'enchantments', {})
        perc_lost -= ench.get('bank', 0) / 10

    for i, pet in enumerate(self.pets):
        if pet.active:
            self.pets[i].active = False
            break
    else:
        pet = None

    if pet is None:
        pass
    elif 'eternal_coins' in pet.abilities:
        perc_lost = 0

    perc_lost = max(perc_lost, 0)
    lost_coins = self.purse / 2 * perc_lost

    did_crack_piggy = False

    if self.has_item({'name': 'piggy_bank'}):
        if lost_coins >= 20_000:
            did_crack_piggy = True
            lost_coins = 0
            self.remove_item({'name': 'piggy_bank'})
            self.recieve_item({'name': 'cracked_piggy_bank'})

    did_broke_piggy = False

    if not did_crack_piggy and self.has_item({'name': 'cracked_piggy_bank'}):
        if lost_coins >= 20_000:
            did_broke_piggy = True
            lost_coins *= 0.25
            self.remove_item({'name': 'cracked_piggy_bank'})
            self.recieve_item({'name': 'broken_piggy_bank'})

    self.purse -= lost_coins

    if 'deaths' not in self.stats:
        self.stats['deaths'] = 0
    self.stats['deaths'] += 1

    if killer is not None:
        if f'deaths_{killer}' not in self.stats:
            self.stats[f'deaths_{killer}'] = 0
        self.stats[f'deaths_{killer}'] += 1

    if did_crack_piggy:
        red('You died and your piggy bank cracked!')
    elif did_broke_piggy:
        red(f'You died, lost {format_number(lost_coins)} coins'
            f' and your piggy bank broke!')
    elif 'eternal_coins' in pet.abilities:
        red('You died with eternal coins from your Phoenix pet!')
    elif perc_lost == 0:
        red('You died!')
    else:
        red(f'You died and lost {format_number(lost_coins)} coins!')
    self.zone = get(ISLANDS, self.island).spawn

    return True


@checkpoint
def enchant(self, item_index: int, /):
    enchanting_level = self.get_skill_level('enchanting')
    exp_level = calc_exp_level(self.experience)

    item = self.inventory[item_index]

    if getattr(item, 'count', 1) != 1:
        red('Cannot Enchant more than one item at once!')
        return

    enchant_table = get_enchantments(item)

    if len(enchant_table) == 0:
        red('Cannot Enchant Item!')
        gray('This item cannot be enchanted!')
        return

    avaliable = []

    all_ench = [row[0] for row in ENCHS]

    gray('Avaliable enchantments and xp level needed:')
    for name in enchant_table:
        if name not in all_ench:
            continue

        for _ench, req in ENCH_REQUIREMENTS:
            if name == _ench and req > enchanting_level:
                break
        else:
            current = item.enchantments.get(name, 0)
            xps = get_ench(name)
            if current != 0:
                current_xp = calc_exp(xps[min(current - 1, len(xps) - 1)])
            else:
                current_xp = 0
            discounted = [
                calc_exp(xp) if lvl + 1 == current else
                calc_exp(xp) - current_xp
                for lvl, xp in enumerate(xps)
            ]
            discounted_level = [calc_exp_level(xp) for xp in discounted]
            avaliable.append((name, discounted_level))

            blue(f'{len(avaliable):>2} {name}')
            if current > 0:
                xp_str = ', '.join(
                    f'{GRAY}{xp}' if lvl + 1 < current
                    else f'{RED}{xp}' if lvl + 1 == current
                    else f'{DARK_AQUA}{xp}{AQUA}➜{AQUA}{dxp}'
                    if xp != dxp else f'{AQUA}{xp}'
                    for lvl, (xp, dxp) in enumerate(
                        zip(xps, discounted_level)))
            else:
                xp_str = ', '.join(
                    f'{AQUA}{xp}' if xp <= exp_level
                    else f'{YELLOW}{xp}' for xp in xps)
            aqua(f'   {xp_str}')

    while True:
        green('Please enter the enchantment index and level.')
        cmd = input(']> ').split()

        if len(cmd) != 2:
            red('Invalid format. Please try again.')
            continue

        index = self.parse_index(cmd[0], len(avaliable))
        if index is None:
            continue

        name, lvls = avaliable[index]
        level = self.parse_index(cmd[1], len(lvls))
        if index is None or level is None:
            continue

        current = item.enchantments.get(name, 0)
        lvl = lvls[level]

        if level + 1 < current:
            red('Higher level already present!')
            return

        white(f'Cost: {DARK_AQUA}{lvl} Experience Levels')

        if exp_level < lvl:
            red("You don't have enough Experience Levels!")
            return

        self.experience -= calc_exp(lvl)

        if current == level + 1:
            green(f'You removed {BLUE}{format_name(name)}'
                  f' {format_roman(level + 1)}{GREEN}'
                  f' from your {item.display()}!')
            item.enchantments.pop(name)
        else:
            green(f'You applied {BLUE}{format_name(name)}'
                  f' {format_roman(level + 1)}{GREEN}'
                  f' to your {item.display()}!')
            item.enchantments[name] = level + 1

            for conf in CONFLICTS:
                if name in conf:
                    for other in conf:
                        if other == name:
                            continue
                        if other in item.enchantments:
                            item.enchantments.pop(other)

        self.inventory[item_index] = item

        self.add_skill_exp('enchanting', 3.5 * lvl ** 1.5)

        break


@checkpoint
def goto(self, dest: str, /):
    island = get(ISLANDS, self.island)
    zone = get(island.zones, self.zone)

    if not includes(island.zones, dest):
        red('Unknown destination! Use `look` to view options!')
        return
    if zone.name == dest:
        yellow(f'Already at {AQUA}{format_name(dest)}{YELLOW}!')
        return

    path, accum_dist = path_find(zone, get(island.zones, dest),
                                 island.conns, island.dists)

    route = f'{GRAY} ➜ {AQUA}'.join(f'{zone}' for zone in path)
    gray(f'Route: {AQUA}{route} {GRAY}({float(accum_dist):.2f}m)')
    for target in path[1:]:
        if target.skill_req is not None:
            name, level = target.skill_req
            exp_level = self.get_skill_level(name)
            if exp_level < level:
                red(f'Cannot go to {format_zone(dest)}!')
                red(f'Requires {name.capitalize()} level {format_roman(level)}')
                return

        dist = calc_dist(zone, target)
        speed = self.get_stat('speed')
        time_cost = float(dist) / (speed / 10)
        green(f'Going from {zone} to {target}...')
        gray(f'(eta: {time_cost:.1f}s)')
        sleep(time_cost)
        self.zone = target.name
        zone = get(island.zones, target.name)

        if self.zone not in self.visited_zones:
            dark_green(f'{BOLD}{format_zone(self.zone)}')
            green(f'New Zone Discovered!')
            self.visited_zones.append(self.zone)

        if self.zone == 'mist':
            red(f'{BOLD}DANGER')
            dark_gray(f'Powerful creatures reside in the Mist')


def place_minion(self, index: int, slot: int, /):
    if not isinstance(self.placed_minions[slot], Empty):
        red('This slot is not empty!')
        return

    minion = self.inventory[index]
    self.placed_minions[slot] = PlacedMinion(
        minion.name, minion.tier, minion.cooldown, floor(time()),
        [Empty() for _ in range(minion.slots)],
    )
    self.inventory[index] = Empty()

    placed_minion_count = 0
    for _minion in self.placed_minions:
        if isinstance(_minion, PlacedMinion):
            placed_minion_count += 1

    aqua(f'You placed a minion! ({placed_minion_count}'
         f'/{get_minion_cap(len(self.crafted_minions))})')


def remove_minion(self, slot: int, /):
    if isinstance(self.placed_minions[slot], Empty):
        red('This slot is empty!')
        return

    minion = self.placed_minions[slot]
    self.recieve_item({'name': minion.name, 'tier': minion.tier})
    for item in minion.inventory:
        if isinstance(item, Empty):
            continue

        pointer = item.to_obj()
        self.recieve_item(pointer)
        self.collect(pointer['name'], pointer.get('count', 1))

    self.placed_minions[slot] = Empty()

    placed_minion_count = 0
    for _minion in self.placed_minions:
        if isinstance(_minion, PlacedMinion):
            placed_minion_count += 1

    green(f'You picked up a minion!'
          f' You currently have {placed_minion_count} out of a maximum of'
          f' {get_minion_cap(len(self.crafted_minions))} minions placed.')


def remove_pet(self, index: int, /):
    pet = self.pets[index]
    if pet.name == 'grandma_wolf_pet':
        red('The Grandma Wolf Pet cannot be converted into an item!')
        return

    pointer = pet.to_obj()
    pointer['active'] = False
    self.pets.pop(index)
    self.recieve_item(pointer)

    green(f'You converted {pet.display()}{GREEN} into an item!')


def sell(self, index: int, /):
    item = self.inventory[index]

    if isinstance(item, Empty):
        yellow('Skipping as no item to sell.')
        return

    island = get(ISLANDS, self.island)
    zone = get(island.zones, self.zone)

    if len(zone.npcs) == 0:
        red('No NPCs around to sell the item.')
        return

    if item.name not in SELL_PRICE:
        red('You cannot sell this item to an NPC!')
        return

    delta = SELL_PRICE[item.name] * getattr(item, 'count', 1)
    self.purse += delta
    green(f'You sold {item.display()}{GREEN} for '
          f'{GOLD}{format_short(delta)} Coins{GREEN}!')
    self.inventory[index] = Empty()


def summon_pet(self, index: int, /):
    self.pets[index].active = True

    for i, pet in enumerate(self.pets):
        if i != index and pet.active:
            self.pets[i].active = False

    green(f'You summoned your {self.pets[index].display()}{GREEN}!')


@checkpoint
def talkto_npc(self, npc: Npc, /) -> Optional[str]:
    if npc.name not in self.npc_talked:
        if npc.init_dialog is not None:
            self.npc_speak(npc.name, npc.init_dialog)
        elif npc.dialog is not None:
            if isinstance(npc.dialog, list):
                self.npc_speak(npc.name, npc.dialog)
            elif isinstance(npc.dialog, tuple):
                self.npc_speak(npc.name, choice(npc.dialog))
        elif npc.function is not None:
            npc.function(self)
        elif npc.trades is not None:
            self.display_shop(npc, None)
            return npc.name
        else:
            self.npc_silent(npc.name)
        if npc.claim_item is not None:
            self.recieve_item(npc.claim_item)
        self.npc_talked.append(npc.name)
        return
    if npc.trades is not None:
        self.display_shop(npc, None)
        return npc.name
    elif npc.dialog is not None:
        if isinstance(npc.dialog, list):
            self.npc_speak(npc.name, npc.dialog)
        elif isinstance(npc.dialog, tuple):
            self.npc_speak(npc.name, choice(npc.dialog))
    elif npc.function is not None:
        npc.function(self)
    else:
        self.npc_silent(npc.name)


def update(self, /, *, save=True):
    now = int(time())
    last = now if self.last_update == 0 else self.last_update
    dt = now - last

    if self.has_item({'name': 'talisman_of_coins'}):
        last_coins_cp = last // 10
        now_coins_cp = now // 10
        if now_coins_cp > last_coins_cp:
            self.purse += (random_amount((1, 5))
                           * (now_coins_cp - last_coins_cp))

    if self.has_item({'name': 'emerald_ring'}):
        last_min_cp = last // 60
        now_min_cp = now // 60
        if now_min_cp > last_min_cp:
            self.purse += now_min_cp - last_min_cp

    last_save_cp = last // 120
    now_save_cp = now // 120
    if save and now_save_cp > last_save_cp:
        self.dump()
        green('Saved!')

    last_data_cp = last // (12 * 3600)
    now_data_cp = now // (12 * 3600)
    if now_data_cp > last_data_cp:
        install_data(is_update=True)

    last_cp = last // (31 * 3600)
    now_cp = now // (31 * 3600)
    if now_cp > last_cp:
        interest = 0
        if self.bank_level not in INTEREST_TABLE:
            red(f'Invalid bank level: {self.bank_level!r}.')
            return

        table = INTEREST_TABLE[self.bank_level]
        for start, end, ratio in table:
            if self.balance > start:
                interest += ratio * (min(self.balance, end) - start)

        interest *= now_cp - last_cp
        self.balance += interest
        green(f"Since you've been away you earned "
              f'{GOLD}{format_number(interest)} coins{GREEN} '
              f'as interest in your personal bank account!')

    if save:
        self.play_time += dt

    self.last_update = now

    inow = floor(now)
    for index, minion in enumerate(self.placed_minions):
        if isinstance(minion, Empty):
            continue
        if minion.last_action + minion.cooldown > floor(inow):
            continue

        iteration = (inow - minion.last_action) // minion.cooldown
        minion.last_action += minion.cooldown * iteration
        for pointer, average in MINION_LOOT[minion.name[:-7]]:
            _pointer = {**pointer, 'count': random_int(average * iteration)}
            minion.recieve_item(_pointer)
        self.placed_minions[index] = minion


def warp(self, dest: str, /):
    if not includes(ISLANDS, dest):
        for i_name, r_name in self.fast_travel:
            if dest == r_name:
                self.island = i_name
                island = get(ISLANDS, self.island)
                self.zone = r_name
                zone = get(island.zones, r_name)

                gray(f'Warped to {AQUA}{zone}{GRAY}'
                     f' of {AQUA}{island}{GRAY}.')
                return
        else:
            red('Unknown destination! Use `warp` to view options!')
            return

    island = get(ISLANDS, self.island)
    dest_island = get(ISLANDS, dest)
    zone = get(island.zones, self.zone)

    if dest_island.skill_req is not None:
        name, level = dest_island.skill_req
        skill_level = self.get_skill_level(name)
        if skill_level < level:
            red(f'Cannot warp to {dest}!')
            red(f'Requires {name.capitalize()} level {format_roman(level)}')
            return

    if dest == self.island and island.spawn == self.zone:
        yellow(f'Already at {AQUA}{format_zone(dest)}{YELLOW}!')
        return

    dest_zone = get(dest_island.zones,
                    default=get(dest_island.zones, dest_island.spawn),
                    portal=self.island)

    for i_name, r_name in self.fast_travel:
        if dest == i_name and r_name is None:
            self.island = i_name
            island = get(ISLANDS, self.island)
            zone = dest_zone
            self.zone = zone.name

            gray(f'Warped to {AQUA}{zone}{GRAY}'
                 f' of {AQUA}{island}{GRAY}.')
            return

    portal_zone = get(island.zones, portal=dest)

    if portal_zone is None:
        red(f'Cannot warp to {dest}.')
        return

    if self.zone != portal_zone.name:
        self.goto(portal_zone.name)
        if self.zone != portal_zone.name:
            return

    island = get(ISLANDS, dest)
    gray(f'Warping to {AQUA}{dest_zone}{GRAY}'
         f' of {AQUA}{island}{GRAY}...')
    sleep(6)

    self.island = dest
    self.zone = dest_zone.name


action_functions = {
    name: globals()[name] for name in __all__
}
