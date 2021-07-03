from decimal import Decimal
from math import ceil
from random import randint, random
from time import sleep, time
from typing import Optional

from ...constant.color import (
    RARITY_COLORS, GOLD, GRAY, GREEN, AQUA, RED, YELLOW, WHITE,
)
from ...constant.mob import (
    CUBISM_EFT, ENDER_SLAYER_EFT, BOA_EFT, SMITE_EFT, IMPALING_EFT,
)
from ...function.io import gray, red, green, white
from ...function.math import random_amount, random_bool, random_int
from ...function.util import (
    checkpoint, format_name, format_number, format_roman, format_short,
)
from ...object.collection import is_collection
from ...object.fishing import FISHING_TABLE, SEA_CREATURES
from ...object.item import get_item, validify_item
from ...object.mob import get_mob
from ...object.object import (
    Item, Empty, Bow, Sword, Armor, Axe, Hoe, Pickaxe, Drill, FishingRod,
    Crop, Mineral, Wood, Mob,
)
from ...object.resource import get_resource


__all__ = ['fish', 'gather', 'slay']


@checkpoint
def fish(self, rod_index: int, iteration: int = 1, /):
    rod = Empty() if rod_index is None else self.inventory[rod_index]

    if not isinstance(rod, (Empty, FishingRod)):
        rod = Empty()

    fishing_lvl = self.get_skill_lvl('fishing')

    fishing_req = getattr(rod, 'fishing_skill_req', None)
    if fishing_req is not None and fishing_req > fishing_lvl:
        red(f'You need Fishing {format_roman(fishing_req)} to use it!')
        return

    enchantments = getattr(rod, 'enchantments', {})

    time_mult = 1 - enchantments.get('lure', 0) * 0.05
    time_mult /= 1 + getattr(rod, 'fishing_speed', 0) / 100
    blessing = 0.05 * enchantments.get('blessing', 0)
    expertise = 1 + 0.02 * enchantments.get('expertise', 0)
    frail = 1 - 0.05 * enchantments.get('frail', 0)
    luck = 1 + 0.01 * enchantments.get('luck_of_the_sea', 0)
    luck += fishing_lvl * 0.002
    magnet = enchantments.get('magnet', 0)

    sea_creature_chance = self.get_stat('sea_creature_chance')

    zone = self.zone
    table = [
        line[:-1] for line in FISHING_TABLE
        if len(line[-1]) == 0 or zone in line[-1]
    ]

    total_weight = 0
    for choice in table:
        if 'catch' in choice[2]:
            total_weight += choice[3] * luck
        else:
            total_weight += choice[3]

    last_cp = Decimal()
    cp_step = Decimal('0.1')
    for i in range(1, iteration + 1):
        sleep(random_amount((5, 30)) * time_mult)
        if i != 1:
            print()

        is_sc = random_bool(sea_creature_chance / 100)
        if is_sc and fishing_lvl >= 1:
            avaliable_sc = [
                line for line in SEA_CREATURES
                if line[2] <= fishing_lvl
            ]
            total_sc_weight = sum(line[1] for line in avaliable_sc)

            pool = random() * total_sc_weight
            for mob, weight, _, text in avaliable_sc:
                if pool < weight:
                    break
                pool -= weight

            green(text)
            sleep(1)

            mob_copy = mob.copy()
            mob_copy.health *= frail

            alive = self.slay(mob_copy, rod_index)
            if not alive:
                return

        else:
            pool = random() * total_weight
            for drop, amount, rarity, weight, exp in table:
                if 'catch' in rarity:
                    weight *= luck
                if pool < weight:
                    break
                pool -= weight

            if isinstance(drop, (int, float, tuple)):
                if isinstance(drop, tuple):
                    drop = random_amount(drop)
                if random_bool(blessing):
                    green('Your Blessing enchant got you double drops!')
                    drop *= 2

                self.purse += drop

                drop_display = format_number(drop)
                if drop_display.endswith('.0'):
                    drop_display = drop_display[:-2]

                if 'catch' in rarity:
                    rarity_display = rarity.upper().replace('_', ' ')
                    gray(f'{RARITY_COLORS[rarity]}{rarity_display}! {AQUA}'
                         f'You found {GOLD}{format_number(drop)} Coins{AQUA}.')
            else:
                item_type = drop.copy()
                if getattr(item_type, 'count', 1) != 1:
                    item_type.count = 1

                if random_bool(blessing):
                    green('Your Blessing enchant got you double drops!')
                    amount *= 2

                self.recieve_item(item_type, amount)
                if is_collection(drop.name):
                    self.collect(drop.name, amount)

                if 'catch' in rarity:
                    rarity_display = rarity.upper().replace('_', ' ')
                    gray(f'{RARITY_COLORS[rarity]}{rarity_display}! {AQUA}'
                         f'You found a {item_type.display()}{AQUA}.')

            self.add_skill_exp('fishing', exp * expertise)
            self.add_exp(random_amount((1, 6)) + magnet)

        if i >= (last_cp + cp_step) * iteration:
            while i >= (last_cp + cp_step) * iteration:
                last_cp += cp_step
            gray(f'{i} / {iteration} ({(last_cp * 100):.0f}%) done')


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
            self.recieve_item(item_type, amount_pool * drop_pool)
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

            if resource.name == 'end_stone' and random_bool(0.1):
                self.slay(get_mob('endermite', level=37))

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


@checkpoint
def slay(self, mob: Mob, weapon_index: Optional[int], iteration: int = 1,
         /) -> bool:
    name = mob.name
    mob_name = format_name(name)

    weapon = (Empty() if weapon_index is None
              else self.inventory[weapon_index])

    if not isinstance(weapon, (Empty, Bow, Sword, FishingRod)):
        weapon = Empty()

    cata_lvl = self.get_skill_lvl('catacombs')
    combat_lvl = self.get_skill_lvl('combat')
    fishing_lvl = self.get_skill_lvl('fishing')

    combat_req = getattr(weapon, 'combat_skill_req', None)
    if combat_req is not None and combat_req > combat_lvl:
        red(f'You need Combat {format_roman(combat_req)} to use it!')
        return
    cata_req = getattr(weapon, 'dungeon_skill_req', None)
    if cata_req is not None and cata_req > cata_lvl:
        red(f'You need Catacombs {format_roman(combat_req)} to use it!')
        return
    fishing_req = getattr(weapon, 'fishing_skill_req', None)
    if fishing_req is not None and fishing_req > fishing_lvl:
        red(f'You need Fishing {format_roman(fishing_req)} to use it!')
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

    enchantments = getattr(weapon, 'enchantments', {})

    farm_armor_speed = False
    farm_suit_speed = False
    pumpkin_buff = False
    deflect = False
    protective_blood = False
    holy_blood = False
    young_blood = False

    if not isinstance(weapon, Empty):
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
                        or self.zone == 'farm'):
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

        damage *= 1 + 0.08 * enchantments.get('power', 0)
        damage *= 1 + 0.05 * enchantments.get('sharpness', 0)
        damage *= 1 + 0.05 * enchantments.get('spiked_hook', 0)
        if name in CUBISM_EFT:
            damage *= 1 + 0.1 * enchantments.get('cubism', 0)
        if name in ENDER_SLAYER_EFT:
            damage *= 1 + 0.12 * enchantments.get('ender_slayer', 0)
        if name in BOA_EFT:
            damage *= 1 + 0.08 * enchantments.get('bane_of_arthropods', 0)
        if name in SMITE_EFT:
            damage *= 1 + 0.08 * enchantments.get('smite', 0)
        if name in IMPALING_EFT:
            damage *= 1 + 0.125 * enchantments.get('impaling', 0)

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

    enchanting_lvl = self.get_skill_lvl('enchanting')

    execute = 0.2 * enchantments.get('execute', 0)
    experience = 1 + 0.125 * enchantments.get('experience', 0)
    experience += 0.04 * enchanting_lvl
    first_strike = 1 + 0.25 * enchantments.get('first_strike', 0)
    giant_killer = enchantments.get('giant_killer', 0)
    infinite_quiver = enchantments.get('infinite_quiver', 0)
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
    for count in range(1, iteration + 1):
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
            gray(f'You healed for {GREEN}{format_short(healed)}'
                 f'{RED}❤{GRAY}.\n'
                 f'Your HP: {GREEN}{format_short(hp)}{GRAY}/'
                 f'{GREEN}{format_short(health)}{RED}❤')
        healed = 0

        mob_hp = mob.health
        while True:
            if isinstance(weapon, Bow) and infinite_quiver != 10:
                if not self.has_item('arrow', 1):
                    red("You don't have any arrows in your inventory!")
                    return
                if random_bool(1 - infinite_quiver / 10):
                    self.remove_item('arrow', 1)
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
                gray(f"You've dealt {YELLOW}{format_short(damage_dealt)}"
                     f'{GRAY} {crit}damage to the {mob_name}!')

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
                     f'{GREEN}{format_short(mob_hp)}{GRAY}'
                     f'/{GREEN}{format_short(mob.health)}{RED}❤')

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
                     f'{format_short(damage_recieved)}{GRAY}'
                     f' damage from the {mob_name}{GRAY}!')

            exp_npng = 0
            for npng_chance in no_pain_no_gain:
                if random_bool(npng_chance / 100):
                    exp_npng += 10
            if exp_npng != 0:
                self.add_exp(exp_npng)

            if hp <= 0:
                if self.die():
                    red(f' ☠ {GRAY}You were killed by {mob_name}.')
                return False

            if random_bool(0.5) and thorns != 0:
                thorns_damage = (thorns / 100) * damage_recieved
                mob_hp -= thorns_damage

                if mob_hp <= 0:
                    a_an = 'an' if mob.name[0] in 'aeiou' else 'a'
                    green(f"You've killed {a_an} {mob_name}{GRAY}!\n"
                          f'Your HP: {GREEN}{format_short(hp)}{GRAY}/'
                          f'{GREEN}{format_short(health)}{RED}❤')
                    break

            gray(f'Your HP: {GREEN}{format_short(hp)}{GRAY}/'
                 f'{GREEN}{format_short(health)}{RED}❤\n'
                 f"{mob_name}'s HP: "
                 f'{GREEN}{format_short(mob_hp)}{GRAY}'
                 f'/{GREEN}{format_short(mob.health)}{RED}❤\n')

            strike_count += 1

        if vampirism != 0 and hp != health:
            delta = (health - hp) * (vampirism / 100)
            hp += delta

        self.purse += mob.coins + scavenger
        self.add_exp(mob.exp * random_int(experience))
        if getattr(mob, 'combat_xp', 0) != 0:
            self.add_skill_exp('combat', mob.combat_xp)
        if getattr(mob, 'fishing_xp', 0) != 0:
            self.add_skill_exp('fishing', mob.fishing_xp)

        for item, loot_amount, rarity, drop_chance in mob.drops:
            drop_chance *= looting
            drop_chance *= 1 + magic_find / 100
            if isinstance(item, Armor):
                drop_chance *= luck

            if not random_bool(drop_chance):
                continue

            loot = validify_item(item)

            self.recieve_item(loot, random_amount(loot_amount))

            if is_coll[loot.name]:
                self.collect(loot.name, random_amount(loot_amount))

            if rarity not in {'common', 'uncommon'}:
                rarity_str = rarity.replace('_', ' ').upper()
                white(f'{RARITY_COLORS[rarity]}{rarity_str} DROP! '
                      f'{WHITE}({loot.display()}{WHITE})')

        if count >= (last_cp + cp_step) * iteration:
            while count >= (last_cp + cp_step) * iteration:
                last_cp += cp_step
            gray(f'{count} / {iteration} ({(last_cp * 100):.0f}%) killed')

        if count != iteration:
            gray('\n')

    return True


grind_functions = {
    name: globals()[name] for name in __all__
}
