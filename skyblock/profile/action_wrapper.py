from decimal import Decimal
from math import ceil
from random import randint, random
from time import sleep, time
from typing import Optional, Tuple

from ..constant.color import (
    RARITY_COLORS, DARK_AQUA, GOLD, GRAY, BLUE, GREEN, AQUA, RED, YELLOW, WHITE)
from ..constant.enchanting import (
    ENCHS, CONFLICTS, ENCH_REQUIREMENTS,
    SWORD_ENCHS, BOW_ENCHS, ARMOR_ENCHS,
    AXE_ENCHS, HOE_ENCHS, PICKAXE_ENCHS)
from ..constant.main import INTEREST_TABLE, SELL_PRICE
from ..constant.mob import CUBISM_EFT, ENDER_SLAYER_EFT, BOA_EFT, SMITE_EFT
from ..function.io import gray, red, green, yellow, blue, aqua, white
from ..function.math import (
    calc_exp_lvl, calc_exp, calc_skill_lvl,
    random_amount, random_bool, random_int)
from ..function.util import (
    checkpoint, display_name, display_number, get, get_ench, includes,
    roman, shorten_number)
from ..object.collection import is_collection
from ..object.fishing import FISHING_TABLE
from ..object.item import get_item, validify_item
from ..object.mob import get_mob
from ..object.object import (
    Item, Empty, Bow, Sword, Armor,
    Axe, Hoe, Pickaxe, Drill, FishingRod, TravelScroll, Pet,
    Crop, Mineral, Wood, Mob)
from ..object.recipe import RECIPES
from ..object.resource import get_resource
from ..map.island import ISLANDS
from ..map.object import calc_dist, path_find


__all__ = ['profile_action']


def profile_action(cls):
    def add_pet(self, index: int, /):
        item = self.inventory[index]

        if not isinstance(item, Pet):
            red('Invalid pet.')

        self.pets.append(item)
        self.inventory[index] = Empty()

        green(f'Successfully added {item.display()} {GREEN}to your pet menu!')

    cls.add_pet = add_pet

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
                for attr in ('rarity', ):
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
            self.recieve_item(item_copy, amount)
            amt_str = '' if amount == 1 else f'{GRAY} x {amount}'
            display.append(f'{item_copy.display()}{amt_str}')

        display_str = f'{GREEN}, '.join(display)

        if isinstance(price, (float, int)):
            green(f'You bought {display_str}{GREEN} for '
                  f'{GOLD}{shorten_number(price)} Coins{GREEN}!')
        else:
            green(f'You bought {display_str}{GREEN}!')

    cls.buy = buy

    def consume(self, index: int, amount: int = 1, /):
        item = self.inventory[index]

        if isinstance(item, TravelScroll):
            if amount != 1:
                red('Can only use 1 travel scroll at a time!')
                return

            if [item.island, item.region] in self.fast_travel:
                red('You already unlocked this fast travel!')
                return

            self.fast_travel.append([item.island, item.region])
            self.inventory[index] = Empty()
            name = display_name(item.island)
            if item.region is not None:
                name += f' {GRAY}- {AQUA}{display_name(item.region)}'
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

            item_copy = item.copy()
            item_copy.count = amount

            gray(f'You consumed {item_copy.display()}{GRAY}!')
            self.add_exp(exp_amount)

            self.inventory[index].count -= amount
            if self.inventory[index].count == 0:
                self.inventory[index] = Empty()

        else:
            red('This item is not consumable!')

    cls.consume = consume

    def craft(self, index: int, amount: int = 1, /):
        recipe = RECIPES[index]

        if recipe.collection_req is not None:
            coll_name, lvl = recipe.collection_req
            if self.coll_lvl(coll_name) < lvl:
                red("You haven't reached the required collection yet!")
                return

        for item, count in recipe.ingredients:
            if not self.has_item(item.name, count * amount):
                red("You don't have the items to do this!")
                return

        for item, count in recipe.ingredients:
            self.remove_item(item.name, count * amount)

        result, result_count = recipe.result
        rarity = result.rarity

        if isinstance(result, Pet):
            keep_weight = 80
            upgrade_weight = 20 + 0.2 * self.get_stat('pet_luck')
            total = keep_weight + upgrade_weight
            if random() > (keep_weight / total):
                rarity = {
                    'common': 'uncommon',
                    'uncommon': 'rare',
                    'rare': 'epic',
                    'epic': 'legendary',
                }[rarity]

        original = get_item(result.name, rarity=rarity)
        if hasattr(original, 'conut'):
            original.count = 1
        self.recieve_item(original, result_count * amount)

    cls.craft = craft

    def despawn_pet(self, /):
        for i, pet in enumerate(self.pets):
            if pet.active:
                self.pets[i].active = False
                break
        else:
            green("You don't have a pet spawned!")
            return

        green(f'You despawned your {pet.display()}{GREEN}!')

    cls.despawn_pet = despawn_pet

    def die(self, /) -> bool:
        if self.has_item('saving_grace'):
            self.remove_item('saving_grace')
            self.island = 'hub'
            self.region = 'village'
            green('Saving Grace has activated! '
                  'You have been revived safely.')
            return False

        bank = 0

        for piece in self.armor:
            if not isinstance(piece, Armor):
                continue

            ench = getattr(piece, 'enchantments', {})
            bank += ench.get('bank', 0) * 10

        original = self.purse / 2
        saved = original * min(bank / 100, 1)
        lost_coins = original - saved
        self.purse -= lost_coins
        self.death_count += 1

        if bank != 0:
            gray(f'Your {BLUE}Bank{GRAY} enchantment saved {GOLD}'
                 f'{shorten_number(saved)} coins{GRAY} for you!')

        red(f'You died and lost {display_number(lost_coins)} coins!')
        self.region = get(ISLANDS, self.island).spawn

        return True

    cls.die = die

    @checkpoint
    def enchant(self, item_index: int, /):
        enchanting_lvl = calc_skill_lvl('enchanting', self.skill_xp_enchanting)
        exp_lvl = calc_exp_lvl(self.experience)

        item = self.inventory[item_index]

        if getattr(item, 'count', 1) != 1:
            red('Cannot Enchant more than one item at once!')
            return

        if isinstance(item, Sword):
            table = SWORD_ENCHS
        elif isinstance(item, Bow):
            table = BOW_ENCHS
        elif isinstance(item, Armor):
            table = ARMOR_ENCHS
        elif isinstance(item, Axe):
            table = AXE_ENCHS
        elif isinstance(item, Hoe):
            table = HOE_ENCHS
        elif isinstance(item, (Pickaxe, Drill)):
            table = PICKAXE_ENCHS
        else:
            red('Cannot Enchant Item!')
            gray('This item cannot be enchanted!')
            return

        avaliable = []

        all_ench = [row[0] for row in ENCHS]

        gray('Avaliable enchantments and xp level needed:')
        for name in table:
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
                green(f'You removed {BLUE}{display_name(name)}'
                      f' {roman(level + 1)} from your {item.display()}!')
                item.enchantments.pop(name)
            else:
                green(f'You applied {BLUE}{display_name(name)}'
                      f' {roman(level + 1)} to your {item.display()}!')
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

    cls.enchant = enchant

    @checkpoint
    def fish(self, rod_index: int, iteration: int = 1, /):
        rod = Empty() if rod_index is None else self.inventory[rod_index]

        if not isinstance(rod, (Empty, FishingRod)):
            rod = Empty()

        enchantments = getattr(rod, 'enchantments', {})

        time_multiplier = 1
        if 'lure' in enchantments:
            time_multiplier -= enchantments['lure'] * 0.05

        total_weight = 0
        for choice in FISHING_TABLE:
            total_weight += choice[3]

        last_cp = Decimal()
        cp_step = Decimal('0.1')
        for i in range(1, iteration + 1):
            sleep(random_amount((5, 30)) * time_multiplier)

            pool = random() * total_weight
            for drop, amount, rarity, weight, exp in FISHING_TABLE:
                if pool < weight:
                    break

            if isinstance(drop, (int, float, tuple)):
                self.purse += random_amount(drop)
            else:
                if isinstance(drop, Item):
                    item_type = get_item(drop.name)
                else:
                    item_type = drop.copy()
                if getattr(item_type, 'count', 1) != 1:
                    item_type.count = 1
                self.recieve_item(item_type, amount)
                if is_collection(drop.name):
                    self.collect(drop.name, amount)

                if 'catch' in rarity:
                    rarity_display = rarity.upper().replace('_', ' ')
                    a_an = 'an' if item_type.name[0] in 'aeiou' else 'a'
                    gray(f'{RARITY_COLORS[rarity]}{rarity_display}! {AQUA}'
                         f'You found {a_an} {item_type.display()}{AQUA}.')

            self.add_skill_exp('fishing', exp)
            self.add_exp(random_amount((1, 6)))

            if i >= (last_cp + cp_step) * iteration:
                while i >= (last_cp + cp_step) * iteration:
                    last_cp += cp_step
                gray(f'{i} / {iteration} ({(last_cp * 100):.0f}%) done')

    cls.fish = fish

    @checkpoint
    def gather(self, name: str, tool_index: Optional[int],
               iteration: Optional[int] = 1, /):
        resource = get_resource(name)
        tool = Empty() if tool_index is None else self.inventory[tool_index]
        iteration = 1 if iteration is None else iteration

        if not isinstance(tool, (Empty, Axe, Hoe, Pickaxe, Drill)):
            tool = Empty()

        enchantments = getattr(tool, 'enchantments', {})

        if isinstance(resource, Crop):
            time_cost = 0.4

            farming_fortune = self.get_stat('farming_fortune', tool_index)
            fortune_mult = 1 + farming_fortune / 100
            drop_item = resource.name
            default_amount = resource.amount

            last_cp = Decimal()
            cp_step = Decimal('0.1')
            is_coll = is_collection(drop_item)
            for i in range(1, iteration + 1):
                sleep(time_cost)
                amount_pool = random_amount(default_amount)
                drop_pool = random_int(fortune_mult)

                item_type = get_item(drop_item)
                if getattr(item_type, 'count', 1) != 1:
                    item_type.count = 1
                self.recieve_item(item_type, drop_pool)
                if is_coll:
                    self.collect(drop_item, amount_pool * drop_pool)

                if resource.name == 'wheat':
                    seeds_pool = random_amount((0, 3))
                    self.recieve_item(Item('seeds'), seeds_pool * drop_pool)
                    if is_coll:
                        self.collect('seeds', seeds_pool * drop_pool)

                self.add_skill_exp('farming', resource.farming_exp)
                if i >= (last_cp + cp_step) * iteration:
                    while i >= (last_cp + cp_step) * iteration:
                        last_cp += cp_step
                    gray(f'{i} / {iteration} ({(last_cp * 100):.0f}%) done')

        elif isinstance(resource, Mineral):
            breaking_power = getattr(tool, 'breaking_power', 0)
            mining_speed = getattr(tool, 'mining_speed', 50)
            if 'efficiency' in enchantments:
                mining_speed += 10 + 20 * enchantments['efficiency']

            if resource.breaking_power > breaking_power:
                red(f'Insufficient breaking power for {resource.name}!')
                return

            time_cost = 30 * resource.hardness / mining_speed

            mining_fortune = self.get_stat('mining_fortune', tool_index)
            fortune_mult = 1 + mining_fortune / 100
            exp_mult = 1 + 0.125 * enchantments.get('experience', 0)

            lapis_exp_bonus = 1

            for piece in self.armor:
                if not isinstance(piece, Armor):
                    break

                if piece.name in {'lapis_helmet', 'lapis_chestplate',
                                  'lapis_leggings', 'lapis_boots'}:
                    lapis_exp_bonus += 0.5

            exp_mult *= lapis_exp_bonus

            drop_item = resource.drop
            default_amount = resource.amount

            last_cp = Decimal()
            cp_step = Decimal('0.1')
            is_coll = is_collection(drop_item)
            for i in range(1, iteration + 1):
                sleep(time_cost)
                amount_pool = random_amount(default_amount)
                drop_pool = random_int(fortune_mult)
                item_type = get_item(drop_item)
                if getattr(item_type, 'count', 1) != 1:
                    item_type.count = 1
                self.recieve_item(item_type, amount_pool * drop_pool)
                if is_coll:
                    self.collect(drop_item, amount_pool * drop_pool)

                self.add_exp(random_amount(resource.exp)
                             * random_amount(exp_mult))
                self.add_skill_exp('mining', resource.mining_exp)
                if i >= (last_cp + cp_step) * iteration:
                    while i >= (last_cp + cp_step) * iteration:
                        last_cp += cp_step
                    gray(f'{i} / {iteration} ({(last_cp * 100):.0f}%) done')

                if 'mithril' in resource.name and randint(1, 50) == 1:
                    white('Titanium has spawned nearby!')
                    self.gather('titanium', tool_index)

        elif isinstance(resource, Wood):
            is_wood = True
            if 'wood' not in resource.name:
                time_cost = 0.5
                break_amount = 1
                is_wood = False
            elif getattr(tool, 'name', None) == 'jungle_axe':
                time_cost = 2
                break_amount = 10
            elif getattr(tool, 'name', None) == 'treecapitator':
                time_cost = 2
                break_amount = 35
            else:
                if isinstance(tool, Axe):
                    tool_speed = tool.tool_speed
                    if 'efficiency' in enchantments:
                        tool_speed += enchantments['efficiency'] ** 2 + 1
                    time_cost = 1.5 * resource.hardness / tool_speed
                else:
                    tool_speed = 1
                    time_cost = 5 * resource.hardness / tool_speed
                time_cost = ceil(time_cost * 20) / 20
                break_amount = 1

            foraging_fortune = self.get_stat('foraging_fortune', tool_index)
            fortune_mult = 1 + foraging_fortune / 100

            wood_name = resource.name
            wood_item = get_item(wood_name)
            wood_item.count = 1

            if is_wood:
                sapling_item = get_item(f'{wood_name[:-5]}_sapling')
                sapling_item.count = 1

            last_cp = Decimal()
            cp_step = Decimal('0.1')
            last_harvest = time()
            for i in range(1, iteration + 1):
                sleep(max(last_harvest - time() + time_cost, 0))
                last_harvest = time()
                drop_pool = random_int(fortune_mult)

                for i in range(break_amount):
                    if i != 0:
                        sleep(0.02)

                    self.recieve_item(wood_item, drop_pool)
                    if is_wood:
                        self.collect(wood_name, drop_pool)
                        if random_amount((1, 5)) == 1:
                            self.recieve_item(sapling_item, drop_pool)

                    self.add_skill_exp('foraging', resource.foraging_exp)

                if i >= (last_cp + cp_step) * iteration:
                    while i >= (last_cp + cp_step) * iteration:
                        last_cp += cp_step
                    gray(f'{i} / {iteration} ({(last_cp * 100):.0f}%) done')

        else:
            red('Unknown resource type.')

    cls.gather = gather

    @checkpoint
    def goto(self, dest: str, /):
        island = get(ISLANDS, self.island)
        region = get(island.regions, self.region)

        if not includes(island.regions, dest):
            red('Unknown destination! Use `look` to view options!')
            return
        if region.name == dest:
            yellow(f'Already at {AQUA}{display_name(dest)}{YELLOW}!')
            return

        path, accum_dist = path_find(region, get(island.regions, dest),
                                     island.conns, island.dists)

        speed = self.get_stat('speed')

        full_set = True

        for piece in self.armor:
            if not isinstance(piece, Armor):
                full_set = False
                continue

        if full_set:
            piece_names = [piece.name for piece in self.armor]
            if piece_names == [
                    'young_dragon_helmet', 'young_dragon_chestplate',
                    'young_dragon_leggings', 'young_dragon_boots']:
                speed += 70
            elif piece_names == ['farm_helmet', 'farm_chestplate',
                                 'farm_leggings', 'farm_boots']:
                if self.island in {'barn', 'desert'} or self.region == 'farm':
                    speed += 25
            elif piece_names == [
                    'farm_suit_helmet', 'farm_suit_chestplate',
                    'farm_suit_leggings', 'farm_suit_boots']:
                if self.island in {'barn', 'desert'}:
                    speed += 20

        route = f'{GRAY} ➜ {AQUA}'.join(f'{region}' for region in path)
        gray(f'Route: {AQUA}{route} {GRAY}({float(accum_dist):.2f}m)')
        for target in path[1:]:
            if target.skill_req is not None:
                name, level = target.skill_req
                skill_exp = getattr(self, f'skill_xp_{name}')
                exp_lvl = calc_skill_lvl(name, skill_exp)
                if exp_lvl < level:
                    red(f'Cannot go to {dest}!')
                    red(f'Requires {name.capitalize()} level {roman(level)}')
                    return

            dist = calc_dist(region, target)
            time_cost = float(dist) / (5 * (speed / 100))
            green(f'Going from {region} to {target}...')
            gray(f'(time cost: {time_cost:.1f}s)')
            sleep(time_cost)
            self.region = target.name
            region = get(island.regions, target.name)

    cls.goto = goto

    def remove_pet(self, index: int, /):
        pet = self.pets[index]
        pet.active = False
        self.pets.pop(index)
        self.recieve_item(pet)

        green(f'You converted {pet.display()}{GREEN} into an item!')

    cls.remove_pet = remove_pet

    def sell(self, index: int, /):
        item = self.inventory[index]

        if isinstance(item, Empty):
            yellow('Skipping as no item to sell.')
            return

        island = get(ISLANDS, self.island)
        region = get(island.regions, self.region)

        if len(region.npcs) == 0:
            red('No NPCs around to sell the item.')
            return

        if item.name not in SELL_PRICE:
            red('You cannot sell this item to an NPC!')
            return

        delta = SELL_PRICE[item.name] * getattr(item, 'count', 1)
        self.purse += delta
        green(f'You sold {item.display()}{GREEN} for '
              f'{GOLD}{shorten_number(delta)} Coins{GREEN}!')
        self.inventory[index] = Empty()

    cls.sell = sell

    @checkpoint
    def slay(self, name: str, weapon_index: Optional[int], amount: int = 1, /):
        mob = get_mob(name)
        mob_name = display_name(mob.name)

        weapon = (Empty() if weapon_index is None
                  else self.inventory[weapon_index])

        if not isinstance(weapon, (Empty, Bow, Sword)):
            weapon = Empty()

        if not isinstance(mob, Mob):
            red('Unknown mob type.')
            return

        health = self.get_stat('health', weapon_index)
        defense = self.get_stat('defense', weapon_index)
        # true_defense = self.get_stat('true_defense', weapon_index)
        strength = self.get_stat('strength', weapon_index)
        speed = self.get_stat('speed', weapon_index)
        crit_chance = self.get_stat('crit_chance', weapon_index)
        crit_damage = self.get_stat('crit_damage', weapon_index)
        # attack_speed = 0
        # intelligence = self.get_stat('intelligence', weapon_index)
        magic_find = self.get_stat('magic_find', weapon_index)
        ferocity = self.get_stat('ferocity', weapon_index)

        thorns = 0

        last_stand = 0
        no_pain_no_gain = []

        combat_lvl = calc_skill_lvl('combat', self.skill_xp_combat)

        enchantments = getattr(weapon, 'enchantments', {})

        farm_armor_speed = False
        farm_suit_speed = False
        pumpkin_buff = False
        deflect = False
        protective_blood = False
        holy_blood = False
        young_blood = False

        if isinstance(weapon, (Bow, Sword)):
            ultimate_jerry = enchantments.get('ultimate_jerry', 0) * 50
            damage = weapon.damage + ultimate_jerry + 5

            for armor_piece in self.armor:
                if not isinstance(armor_piece, Armor):
                    break
            else:
                piece_names = [piece.name for piece in self.armor]
                if piece_names == ['farm_helmet', 'farm_chestplate',
                                   'farm_leggings', 'farm_boots']:
                    if (self.island in {'barn', 'desert'}
                            or self.region == 'farm'):
                        farm_armor_speed += True
                elif piece_names == [
                        'farm_suit_helmet', 'farm_suit_chestplate',
                        'farm_suit_leggings', 'farm_suit_boots']:
                    if self.island in {'barn', 'desert'}:
                        farm_suit_speed = True
                elif piece_names == ['pumpkin_helmet', 'pumpkin_chestplate',
                                     'pumpkin_leggings', 'pumpkin_boots']:
                    pumpkin_buff = True
                elif piece_names == ['cactus_helmet', 'cactus_chestplate',
                                     'cactus_leggings', 'cactus_boots']:
                    deflect = True
                elif piece_names == ['protector_dragon_helmet',
                                     'protector_dragon_chestplate',
                                     'protector_dragon_leggings',
                                     'protector_dragon_boots']:
                    protective_blood = True
                elif piece_names == [
                        'holy_dragon_helmet', 'holy_dragon_chestplate',
                        'holy_dragon_leggings', 'holy_dragon_boots']:
                    holy_blood = True
                elif piece_names == [
                        'young_dragon_helmet', 'young_dragon_chestplate',
                        'young_dragon_leggings', 'young_dragon_boots']:
                    young_blood = True
                elif piece_names == [
                        'strong_dragon_helmet', 'strong_dragon_chestplate',
                        'strong_dragon_leggings', 'strong_dragon_boots']:
                    if isinstance(weapon, Empty):
                        pass
                    elif weapon.name == 'aspect_of_the_end':
                        damage += 75

            damage += weapon.hot_potato

            if enchantments.get('one_for_all', 0) != 0:
                damage *= 3.1

            strength += weapon.hot_potato
            crit_chance += weapon.crit_chance
            crit_damage += weapon.crit_damage
            ferocity += weapon.ferocity

            damage *= 1 + 0.08 * enchantments.get('power', 0)
            damage *= 1 + 0.05 * enchantments.get('sharpness', 0)
            if name in CUBISM_EFT:
                damage *= 1 + 0.1 * enchantments.get('cubism', 0)
            if name in ENDER_SLAYER_EFT:
                damage *= 1 + 0.12 * enchantments.get('ender_slayer', 0)
            if name in BOA_EFT:
                damage *= 1 + 0.08 * enchantments.get('bane_of_arthropods', 0)
            if name in SMITE_EFT:
                damage *= 1 + 0.08 * enchantments.get('smite', 0)

            crit_damage += 10 * enchantments.get('critical', 0)
            ferocity += enchantments.get('vicious', 0)
        else:
            damage = 5

        rejuvenate = 0

        for piece in self.armor:
            if not isinstance(piece, Armor):
                continue

            ench = getattr(piece, 'enchantments', {})
            rejuvenate += ench.get('rejuvenate', 0) * 2
            thorns += ench.get('thorns', 0) * 3
            last_stand += ench.get('last_stand', 0) * 5
            no_pain_no_gain.append(ench.get('no_pain_no_gain', 0) * 25)

        if deflect:
            thorns += 33

        warrior = 0.04 * min(combat_lvl, 50)
        warrior += 0.01 * max(min(combat_lvl - 50, 10), 0)
        damage *= 1 + warrior
        if pumpkin_buff:
            damage *= 1.1

        enchanting_lvl = calc_skill_lvl('enchanting', self.skill_xp_enchanting)

        execute = 0.2 * enchantments.get('execute', 0)
        experience = 1 + 0.125 * enchantments.get('experience', 0)
        experience += 0.04 * enchanting_lvl
        first_strike = 1 + 0.25 * enchantments.get('first_strike', 0)
        giant_killer = enchantments.get('giant_killer', 0)
        life_steal = 0.005 * enchantments.get('life_steal', 0)
        if isinstance(weapon, Bow):
            looting = 1 + 0.15 * enchantments.get('chance', 0)
        elif isinstance(weapon, Sword):
            looting = 1 + 0.15 * enchantments.get('looting', 0)
        else:
            looting = 1
        luck = 1 + 0.05 * enchantments.get('luck', 0)
        overload = enchantments.get('overload', 0)
        prosecute = 0.1 * enchantments.get('prosecute', 0)
        scavenger = 0.3 * enchantments.get('scavenger', 0)
        if 'syphon' in enchantments:
            syphon = 0.1 + 0.1 * enchantments['syphon']
        else:
            syphon = 0
        triple_strike = 1 + 0.10 * enchantments.get('triple_strike', 0)
        vampirism = enchantments.get('vampirism', 0)

        soul_eater = enchantments.get('soul_eater', 0) * 2
        soul_eater_strength = 0

        crit_chance += overload
        crit_damage += overload

        hp = health

        last_cp = Decimal()
        cp_step = Decimal('0.1')
        is_coll = {
            row[0].name: is_collection(row[0].name) for row in mob.drops}
        green(f'Slaying {mob.display()}{GREEN}:')
        for count in range(1, amount + 1):
            actual_speed = speed
            if young_blood and hp >= health / 2:
                actual_speed += 70
            if farm_armor_speed:
                actual_speed += 25
            if farm_suit_speed:
                actual_speed += 20
            time_cost = 10 / (5 * actual_speed / 100)
            sleep(time_cost)

            healed = (round((time_cost // 2) * (1.5 + health / 100), 1)
                      * (1 + (rejuvenate / 100)))
            if holy_blood:
                healed *= 3
            hp = min(hp - + healed, health)
            if healed != 0:
                gray(f'You healed for {GREEN}{shorten_number(healed)}'
                     f'{RED}❤{GRAY}.\n'
                     f'Your HP: {GREEN}{shorten_number(hp)}{GRAY}/'
                     f'{GREEN}{shorten_number(health)}{RED}❤\n')
            healed = 0

            mob_hp = mob.health
            while True:
                strike_count = 0

                killed = False

                for _ in range(random_int(1 + ferocity / 100)):
                    crit = ''
                    if random_bool(crit_chance / 100):
                        damage_dealt = damage * (1 + crit_damage / 100)
                        if crit_chance >= 100 and random_bool(overload * 0.1):
                            damage_dealt *= 1.1
                        crit = 'crit '
                    else:
                        damage_dealt = damage

                    damage_dealt *= 1 + (strength + soul_eater_strength) / 100

                    if soul_eater_strength != 0:
                        soul_eater_strength = 0

                    damage_dealt *= (
                        1 + giant_killer * (min(0.1 * (mob_hp - hp), 5) / 100))

                    if strike_count == 0:
                        damage_dealt *= first_strike
                    if strike_count < 3:
                        damage_dealt *= triple_strike

                    damage_dealt *= 1 + min(prosecute * (mob_hp / mob.health),
                                            0.35)
                    damage_dealt += (execute / 100) * (mob.health - mob_hp)

                    mob_hp = max(mob_hp - damage_dealt, 0)
                    gray(f"You've dealt {YELLOW}{shorten_number(damage_dealt)}"
                         f'{GRAY} {crit}damage to the {mob_name}!\n\n')

                    if life_steal != 0:
                        healed += life_steal * health

                    if syphon != 0:
                        healed += syphon * health * (crit_damage // 100)

                    if mob_hp <= 0:
                        a_an = 'an' if mob.name[0] in 'aeiou' else 'a'
                        green(f"You've killed {a_an} {mob_name}!")
                        soul_eater_strength = mob.damage * soul_eater
                        killed = True
                        break

                    gray(f"{mob_name}'s HP: "
                         f'{GREEN}{shorten_number(mob_hp)}{GRAY}'
                         f'/{GREEN}{shorten_number(mob.health)}{RED}❤\n')

                if killed:
                    break

                actual_defense = defense
                if protective_blood:
                    actual_defense *= 1 + (1 - hp / health)

                if last_stand != 0 and hp / health < 0.4:
                    actual_defense *= last_stand / 100

                if mob.damage != 0:
                    damage_recieved = mob.damage / (1 + defense / 100)
                    if pumpkin_buff:
                        damage_recieved *= 0.9
                    hp = max(hp - damage_recieved, 0)
                    gray(f"You've recieved {YELLOW}"
                         f'{shorten_number(damage_recieved)}{GRAY}'
                         f' damage from the {mob_name}{GRAY}!\n'
                         f'Your HP: {GREEN}{shorten_number(hp)}{GRAY}/'
                         f'{GREEN}{shorten_number(health)}{RED}❤\n')

                exp_npng = 0
                for npng_chance in no_pain_no_gain:
                    if random_bool(npng_chance / 100):
                        exp_npng += 10
                if exp_npng != 0:
                    self.add_exp(exp_npng)

                if hp <= 0:
                    if self.die():
                        red(f' ☠ {GRAY}You were killed by {mob_name}.')
                    return

                if random_bool(0.5) and thorns != 0:
                    thorns_damage = (thorns / 100) * damage_recieved
                    mob_hp -= thorns_damage

                    if mob_hp <= 0:
                        a_an = 'an' if mob.name[0] in 'aeiou' else 'a'
                        green(f"You've killed {a_an} {mob_name}{GRAY}!\n"
                              f'Your HP: {GREEN}{shorten_number(hp)}{GRAY}/'
                              f'{GREEN}{shorten_number(health)}{RED}❤\n')
                        break

                gray(f'Your HP: {GREEN}{shorten_number(hp)}{GRAY}/'
                     f'{GREEN}{shorten_number(health)}{RED}❤\n'
                     f"{mob_name}'s HP: "
                     f'{GREEN}{shorten_number(mob_hp)}{GRAY}'
                     f'/{GREEN}{shorten_number(mob.health)}{RED}❤\n\n')

                strike_count += 1

            if vampirism != 0 and hp != health:
                delta = (health - hp) * (vampirism / 100)
                hp += delta

                gray(f'Your {BLUE}Vampirism{GRAY} enchantment healed you for '
                     f'{AQUA}{shorten_number(delta)}{RED}❤{GRAY}!\n'
                     f'Your HP: {GREEN}{shorten_number(hp)}{GRAY}/'
                     f'{GREEN}{shorten_number(health)}{RED}❤\n')

            self.purse += mob.coins + scavenger
            self.add_exp(mob.exp * random_int(experience))
            self.add_skill_exp('combat', mob.combat_xp)

            for item, count, rarity, drop_chance in mob.drops:
                drop_chance *= looting
                drop_chance *= 1 + magic_find / 100
                if isinstance(item, Armor):
                    drop_chance *= luck

                if not random_bool(drop_chance):
                    continue

                loot = validify_item(item)

                self.recieve_item(loot, random_amount(count))

                if is_coll[loot.name]:
                    self.collect(loot.name, loot.count)

                if rarity not in {'common', 'uncommon'}:
                    rarity_str = rarity.replace('_', ' ').upper()
                    white(f'{RARITY_COLORS[rarity]}{rarity_str} DROP! '
                          f'{WHITE}({loot.display()}{WHITE})')

            if count >= (last_cp + cp_step) * amount:
                while count >= (last_cp + cp_step) * amount:
                    last_cp += cp_step
                gray(f'{count} / {amount} ({(last_cp * 100):.0f}%) killed')

            gray('\n')

    cls.slay = slay

    def summon_pet(self, index: int, /):
        self.pets[index].active = True

        for i, pet in enumerate(self.pets):
            if i != index and pet.active:
                self.pets[i].active = False

        green(f'You summoned your {self.pets[index].display()}{GREEN}!')

    cls.summon_pet = summon_pet

    def update(self, /):
        now = int(time())
        last = now if self.last_update == 0 else self.last_update
        dt = now - last

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
                  f'{GOLD}{display_number(interest)} coins{GREEN} '
                  f'as interest in your personal bank account!')

        self.play_time += dt

        self.last_update = now

    cls.update = update

    def warp(self, dest: str, /):
        if not includes(ISLANDS, dest):
            for i_name, r_name in self.fast_travel:
                if dest == r_name:
                    self.island = i_name
                    island = get(ISLANDS, self.island)
                    self.region = r_name
                    region = get(island.regions, r_name)

                    gray(f'Warped to {AQUA}{region}{GRAY}'
                         f' of {AQUA}{island}{GRAY}.')
                    return
            else:
                red('Unknown destination! Use `warp` to view options!')
                return

        island = get(ISLANDS, self.island)
        dest_island = get(ISLANDS, dest)
        region = get(island.regions, self.region)

        if dest_island.skill_req is not None:
            name, level = dest_island.skill_req
            skill_exp = getattr(self, f'skill_xp_{name}')
            exp_lvl = calc_skill_lvl(name, skill_exp)
            if exp_lvl < level:
                red(f'Cannot warp to {dest}!')
                red(f'Requires {name.capitalize()} level {roman(level)}')
                return

        if dest == self.island and island.spawn == self.region:
            yellow(f'Already at {AQUA}{display_name(dest)}{YELLOW}!')
            return

        dest_region = get(dest_island.regions,
                          default=get(dest_island.regions, dest_island.spawn),
                          portal=self.island)

        for i_name, r_name in self.fast_travel:
            if dest == i_name and r_name is None:
                self.island = i_name
                island = get(ISLANDS, self.island)
                region = dest_region
                self.region = region.name

                gray(f'Warped to {AQUA}{region}{GRAY}'
                     f' of {AQUA}{island}{GRAY}.')
                return

        portal_region = get(island.regions, portal=dest)

        if portal_region is None:
            red(f'Cannot warp to {dest}.')
            return

        if self.region != portal_region.name:
            self.goto(portal_region.name)
            if self.region != portal_region.name:
                return

        island = get(ISLANDS, dest)
        gray(f'Warping to {AQUA}{dest_region}{GRAY}'
             f' of {AQUA}{island}{GRAY}...')
        sleep(6)

        self.island = dest
        self.region = dest_region.name

    cls.warp = warp

    return cls
