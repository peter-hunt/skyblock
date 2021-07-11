from random import choice, random
from time import sleep, time
from typing import Optional, Tuple

from ...constant.color import *
from ...constant.enchanting import *
from ...constant.main import INTEREST_TABLE, SELL_PRICE
from ...function.enchanting import get_enchantments
from ...function.io import *
from ...function.math import calc_exp_lvl, calc_exp, random_amount
from ...function.reforging import combine_ench
from ...function.util import (
    checkpoint, format_name, format_number, format_roman, format_short,
    format_zone, get, get_ench, includes,
)
from ...map.island import ISLANDS
from ...map.object import *
from ...object.item import get_item, validify_item
from ...object.object import *
from ...object.recipe import RECIPES


__all__ = [
    'add_pet', 'buy', 'combine', 'consume', 'craft', 'despawn_pet', 'die',
    'enchant', 'goto', 'remove_pet', 'sell', 'summon_pet', 'talkto_npc',
    'update', 'warp',
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
        price = cost * amount
        if self.purse < price:
            red('Not enough coins!')
            return
        self.purse -= price
    else:
        price = None
        for item in cost:
            if isinstance(item, (int, float)):
                if self.purse < item * amount:
                    red('Not enough coins!')
                    return
                continue
            kwargs = {}
            for attr in ('rarity',):
                if hasattr(item, attr):
                    kwargs[attr] = getattr(item, attr)
            if not self.has_item(item[0].name, item[1] * amount, **kwargs):
                red("You don't have the required items.")
                return

        for item in cost:
            if isinstance(item, (int, float)):
                self.purse -= item * amount
                continue
            kwargs = {}
            for attr in ('rarity',):
                if hasattr(item, attr):
                    kwargs[attr] = getattr(item, attr)
            self.remove_item(item[0].name, item[1] * amount, **kwargs)

    good = trade[1]
    if not isinstance(good, list):
        good = [good]

    display = []

    for item in good:
        item_copy = validify_item(item)
        if getattr(item_copy, 'count', 1) != 1:
            item_copy.count = 1
        self.recieve_item(item_copy, amount)
        amt_str = '' if amount == 1 else f'{GRAY} x {amount}'
        display.append(f'{item_copy.display()}{amt_str}')

    display_str = f'{GREEN}, '.join(display)

    if isinstance(price, (float, int)):
        green(f'You bought {display_str}{GREEN} for '
              f'{GOLD}{format_short(price)} Coins{GREEN}!')
    else:
        green(f'You bought {display_str}{GREEN}!')


def combine(self, index_1: int, index_2: int, /):
    item_1 = self.inventory[index_1]
    item_2 = self.inventory[index_2]

    if isinstance(item_1, Empty) or isinstance(item_2, Empty):
        red('These items cannot be combined!')
        return

    if isinstance(item_1, EnchantedBook) and isinstance(item_2, EnchantedBook):
        result_ench = combine_ench(item_1.enchantments, item_2.enchantments)

        self.inventory[index_1] = Empty()
        self.inventory[index_2] = Empty()
        self.recieve_item(EnchantedBook(enchantments=result_ench))

        return

    if (isinstance(item_2, (Axe, Drill, Pickaxe, Hoe,
                            Armor, Bow, Sword, FishingRod))
            and isinstance(item_1, EnchantedBook)):
        index_1, index_2 = index_2, index_1
        item_1, item_2 = item_2, item_1

    if (isinstance(item_1, (Axe, Drill, Pickaxe, Hoe,
                            Armor, Bow, Sword, FishingRod))
            and isinstance(item_2, EnchantedBook)):
        result_ench = combine_ench(item_1.enchantments, item_2.enchantments)
        ench_table = get_enchantments(item_1)
        item_1.enchantments = {
            name: value
            for name, value in result_ench.items()
            if name in ench_table
        }
        self.inventory[index_1] = Empty()
        self.inventory[index_2] = Empty()
        self.recieve_item(item_1)
        return

    if (isinstance(item_2, (Accessory, Armor, Bow, Sword, FishingRod))
            and isinstance(item_1, ReforgeStone)):
        index_1, index_2 = index_2, index_1
        item_1, item_2 = item_2, item_1

    if (isinstance(item_1, (Accessory, Armor, Bow, Sword, FishingRod))
            and isinstance(item_2, ReforgeStone)):
        cost = item_2.cost['curelm'.index(item_1.rarity[0])]

        if item_2.category == 'accessory':
            if not isinstance(item_1, Accessory):
                red('These items cannot be combined!')
                return
        elif item_2.category == 'armor':
            if not isinstance(item_1, Armor):
                red('These items cannot be combined!')
                return
        elif item_2.category == 'bow':
            if not isinstance(item_1, Bow):
                red('These items cannot be combined!')
                return
        elif item_2.category == 'melee':
            if not (isinstance(item_1, (Sword, FishingRod))
                    and getattr(item_1, 'damage', 0) != 0):
                red('These items cannot be combined!')
                return

        if self.purse < cost:
            red("You don't have enough coins to do that!")
            return

        self.purse -= cost

        item_1.modifier = item_2.modifier
        self.inventory[index_1] = Empty()
        self.inventory[index_2] = Empty()
        gray(f'- {GOLD}{format_number(cost)} Coins')
        self.recieve_item(item_1)
        return

    if (item_1.name in {'hot_potato_book', 'fuming_potato_book'} and
            isinstance(item_2, (Armor, Bow, Sword, FishingRod))):
        index_1, index_2 = index_2, index_1
        item_1, item_2 = item_2, item_1

    if (isinstance(item_1, (Armor, Bow, Sword, FishingRod))
            and item_2.name == 'hot_potato_book'):
        if 10 <= item_1.hot_potato < 15:
            red('Error!')
            gray('You have already applied the maximum number of'
                 ' normal Hot Potato books to this item!\n'
                 'Use Fuming Potato books to continue.')
        elif item_1.hot_potato >= 15:
            red('Error!')
            gray('You have already applied the maximum number of'
                 ' Hot Potato books to this item!')
        else:
            item_1.hot_potato += 1
            self.inventory[index_1] = Empty()
            self.inventory[index_2] = Empty()
            self.recieve_item(item_1)
        return

    if (isinstance(item_1, (Armor, Bow, Sword, FishingRod))
            and item_2.name == 'fuming_potato_book'):
        if item_1.hot_potato >= 15:
            red('Error!')
            gray('You have already applied the maximum number of'
                 ' Hot Potato books to this item!')
        else:
            item_1.hot_potato += 1
            self.inventory[index_1] = Empty()
            self.inventory[index_2] = Empty()
            self.recieve_item(item_1)
        return

    red('These items cannot be combined!')
    return


def consume(self, index: int, amount: int = 1, /):
    item = self.inventory[index]

    if isinstance(item, TravelScroll):
        if amount != 1:
            red('Can only use 1 travel scroll at a time!')
            return

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

        if self.has_item('experience_artifact'):
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


def craft(self, index: int, amount: int = 1, /):
    recipe = RECIPES[index]

    if recipe.collection_req is not None:
        coll_name, lvl = recipe.collection_req
        if self.get_collection_lvl(coll_name) < lvl:
            red("You haven't reached the required collection yet!")
            return

    for item, count in recipe.ingredients:
        if not self.has_item(item.name, count * amount):
            red("You don't have the items to do this!")
            return

    for item, count in recipe.ingredients:
        self.remove_item(item.name, count * amount)

    result, result_count = recipe.result

    if isinstance(result, Pet):
        keep_weight = 80
        upgrade_weight = 20 + 0.2 * self.get_stat('pet_luck')
        total = keep_weight + upgrade_weight
        if random() > (keep_weight / total):
            result.rarity = {
                'common': 'uncommon',
                'uncommon': 'rare',
                'rare': 'epic',
                'epic': 'legendary',
            }[result.rarity]

    self.recieve_item(result, result_count * amount)


def despawn_pet(self, /):
    for i, pet in enumerate(self.pets):
        if pet.active:
            self.pets[i].active = False
            break
    else:
        green("You don't have a pet spawned!")
        return

    green(f'You despawned your {pet.display()}{GREEN}!')


def die(self, killer: Optional[str] = None, /) -> bool:
    if self.has_item('saving_grace'):
        self.remove_item('saving_grace')
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

    if self.has_item('piggy_bank'):
        if lost_coins >= 20_000:
            did_crack_piggy = True
            lost_coins = 0
            self.remove_item('piggy_bank')
            self.recieve_item(get_item('cracked_piggy_bank'))

    did_broke_piggy = False

    if not did_crack_piggy and self.has_item('cracked_piggy_bank'):
        if lost_coins >= 20_000:
            did_broke_piggy = True
            lost_coins *= 0.25
            self.remove_item('cracked_piggy_bank')
            self.recieve_item(get_item('broken_piggy_bank'))

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
    elif perc_lost == 0:
        red(f'You died!')
    else:
        red(f'You died and lost {format_number(lost_coins)} coins!')
    self.zone = get(ISLANDS, self.island).spawn

    return True


@checkpoint
def enchant(self, item_index: int, /):
    enchanting_lvl = self.get_skill_lvl('enchanting')
    exp_lvl = calc_exp_lvl(self.experience)

    item = self.inventory[item_index]

    if getattr(item, 'count', 1) != 1:
        red('Cannot Enchant more than one item at once!')
        return

    ench_table = get_enchantments(item)

    if len(ench_table) == 0:
        red('Cannot Enchant Item!')
        gray('This item cannot be enchanted!')
        return

    avaliable = []

    all_ench = [row[0] for row in ENCHS]

    gray('Avaliable enchantments and xp level needed:')
    for name in ench_table:
        if name not in all_ench:
            continue

        for _ench, req in ENCH_REQUIREMENTS:
            if name == _ench and req > enchanting_lvl:
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
            discounted_lvl = [calc_exp_lvl(xp) for xp in discounted]
            avaliable.append((name, discounted_lvl))

            blue(f'{len(avaliable):>2} {name}')
            if current > 0:
                xp_str = ', '.join(
                    f'{GRAY}{xp}' if lvl + 1 < current
                    else f'{RED}{xp}' if lvl + 1 == current
                    else f'{DARK_AQUA}{xp}{AQUA}➜{AQUA}{dxp}'
                    if xp != dxp else f'{AQUA}{xp}'
                    for lvl, (xp, dxp) in enumerate(
                        zip(xps, discounted_lvl)))
            else:
                xp_str = ', '.join(
                    f'{AQUA}{xp}' if xp <= exp_lvl
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

        if exp_lvl < lvl:
            red("You don't have enough Levels!")
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
            exp_lvl = self.get_skill_lvl(name)
            if exp_lvl < level:
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


def remove_pet(self, index: int, /):
    pet = self.pets[index]
    pet.active = False
    self.pets.pop(index)
    self.recieve_item(pet)

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
            self.npc_silent(npc)
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
        self.npc_silent(npc)


def update(self, /):
    now = int(time())
    last = now if self.last_update == 0 else self.last_update
    dt = now - last

    if self.has_item('talisman_of_coins'):
        last_coins_cp = last // 10
        now_coins_cp = now // 10
        if now_coins_cp > last_coins_cp:
            self.purse += (random_amount((1, 5))
                           * (now_coins_cp - last_coins_cp))

    if self.has_item('emerald_ring'):
        last_min_cp = last // 60
        now_min_cp = now // 60
        if now_min_cp > last_min_cp:
            self.purse += now_min_cp - last_min_cp

    last_save_cp = last // 300
    now_save_cp = now // 300
    if now_save_cp > last_save_cp:
        self.dump()
        green('Saved!')

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

    self.play_time += dt

    self.last_update = now


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
        skill_lvl = self.get_skill_lvl(name)
        if skill_lvl < level:
            red(f'Cannot warp to {dest}!')
            red(f'Requires {name.capitalize()} level {format_roman(level)}')
            return

    if dest == self.island and island.spawn == self.zone:
        yellow(f'Already at {AQUA}{format_name(dest)}{YELLOW}!')
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
