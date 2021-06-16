from decimal import Decimal
from math import ceil
from time import sleep, time
from typing import Optional, Tuple

from ..constant.color import (
    RARITY_COLORS, BOLD, DARK_AQUA, GOLD, GRAY, BLUE, GREEN,
    AQUA, RED, LIGHT_PURPLE, YELLOW, WHITE,
)
from ..constant.enchanting import (
    ENCHS, CONFLICTS, ENCH_REQUIREMENTS,
    SWORD_ENCHS, BOW_ENCHS, ARMOR_ENCHS,
    AXE_ENCHS, HOE_ENCHS, PICKAXE_ENCHS,
)
from ..constant.main import INTEREST_TABLE, SELL_PRICE
from ..constant.mob import CUBISM_EFT, ENDER_SLAYER_EFT, BOA_EFT, SMITE_EFT
from ..function.io import gray, red, green, yellow, blue, aqua, white
from ..function.math import (
    calc_exp, calc_lvl, calc_skill_exp, random_amount, random_bool, random_int,
)
from ..function.util import (
    backupable, display_name, display_number, get, get_ench, includes,
    roman, shorten_number,
)
from ..item.item import COLLECTION_ITEMS
from ..item.mob import get_mob
from ..item.object import (
    Item, Empty, Bow, Sword, Armor,
    Axe, Hoe, Pickaxe, TravelScroll, Pet,
    Crop, Mineral, Tree, Mob,
)
from ..item.recipe import RECIPES
from ..item.resource import get_resource
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
                for attr in ('rarity', ):
                    if hasattr(item, attr):
                        kwargs[attr] = getattr(item, attr)
                self.remove_item(item[0].name, item[1] * amount, **kwargs)

        good = trade[1]
        if not isinstance(good, list):
            good = [good]

        display = []

        for item in good:
            self.recieve_item(item, amount)
            amt_str = '' if amount == 1 else f'{GRAY} x {amount}'
            display.append(f'{item}{amt_str}')

        display_str = f'{GREEN}, '.join(display)

        if isinstance(price, (float, int)):
            green(f"You bought {display_str}{GREEN} for "
                  f"{GOLD}{shorten_number(price)} Coins{GREEN}!")
        else:
            green(f"You bought {display_str}{GREEN}!")

    cls.buy = buy

    def consume(self, index: int, /):
        item = self.inventory[index]

        if isinstance(item, TravelScroll):
            if [item.island, item.region] in self.fast_travel:
                red('You already unlocked this fast travel!')
                return

            self.fast_travel.append([item.island, item.region])
            self.inventory[index] = Empty()
            name = display_name(item.island)
            if item.region is not None:
                name += f' {display_name(item.region)}'
            yellow('You consumed the scroll!')
            yellow(f'You may now fast travel to {GREEN}{name}{YELLOW}!')

        else:
            red('This item is not consumable!')

    cls.consume = consume

    def craft(self, index: int, amount: int = 1, /):
        recipe = RECIPES[index]

        for item, count in recipe.ingredients:
            if not self.has_item(item.name, count * amount):
                red("You don't have the items to do this!")
                return

        for item, count in recipe.ingredients:
            self.remove_item(item.name, count * amount)

        result_name, result_count = recipe.result
        self.recieve_item(result_name, result_count * amount)

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

    def die(self, /):
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
            gray(f"Your {BLUE}Bank{GRAY} enchantment saved {GOLD}"
                 f"{shorten_number(saved)} coins{GRAY} for you!")

        red(f'You died and lost {display_number(lost_coins)} coins!')
        self.region = get(ISLANDS, self.island).spawn

    cls.die = die

    @backupable
    def enchant(self, item_index: int, /):
        enchanting_lvl = calc_skill_exp('enchanting', self.skill_xp_enchanting)
        exp_lvl = calc_exp(self.experience)

        item = self.inventory[item_index]

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
        elif isinstance(item, Pickaxe):
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
                    current_xp = calc_lvl(xps[min(current - 1, len(xps) - 1)])
                else:
                    current_xp = 0
                discounted = [
                    calc_lvl(xp) if lvl + 1 == current else
                    calc_lvl(xp) - current_xp
                    for lvl, xp in enumerate(xps)
                ]
                discounted_lvl = [calc_exp(xp) for xp in discounted]
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

            self.experience -= calc_lvl(lvl)

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

    @backupable
    def get_item(self, name: str, tool_index: Optional[int],
                 amount: Optional[int] = 1, /):
        resource = get_resource(name)
        tool = Empty() if tool_index is None else self.inventory[tool_index]
        amount = 1 if amount is None else amount

        if not isinstance(tool, (Empty, Axe, Hoe, Pickaxe)):
            tool = Empty()

        enchantments = getattr(tool, 'enchantments', {})

        if isinstance(resource, Crop):
            time_cost = 0.4

            farming_fortune = self.get_stat('farming_fortune', tool_index)
            fortune_mult = 1 + farming_fortune / 100
            drop_item = resource.drop
            default_amount = resource.amount

            last_cp = Decimal()
            cp_step = Decimal('0.1')
            is_collection = includes(COLLECTION_ITEMS, drop_item)
            for count in range(1, amount + 1):
                sleep(time_cost)
                amount_pool = random_amount(default_amount)
                drop_pool = random_int(fortune_mult)
                self.recieve_item(Item(drop_item), amount_pool * drop_pool)
                if is_collection:
                    self.collect(drop_item, amount_pool * drop_pool)

                self.add_skill_exp('farming', resource.farming_exp)
                if count >= (last_cp + cp_step) * amount:
                    while count >= (last_cp + cp_step) * amount:
                        last_cp += cp_step
                    gray(f'{count} / {amount} ({(last_cp * 100):.0f}%) done')

        elif isinstance(resource, Mineral):
            breaking_power = getattr(tool, 'breaking_power', 0)
            mining_speed = getattr(tool, 'mining_speed', 50)
            if 'efficiency' in enchantments:
                mining_speed += 10 + 20 * enchantments['efficiency']

            if resource.breaking_power > breaking_power:
                red(f'Insufficient breaking power for {resource.name}!')
                return

            time_cost = 30 * resource.hardness / mining_speed

            enchanting_lvl = calc_skill_exp('enchanting',
                                            self.skill_xp_enchanting)

            mining_fortune = self.get_stat('mining_fortune', tool_index)
            fortune_mult = 1 + mining_fortune / 100
            experience = 1 + 0.125 * enchantments.get('experience', 0)
            experience *= 1 + 0.04 * enchanting_lvl
            drop_item = resource.drop
            default_amount = resource.amount

            last_cp = Decimal()
            cp_step = Decimal('0.1')
            is_collection = includes(COLLECTION_ITEMS, drop_item)
            for count in range(1, amount + 1):
                sleep(time_cost)
                amount_pool = random_amount(default_amount)
                drop_pool = random_int(fortune_mult)
                self.recieve_item(Item(drop_item), amount_pool * drop_pool)
                if is_collection:
                    self.collect(drop_item, amount_pool * drop_pool)

                self.add_exp(resource.exp * random_amount(experience))
                self.add_skill_exp('mining', resource.mining_exp)
                if count >= (last_cp + cp_step) * amount:
                    while count >= (last_cp + cp_step) * amount:
                        last_cp += cp_step
                    gray(f'{count} / {amount} ({(last_cp * 100):.0f}%) done')

        elif isinstance(resource, Tree):
            if isinstance(tool, Axe):
                tool_speed = tool.tool_speed
                if 'efficiency' in enchantments:
                    tool_speed += enchantments['efficiency'] ** 2 + 1
                time_cost = 1.5 * resource.hardness / tool_speed
            else:
                tool_speed = 1
                time_cost = 5 * resource.hardness / tool_speed
            time_cost = ceil(time_cost * 20) / 20

            foraging_fortune = self.get_stat('foraging_fortune', tool_index)
            fortune_mult = 1 + foraging_fortune / 100

            drop_item = resource.drop

            last_cp = Decimal()
            cp_step = Decimal('0.1')
            is_collection = includes(COLLECTION_ITEMS, drop_item)
            for count in range(1, amount + 1):
                sleep(time_cost)
                drop_pool = random_int(foraging_fortune)
                self.recieve_item(Item(drop_item), drop_pool)
                if is_collection:
                    self.collect(drop_item, drop_pool)

                self.add_skill_exp('foraging', resource.foraging_exp)
                if count >= (last_cp + cp_step) * amount:
                    while count >= (last_cp + cp_step) * amount:
                        last_cp += cp_step
                    gray(f'{count} / {amount} ({(last_cp * 100):.0f}%) done')

        else:
            red('Unknown resource type.')

    cls.get_item = get_item

    @backupable
    def goto(self, dest: str, /):
        island = get(ISLANDS, self.island)
        region = get(island.regions, self.region)

        if not includes(island.regions, dest):
            red(f'Region not found: {dest!r}')
            return
        if region.name == dest:
            yellow(f'Already at region: {dest!r}')
            return
        path, accum_dist = path_find(region, get(island.regions, dest),
                                     island.conns, island.dists)

        speed = 100

        for piece in self.armor:
            if isinstance(piece, Armor):
                speed += piece.speed

        route = f'{GRAY} ➜ {AQUA}'.join(f'{region}' for region in path)
        aqua(f'Route: {route} ({float(accum_dist):.2f}m)')
        for target in path[1:]:
            if target.skill_req is not None:
                name, level = target.skill_req
                skill_exp = getattr(self, f'skill_xp_{name}')
                exp_lvl = calc_skill_exp(name, skill_exp)
                if exp_lvl < level:
                    red(f'Cannot go to {dest}!')
                    red(f'Requires {name.capitalize()} level {roman(level)}')
                    return

            dist = calc_dist(region, target)
            time_cost = float(dist) / (5 * (speed / 100))
            green(f'Going from {region} to {target}...')
            gray(f'(time cost: {time_cost:.2f}s)')
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
        island = get(ISLANDS, self.island)
        region = get(island.regions, self.region)

        if len(region.npcs) == 0:
            red('No NPCs around to sell the item.')
            return

        item = self.inventory[index]
        if item.name not in SELL_PRICE:
            red('You cannot sell this item to an NPC!')
            return

        delta = SELL_PRICE[item.name] * getattr(item, 'count', 1)
        self.purse += delta
        green(f"You sold {item.display()}{GREEN} for "
              f"{GOLD}{shorten_number(delta)} Coins{GREEN}!")
        self.inventory[index] = Empty()

    cls.sell = sell

    @backupable
    def slay(self, name: str, weapon_index: Optional[int], amount: int = 1, /):
        mob = get_mob(name)
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

        combat_lvl = calc_skill_exp('combat', self.skill_xp_combat)

        enchantments = getattr(weapon, 'enchantments', {})

        if isinstance(weapon, (Bow, Sword)):
            ultimate_jerry = enchantments.get('ultimate_jerry', 0) * 50
            damage = weapon.damage + ultimate_jerry + 5
            if ultimate_jerry != 0:
                gray(f"Your {LIGHT_PURPLE}{BOLD}Ultimate Jerry{GRAY} "
                     f"enchantment granted {GREEN}+ {ultimate_jerry}"
                     f" {GRAY}additional weapon base damage!\n")
            additional_damage = damage * \
                enchantments.get('one_for_all', 0) * 2.1
            if additional_damage != 0:
                gray(f"Your {LIGHT_PURPLE}{BOLD}One For All{GRAY} "
                     f"enchantment granted {GREEN}+{additional_damage}"
                     f" {GRAY}additional weapon base damage!\n")
            damage += additional_damage + weapon.hot_potato

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

        warrior = 0.04 * min(combat_lvl, 50)
        warrior += 0.01 * max(min(combat_lvl - 50, 10), 0)
        damage *= 1 + warrior

        time_cost = 10 / (5 * speed / 100)

        execute = 0.2 * enchantments.get('execute', 0)
        experience = 1 + 0.125 * enchantments.get('experience', 0)
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
        is_collection = {
            row[0].name: includes(COLLECTION_ITEMS, row[0].name)
            for row in mob.drops
        }
        green(f'Slaying {mob.display()}')
        for count in range(1, amount + 1):
            sleep(time_cost)
            healed = round((time_cost // 2) * (1.5 + health / 100), 1)
            healed *= 1 + (rejuvenate / 100)
            healed = max(health - hp, healed)
            if healed != 0:
                hp += healed
                gray(f'You healed for {GREEN}{shorten_number(healed)}'
                     f'{RED}❤{GRAY}.')

            mob_hp = mob.health
            while True:
                strike_count = 0

                for _ in range(random_int(1 + ferocity / 100)):
                    crit = ''
                    if random_bool(crit_chance / 100):
                        damage_delt = damage * (1 + crit_damage / 100)
                        if crit_chance >= 100 and random_bool(overload * 0.1):
                            damage_delt *= 1.1
                        crit = 'crit '
                    else:
                        damage_delt = damage

                    damage_delt *= 1 + (strength + soul_eater_strength) / 100

                    if soul_eater_strength != 0:
                        gray(f"Your {LIGHT_PURPLE}{BOLD}Soul Eater{GRAY}"
                             f" enchantment applied {RED}+"
                             f" {soul_eater_strength} ❁ Strength{GRAY}"
                             f" on your hit!\n")
                        soul_eater_strength = 0

                    damage_delt *= (
                        1 + giant_killer * (min(0.1 * (mob_hp - hp), 5) / 100)
                    )

                    if strike_count == 0:
                        damage_delt *= first_strike
                    if strike_count < 3:
                        damage_delt *= triple_strike

                    damage_delt *= 1 + min(prosecute * (mob_hp / mob.health),
                                           0.35)
                    damage_delt += (execute / 100) * (mob.health - mob_hp)

                    mob_hp -= damage_delt
                    gray(f"You delt {YELLOW}{shorten_number(damage_delt)}{GRAY}"
                         f" {crit}damage to the {display_name(mob.name)}!\n")

                    if life_steal != 0:
                        delta = min(health - hp, life_steal * health)
                        if delta != 0:
                            hp += delta
                            gray(f"Your {BLUE}Life Steal{GRAY} "
                                 f"enchantment healed you for {AQUA}"
                                 f"{shorten_number(delta)}{RED}❤{GRAY}!\n")

                    if syphon != 0:
                        delta = min(health - hp,
                                    syphon * health * (crit_damage // 100))
                        if delta != 0:
                            hp += delta
                            gray(f"Your {BLUE}Syphon{GRAY} "
                                 f"enchantment healed you for {AQUA}"
                                 f"{shorten_number(delta)}{RED}❤{GRAY}!\n")

                if mob_hp <= 0:
                    a_an = 'an' if mob.name[0] in 'aeiou' else 'a'
                    green(f"You've killed {a_an} "
                          f"{display_name(mob.name)}!")
                    soul_eater_strength = mob.damage * soul_eater
                    break

                actual_defense = defense
                if last_stand != 0 and hp / health < 0.4:
                    additional_defense = actual_defense * (last_stand / 100)
                    actual_defense += additional_defense
                    gray(f"Your {LIGHT_PURPLE}{BOLD}Last Stand{GRAY}"
                         f" enchantment granted you {GREEN}+"
                         f" {additional_defense} ❈ Defense{GRAY}!\n")

                damage_recieved = mob.damage / (1 + defense / 100)
                hp -= damage_recieved
                gray(f"You recieved {YELLOW}"
                     f"{shorten_number(damage_recieved)}{GRAY}"
                     f" damage from the {display_name(mob.name)}{GRAY}!\n")

                exp_npng = 0
                for npng_chance in no_pain_no_gain:
                    if random_bool(npng_chance / 100):
                        exp_npng += 10
                if exp_npng != 0:
                    self.add_exp(exp_npng)
                    gray(f"Your {LIGHT_PURPLE}{BOLD}No Pain No Gain{GRAY}"
                         f" enchantment granted you {GREEN}{exp_npng}"
                         f" experience point{GRAY}!\n")

                if hp <= 0:
                    self.die()
                    return

                if random_bool(0.5) and thorns != 0:
                    thorns_damage = (thorns / 100) * damage_recieved
                    mob_hp -= thorns_damage
                    gray(f"Your {BLUE}Thorns{GRAY} enchantment delt {YELLOW}"
                         f"{shorten_number(damage_delt)}{GRAY} {crit}damage"
                         f" to the {display_name(mob.name)}{GRAY}!\n")

                    if mob_hp <= 0:
                        a_an = 'an' if mob.name[0] in 'aeiou' else 'a'
                        green(f"You've killed {a_an} "
                              f"{display_name(mob.name)}{GRAY}!")
                        gray(f'Your HP: {AQUA}{shorten_number(hp)}{RED}❤')
                        break

                gray(f'Your HP: {AQUA}{shorten_number(hp)}{RED}❤')
                gray(f"{display_name(mob.name)}'s HP: "
                     f"{AQUA}{shorten_number(mob_hp)}{RED}❤\n\n")

                strike_count += 1

            if vampirism != 0 and hp != health:
                delta = (health - hp) * (vampirism / 100)
                hp += delta

                gray(f"Your {BLUE}Vampirism{GRAY} enchantment healed you for "
                     f"{AQUA}{shorten_number(delta)}{RED}❤{GRAY}!")

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

                loot = item.copy()
                if hasattr(loot, 'count'):
                    loot.count = 1

                self.recieve_item(loot, random_amount(count))

                if is_collection[loot.name]:
                    self.collect(loot.name, loot.count)

                if rarity not in {'common', 'uncommon'}:
                    rarity_str = rarity.upper()
                    white(f'{RARITY_COLORS[rarity]}{rarity_str} DROP! '
                          f'{WHITE}({item.display()}{WHITE})')

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
                  f"{GOLD}{display_number(interest)} coins{GREEN} "
                  f"as interest in your personal bank account!")

        self.play_time += dt

        self.last_update = now

    cls.update = update

    def warp(self, dest: str, /):
        island = get(ISLANDS, self.island)
        region = get(island.regions, self.region)

        for i_name, r_name in self.fast_travel:
            name = i_name if r_name is None else r_name
            if dest == name:
                self.island = i_name
                island = get(ISLANDS, self.island)
                self.region = island.spawn if r_name is None else r_name
                region = get(island.regions, self.region)
                gray(f'Warped to {AQUA}{region}{GRAY}'
                     f' of {AQUA}{island}{GRAY}.')
                return

        if dest == self.island:
            red(f'Already at island: {dest!r}')
            return

        if not includes(ISLANDS, dest):
            red("Unknown destination!"
                " Check the Fast Travel menu to view options!")
            return

        if dest == 'hub':
            pass
        elif getattr(region, 'portal', None) != dest:
            for _region in island.regions:
                if getattr(_region, 'portal', None) == dest:
                    self.goto(_region.name)
                    if self.region != _region.name:
                        return
                    region = _region
                    break
            else:
                red(f'Cannot warp to {dest}')
                return

        last = self.island
        island = get(ISLANDS, dest)

        if island.skill_req is not None:
            name, level = island.skill_req
            skill_exp = getattr(self, f'skill_xp_{name}')
            exp_lvl = calc_skill_exp(name, skill_exp)
            if exp_lvl < level:
                red(f'Cannot warp to {dest}!')
                red(f'Requires {name.capitalize()} level {roman(level)}')
                return

        self.island = dest
        region = get(island.regions, portal=last,
                     default=get(island.regions, island.spawn))
        self.region = region.name
        gray(f'Warped to {AQUA}{region}{GRAY} of {AQUA}{island}{GRAY}.')

    cls.warp = warp

    return cls
