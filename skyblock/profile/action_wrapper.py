from decimal import Decimal
from math import ceil
from time import sleep, time
from typing import Optional, Tuple

from ..constant.color import (
    RARITY_COLORS, BOLD, GOLD, GRAY, BLUE, GREEN,
    AQUA, RED, LIGHT_PURPLE, YELLOW, WHITE,
)
from ..constant.main import INTEREST_TABLE, SELL_PRICE
from ..constant.mob import ENDER_SLAYER_EFFECTIVE
from ..constant.util import Number
from ..function.io import gray, red, green, yellow, aqua, white
from ..function.math import (
    calc_skill_exp, random_amount, random_bool, random_int,
)
from ..function.util import (
    backupable, display_name, display_number, get, includes,
    roman, shorten_number,
)
from ..item.item import COLLECTION_ITEMS
from ..item.mob import get_mob
from ..item.object import (
    ItemType, Item, Empty, Bow, Sword, Armor,
    Axe, Hoe, Pickaxe, Crop, Mineral, Tree, Mob,
)
from ..item.resource import get_resource
from ..map.island import ISLANDS
from ..map.object import calc_dist, path_find

__all__ = ['profile_action']


def profile_action(cls):
    def buy(self, trade: Tuple[Number, ItemType], amount: int, /):
        price = trade[0] * amount
        if self.purse < price:
            red('Not enough coins!')
            return

        item = trade[1]

        self.purse -= price
        self.recieve(item, amount)

        green(f"You bought {item.display()}{GREEN} for "
              f"{GOLD}{shorten_number(price)} Coins{GREEN}!")

    cls.buy = buy

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
    def get_item(self, name: str, tool_index: Optional[int], amount: int, /):
        resource = get_resource(name)
        tool = Empty() if tool_index is None else self.inventory[tool_index]

        if not isinstance(tool, (Empty, Axe, Hoe, Pickaxe)):
            tool = Empty()

        enchantments = getattr(tool, 'enchantments', {})

        if isinstance(resource, Crop):
            time_cost = 0.4

            farming_lvl = calc_skill_exp('farming', self.skill_xp_farming)

            farming_fortune = (1 + 0.125 * enchantments.get('harvesting', 0)
                               + 0.04 * farming_lvl)
            drop_item = resource.drop
            default_amount = resource.amount

            last_cp = Decimal()
            cp_step = Decimal('0.1')
            is_collection = includes(COLLECTION_ITEMS, drop_item)
            for count in range(1, amount + 1):
                sleep(time_cost)
                drop_pool = random_int(farming_fortune)
                self.recieve(Item(drop_item), default_amount * drop_pool)
                if is_collection:
                    self.collect(drop_item, default_amount * drop_pool)

                self.add_skill_exp('farming', resource.farming_exp)
                if count >= (last_cp + cp_step) * amount:
                    while count >= (last_cp + cp_step) * amount:
                        last_cp += cp_step
                    gray(f'{count} / {amount} ({(last_cp * 100):.0f}%) done')

        elif isinstance(resource, Mineral):
            breaking_power = getattr(tool, 'breaking_power', 0)
            mining_speed = getattr(tool, 'mining_speed', 50)
            mining_speed = tool.mining_speed
            if 'efficiency' in enchantments:
                mining_speed += 10 + 20 * enchantments['efficiency']

            if resource.breaking_power > breaking_power:
                red(f'Insufficient breaking power for {resource.name}.')
                return

            time_cost = 30 * resource.hardness / mining_speed

            mining_lvl = calc_skill_exp('mining', self.skill_xp_mining)

            mining_fortune = (1 + 0.1 * enchantments.get('fortune', 0)
                              + 0.04 * mining_lvl)
            experience = 1 + 0.125 * enchantments.get('experience', 0)
            drop_item = resource.drop
            default_amount = resource.amount

            last_cp = Decimal()
            cp_step = Decimal('0.1')
            is_collection = includes(COLLECTION_ITEMS, drop_item)
            for count in range(1, amount + 1):
                sleep(time_cost)
                drop_pool = random_int(mining_fortune)
                self.recieve(Item(drop_item), default_amount * drop_pool)
                if is_collection:
                    self.collect(drop_item, default_amount * drop_pool)

                self.add_exp(resource.exp * random_int(experience))
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

            foraging_lvl = calc_skill_exp('foraging', self.skill_xp_foraging)
            foraging_fortune = 1 + 0.04 * foraging_lvl

            drop_item = resource.drop

            last_cp = Decimal()
            cp_step = Decimal('0.1')
            is_collection = includes(COLLECTION_ITEMS, drop_item)
            for count in range(1, amount + 1):
                sleep(time_cost)
                drop_pool = random_int(foraging_fortune)
                self.recieve(Item(drop_item), drop_pool)
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

        route = ' -> '.join(f'{region}' for region in path)
        aqua(f'Route: {route} ({float(accum_dist):.2f}m)')
        for target in path[1:]:
            if target.skill_req is not None:
                name, level = target.skill_req
                skill_exp = getattr(self, f'skill_xp_{name}')
                exp_lvl = calc_skill_exp(name, skill_exp)
                if exp_lvl < level:
                    red(f'Cannot warp to {dest}!')
                    red(f'Requires {name.capitalize()} level {roman(level)}')
                    return

            dist = calc_dist(region, target)
            time_cost = float(dist) / (5 * (self.base_speed / 100))
            green(f'Going from {region} to {target}...')
            gray(f'(time cost: {time_cost:.2f}s)')
            sleep(time_cost)
            self.region = target.name
            region = get(island.regions, target.name)

    cls.goto = goto

    def sell(self, index: int, /):
        island = get(ISLANDS, self.island)
        region = get(island.regions, self.region)

        if len(region.npcs) == 0:
            red('No NPCs around to sell the item.')
            return

        item = self.inventory[index]
        if item.name not in SELL_PRICE:
            red(f"Can't sell {item.display()}.")
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

        health = self.base_health
        defense = self.base_defense
        # true_defense = 0
        strength = self.base_strength
        speed = self.base_speed
        crit_chance = 30
        crit_damage = self.base_crit_damage
        # attack_speed = 0
        # intelligence = self.base_intelligence
        magic_find = 0
        ferocity = 0

        thorns = 0

        last_stand = 0
        no_pain_no_gain = []

        combat_lvl = calc_skill_exp('combat', self.skill_xp_combat)
        farming_lvl = calc_skill_exp('farming', self.skill_xp_farming)
        foraging_lvl = calc_skill_exp('foraging', self.skill_xp_foraging)
        mining_lvl = calc_skill_exp('mining', self.skill_xp_mining)

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
                     f"enchantment granted {GREEN}+ {additional_damage}"
                     f" {GRAY}additional weapon base damage!\n")
            damage += additional_damage + weapon.hot_potato

            strength += weapon.hot_potato
            crit_chance += weapon.crit_chance
            crit_damage += weapon.crit_damage
            ferocity += weapon.ferocity

            damage *= 1 + 0.08 * enchantments.get('power', 0)
            damage *= 1 + 0.05 * enchantments.get('sharpness', 0)
            if name in ENDER_SLAYER_EFFECTIVE:
                damage *= 1 + 0.12 * enchantments.get('ender_slayer', 0)
            crit_damage += 10 * enchantments.get('critical', 0)
            ferocity += enchantments.get('vicious', 0)
        else:
            damage = 5

        rejuvenate = 0

        for piece in self.armor:
            if not isinstance(piece, Armor):
                continue

            strength += piece.strength
            health += piece.health
            defense += piece.health
            speed += piece.health

            # intelligence += ench.get('big_brain', 0) * 5
            ench = getattr(piece, 'enchantments', {})
            health += ench.get('growth', 0) * 15
            rejuvenate += ench.get('rejuvenate', 0) * 2
            defense += ench.get('protection', 0) * 8
            thorns += ench.get('thorns', 0) * 3
            # true_defense += ench.get('true_protection', 0) * 5
            last_stand += ench.get('last_stand', 0) * 5
            no_pain_no_gain.append(ench.get('no_pain_no_gain', 0) * 25)

        strength += min(foraging_lvl, 14) * 1
        strength += max(min(foraging_lvl - 14, 36), 0) * 2
        crit_chance += combat_lvl * 0.5
        defense += min(mining_lvl, 14) * 1
        defense += max(min(mining_lvl - 14, 46), 0) * 2
        health += min(farming_lvl, 14) * 2
        health += max(min(farming_lvl - 14, 5), 0) * 3
        health += max(min(farming_lvl - 19, 6), 0) * 4
        health += max(min(farming_lvl - 25, 35), 0) * 5

        damage *= 1 + 0.04 * combat_lvl

        time_cost = 2 / (speed / 100)

        execute = 0.2 * enchantments.get('execute', 0)
        experience = 1 + 0.125 * enchantments.get('experience', 0)
        first_strike = 1 + 0.25 * enchantments.get('first_strike', 0)
        giant_killer = enchantments.get('giant_killer', 0)
        life_steal = 0.5 * enchantments.get('life_steal', 0)
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
                     f'{RED}♥{GRAY}.')

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
                        hp += delta

                        gray(f"Your {BLUE}Life Steal{GRAY} "
                             f"enchantment healed you for {AQUA}"
                             f"{shorten_number(delta)}{RED}♥{GRAY}!\n")

                    if syphon != 0:
                        delta = min(health - hp,
                                    syphon * health * (crit_damage // 100))
                        if delta != 0:
                            hp += delta

                            gray(f"Your {BLUE}Syphon{GRAY} "
                                 f"enchantment healed you for {AQUA}"
                                 f"{shorten_number(delta)}{RED}♥{GRAY}!\n")

                if mob_hp <= 0:
                    a_an = 'an' if mob.name[0] in 'aeiou' else 'a'
                    green(f"You've killed {a_an} "
                          f"{display_name(mob.name)}!\n\n")
                    soul_eater_strength = mob.damage * soul_eater
                    break

                actual_defense = defense
                if last_stand != 0 and hp / health < 0.4:
                    additional_defense = actual_defense * (last_stand / 100)
                    actual_defense += additional_defense
                    gray(f"Your {LIGHT_PURPLE}{BOLD}Last Stand{GRAY}"
                         f" enchantment granted you {GREEN}+"
                         f" {additional_defense} ☘ Defense{GRAY}!\n")

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
                    gray(f"Your {LIGHT_PURPLE}{BOLD}No Pain No Gain{GRAY}"
                         f" enchantment granted you {GREEN}{exp_npng}"
                         f" experience point{GRAY}!\n")
                    self.add_exp(exp_npng)

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
                        gray(f'Your HP: {AQUA}{shorten_number(hp)}{RED}♥')
                        break

                gray(f'Your HP: {AQUA}{shorten_number(hp)}{RED}♥')
                gray(f"{display_name(mob.name)}'s HP: "
                     f"{AQUA}{shorten_number(mob_hp)}{RED}♥\n\n")

                strike_count += 1

            if vampirism != 0 and hp != health:
                delta = (health - hp) * (vampirism / 100)
                hp += delta

                gray(f"Your {BLUE}Vampirism{GRAY} enchantment healed you for "
                     f"{AQUA}{shorten_number(delta)}{RED}♥{GRAY}!")

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

                self.recieve(loot, random_amount(count))

                if is_collection[loot.name]:
                    self.collect(loot.name, loot.count)

                if rarity not in {'common', 'uncommon'}:
                    rarity_str = rarity.upper()
                    white(f'{RARITY_COLORS[rarity]}{rarity_str} DROP! '
                          f'({item.display()}{WHITE})')

            if count >= (last_cp + cp_step) * amount:
                while count >= (last_cp + cp_step) * amount:
                    last_cp += cp_step
                gray(f'{count} / {amount} ({(last_cp * 100):.0f}%) killed')

            gray('\n')

    cls.slay = slay

    def update(self, /):
        now = int(time())
        last = now if self.last_update == 0 else self.last_update
        # dt = now - last

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

        self.last_update = now

    cls.update = update

    @backupable
    def warp(self, dest: str, /):
        island = get(ISLANDS, self.island)
        region = get(island.regions, self.region)

        if not includes(ISLANDS, dest):
            red(f'Island not found: {dest!r}')
            return
        if dest == self.island:
            yellow(f'Already at island: {dest!r}')
            return

        if getattr(region, 'portal', None) != dest:
            yellow(f'Cannot warp to {dest}')
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
        region = get(island.regions, portal=last)
        self.region = region.name
        gray(f'Warped to {AQUA}{region}{GRAY} of {AQUA}{island}{GRAY}.')

    cls.warp = warp

    return cls
