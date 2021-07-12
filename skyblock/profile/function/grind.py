from decimal import Decimal
from math import ceil
from os import get_terminal_size
from random import randint, random
from time import sleep, time
from typing import Optional

from ...constant.ability import SET_BONUSES
from ...constant.color import *
from ...constant.mob import (
    CUBISM_EFT, ENDER_SLAYER_EFT, BOA_EFT, SMITE_EFT, BLAST_PROT_EFT,
    PROJ_PROT_EFT, IMPALING_EFT, SEA_CREATURES, ZOMBIES, SKELETONS,
)
from ...function.io import *
from ...function.math import (
    calc_bestiary_level, calc_pet_level, random_amount, random_bool, random_int,
)
from ...function.util import (
    checkpoint, format_crit, format_name, format_number, format_roman,
)
from ...object.fishing import FISHING_TABLE, SC_TABLE
from ...object.item import get_item, get_stone, validify_item
from ...object.mob import get_mob
from ...object.object import *
from ...object.resource import get_resource


__all__ = ['fish', 'gather', 'slay']


@checkpoint
def fish(self, rod_index: int, iteration: int = 1, /):
    rod = Empty() if rod_index is None else self.inventory[rod_index]

    if not isinstance(rod, (Empty, FishingRod)):
        rod = Empty()

    fishing_level = self.get_skill_level('fishing')

    fishing_req = getattr(rod, 'fishing_skill_req', None)
    if fishing_req is not None and fishing_req > fishing_level:
        red(f'You need Fishing {format_roman(fishing_req)} to use it!')
        return

    enchants = getattr(rod, 'enchantments', {})

    time_mult = 1 - enchants.get('lure', 0) * 0.05
    time_mult /= 1 + rod.get_stat('fishing_speed', self) / 100
    blessing = 0.05 * enchants.get('blessing', 0)
    expertise = 1 + 0.02 * enchants.get('expertise', 0)
    frail = 1 - 0.05 * enchants.get('frail', 0)
    luck = 1 + 0.01 * enchants.get('luck_of_the_sea', 0)
    luck += fishing_level * 0.002
    magnet = enchants.get('magnet', 0)

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
        if is_sc and fishing_level >= 1:
            avaliable_sc = [
                line for line in SC_TABLE
                if line[2] <= fishing_level
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
            for drop, amount, rarity, weight, fishing_exp in table:
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
                self.collect(drop.name, amount)

                if 'catch' in rarity:
                    rarity_display = rarity.upper().replace('_', ' ')
                    gray(f'{RARITY_COLORS[rarity]}{rarity_display}! {AQUA}'
                         f'You found a {item_type.display()}{AQUA}.')

            exp_gained = fishing_exp * expertise
            self.add_skill_exp('fishing', exp_gained, display=True)
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

    active_pet = self.get_active_pet()
    has_active_pet = isinstance(active_pet, Pet)
    if has_active_pet:
        pet_mult = calc_pet_level(active_pet.rarity, active_pet.exp) / 100
    else:
        pet_mult = 0

    if not isinstance(tool, (Empty, Axe, Hoe, Pickaxe, Drill)):
        tool = Empty()

    enchants = getattr(tool, 'enchantments', {})

    if isinstance(resource, Crop):
        time_cost = 0.4
        if self.has_item('farmer_orb'):
            time_cost -= 0.05

        farming_fortune = self.get_stat('farming_fortune', tool_index)
        fortune_mult = 1 + farming_fortune / 100
        drop_item = resource.name
        default_amount = resource.amount

        last_cp = Decimal()
        cp_step = Decimal('0.1')
        for i in range(1, iteration + 1):
            sleep(time_cost)
            amount_pool = random_amount(default_amount)
            drop_pool = random_int(fortune_mult)

            item_type = get_item(drop_item)
            if getattr(item_type, 'count', 1) != 1:
                item_type.count = 1
            self.recieve_item(item_type, amount_pool * drop_pool)
            self.collect(drop_item, amount_pool * drop_pool)

            if resource.name == 'wheat':
                seeds_pool = random_amount((0, 3))
                self.recieve_item(Item('seeds'), seeds_pool * drop_pool)
                self.collect('seeds', seeds_pool * drop_pool)

            self.add_skill_exp('farming', resource.farming_exp, display=True)
            if i >= (last_cp + cp_step) * iteration:
                while i >= (last_cp + cp_step) * iteration:
                    last_cp += cp_step
                gray(f'{i} / {iteration} ({(last_cp * 100):.0f}%) done')

    elif isinstance(resource, Mineral):
        magic_find = self.get_stat('magic_find', tool_index)

        breaking_power = tool.get_stat('breaking_power', self)
        mining_speed = tool.get_stat('mining_speed', self, default=50)
        if 'efficiency' in enchants:
            mining_speed += 10 + 20 * enchants['efficiency']

        if resource.breaking_power > breaking_power:
            red(f'Insufficient breaking power'
                f' for {format_name(resource.name)}!')
            return

        time_cost = 30 * resource.hardness / mining_speed

        mining_fortune = self.get_stat('mining_fortune', tool_index)
        fortune_mult = 1 + mining_fortune / 100
        exp_mult = 1 + 0.125 * enchants.get('experience', 0)
        if self.has_item('experience_artifact'):
            exp_mult *= 1.25

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
        for i in range(1, iteration + 1):
            sleep(time_cost)
            amount_pool = random_amount(default_amount)
            drop_pool = random_int(fortune_mult)
            item_type = get_item(drop_item)
            if getattr(item_type, 'count', 1) != 1:
                item_type.count = 1
            self.recieve_item(item_type, amount_pool * drop_pool)
            self.collect(drop_item, amount_pool * drop_pool)

            self.add_exp(random_amount(resource.exp) * random_amount(exp_mult))
            self.add_skill_exp('mining', resource.mining_exp, display=True)

            if resource.name == 'end_stone' and random_bool(0.1):
                self.slay(get_mob('endermite', level=37))

            if 'diamond' in resource.name:
                if random_bool(0.01 * (1 + magic_find / 100)):
                    loot = get_stone('rare_diamond')
                    self.recieve_item(loot)

                    rarity_color = RARITY_COLORS['rare']
                    white(f'{rarity_color}RARE DROP! '
                          f'{WHITE}({loot.display()}{WHITE})')

            mithril_powder = random_amount(resource.mithril_powder)
            if mithril_powder != 0:
                self.mithril_powder += mithril_powder
                dark_green(f'+ {format_number(mithril_powder)} Mithril Powder')

            if i >= (last_cp + cp_step) * iteration:
                while i >= (last_cp + cp_step) * iteration:
                    last_cp += cp_step
                gray(f'{i} / {iteration} ({(last_cp * 100):.0f}%) done')

            if 'mithril' in resource.name and randint(1, 50) == 1:
                white('Titanium has spawned nearby!')
                self.gather('titanium', tool_index)

    elif isinstance(resource, Wood):
        is_wood = True

        break_amount = 1
        cooldown = 0
        time_cost = 0.5
        if 'wood' not in resource.name:
            time_cost = 0.5
            is_wood = False
        elif getattr(tool, 'name', None) in {'jungle_axe', 'treecapitator'}:
            cooldown = 2
            if has_active_pet:
                if 'evolves_axes' in active_pet.abilities:
                    cooldown *= 1 - 0.5 * pet_mult
            break_amount = 10 if tool.name[0] == 'j' else 35
        else:
            if isinstance(tool, Axe):
                tool_speed = tool.tool_speed
                if 'efficiency' in enchants:
                    tool_speed += enchants['efficiency'] ** 2 + 1
                time_cost = 1.5 * resource.hardness / tool_speed
            else:
                tool_speed = 1
                time_cost = 5 * resource.hardness / tool_speed
            time_cost = ceil(time_cost * 20) / 20
        time_cost += cooldown

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

                self.add_skill_exp('foraging', resource.foraging_exp,
                                   display=True)

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

    if not isinstance(weapon, (Empty, Bow, Sword, FishingRod, Pickaxe, Drill)):
        weapon = Empty()

    catacombs_level = self.get_skill_level('catacombs')
    combat_level = self.get_skill_level('combat')
    fishing_level = self.get_skill_level('fishing')

    combat_req = getattr(weapon, 'combat_skill_req', None)
    if combat_req is not None and combat_req > combat_level:
        red(f'You need Combat {format_roman(combat_req)} to use it!')
        return
    cata_req = getattr(weapon, 'dungeon_skill_req', None)
    if cata_req is not None and cata_req > catacombs_level:
        red(f'You need Catacombs {format_roman(combat_req)} to use it!')
        return
    fishing_req = getattr(weapon, 'fishing_skill_req', None)
    if fishing_req is not None and fishing_req > fishing_level:
        red(f'You need Fishing {format_roman(fishing_req)} to use it!')
        return

    bestiary_level = calc_bestiary_level(self.stats.get(f'kills_{name}', 0))
    bestiary_stat = min(bestiary_level, 5)
    bestiary_stat += 2 * max(min(bestiary_level - 5, 5), 0)
    bestiary_stat += 3 * max(bestiary_level - 10, 0)

    health = self.get_stat('health', weapon_index)
    defense = self.get_stat('defense', weapon_index)
    true_defense = self.get_stat('true_defense', weapon_index)
    strength = self.get_stat('strength', weapon_index)
    strength += bestiary_stat
    speed = self.get_stat('speed', weapon_index)
    crit_chance = self.get_stat('crit_chance', weapon_index)
    crit_damage = self.get_stat('crit_damage', weapon_index)
    attack_speed = self.get_stat('attack_speed', weapon_index)
    # intelligence = self.get_stat('intelligence', weapon_index)
    attack_speed = self.get_stat('attack_speed', weapon_index)
    magic_find = self.get_stat('magic_find', weapon_index)
    magic_find += bestiary_stat
    ferocity = self.get_stat('ferocity', weapon_index)

    thorns = 0

    last_stand = 0
    no_pain_no_gain = []

    weapon_enchants = getattr(weapon, 'enchantments', {})

    weapon_dmg = 0
    if not isinstance(weapon, Empty):
        weapon_dmg = weapon.get_stat('damage', self)
        if weapon_enchants.get('ultimate_jerry', 0) != 0:
            weapon_dmg += weapon_enchants['ultimate_jerry'] * 10

    set_bonus = True
    for piece in self.armor:
        if not isinstance(piece, Armor):
            set_bonus = False
            break

        piece_enchants = getattr(piece, 'enchantments', {})

        if name in BLAST_PROT_EFT:
            defense += 30 * piece_enchants.get('blast_protection', 0)
        if name in PROJ_PROT_EFT:
            defense += 7 * piece_enchants.get('projectile_protection', 0)

        for current_ability in piece.abilities:
            if current_ability in SET_BONUSES:
                break
        else:
            continue
        if set_bonus is True:
            set_bonus = current_ability
        elif set_bonus is not False:
            if current_ability != set_bonus:
                set_bonus = False

    enchants = 0
    enchants += 0.05 * weapon_enchants.get('sharpness', 0)
    if name in SMITE_EFT:
        enchants += 0.08 * weapon_enchants.get('smite', 0)
    if name in BOA_EFT:
        enchants += 0.08 * weapon_enchants.get('bane_of_arthropods', 0)
    if name in ENDER_SLAYER_EFT:
        enchants += 0.12 * weapon_enchants.get('ender_slayer', 0)
    if name in CUBISM_EFT:
        enchants += 0.1 * weapon_enchants.get('cubism', 0)
    if name in IMPALING_EFT:
        enchants += 0.125 * weapon_enchants.get('impaling', 0)
    enchants += 0.08 * weapon_enchants.get('power', 0)
    enchants += 0.05 * weapon_enchants.get('spiked_hook', 0)

    crit_damage += 10 * weapon_enchants.get('critical', 0)
    ferocity += weapon_enchants.get('vicious', 0)

    healing_mult = 1

    for piece in self.armor:
        if not isinstance(piece, Armor):
            continue

        piece_enchants = getattr(piece, 'enchantments', {})
        healing_mult += 0.02 + piece_enchants.get('rejuvenate', 0)
        thorns += 3 * piece_enchants.get('thorns', 0)
        last_stand += 5 * piece_enchants.get('last_stand', 0)
        no_pain_no_gain.append(25 * piece_enchants.get('no_pain_no_gain', 0))

    if set_bonus == 'deflect':
        thorns += 33

    armor_bonuses = 0
    if set_bonus == 'pumpkin_buff':
        armor_bonuses *= 1.1

    enchanting_level = self.get_skill_level('enchanting')

    execute_level = 0.2 * weapon_enchants.get('execute_level', 0)
    prosecute_level = 0.1 * weapon_enchants.get('prosecute_level', 0)
    fire_aspect_level = weapon_enchants.get('fire_aspect_level', 0)
    first_strike = 0.25 * weapon_enchants.get('first_strike', 0)
    flame = weapon_enchants.get('flame', 0)
    giant_killer = weapon_enchants.get('giant_killer', 0)
    infinite_quiver = weapon_enchants.get('infinite_quiver', 0)
    knockback = 1 + 0.1 * weapon_enchants.get('knockback', 0)
    life_steal = 0.005 * weapon_enchants.get('life_steal', 0)
    if isinstance(weapon, Bow):
        looting = 1 + 0.15 * weapon_enchants.get('chance', 0)
    elif isinstance(weapon, Sword):
        looting = 1 + 0.15 * weapon_enchants.get('looting', 0)
    else:
        looting = 1
    luck = 1 + 0.05 * weapon_enchants.get('luck', 0)
    overload = weapon_enchants.get('overload', 0)
    prosecute = 0.1 * weapon_enchants.get('prosecute', 0)
    punch = 1 + 0.08 * weapon_enchants.get('punch', 0)
    scavenger = 0.3 * weapon_enchants.get('scavenger', 0)
    coins_mult = 1 + 0.01 * bestiary_level
    if 'syphon' in weapon_enchants:
        syphon = 0.1 + 0.1 * weapon_enchants['syphon']
    else:
        syphon = 0
    triple_strike = 0.1 * weapon_enchants.get('triple_strike', 0)
    thunderbolt = 0.15 * weapon_enchants.get('thunderbolt', 0)
    thunderlord_level = weapon_enchants.get('thunderlord', 0)
    if thunderlord_level <= 3:
        thunderlord = 0.3 * thunderlord_level
    elif thunderlord_level <= 5:
        thunderlord = 0.25 * thunderlord_level
    else:
        thunderlord = 0.3 * thunderlord_level
    vampirism = weapon_enchants.get('vampirism', 0)

    added_exp = 0.2 * bestiary_level
    added_coin = 0
    if self.has_item('scavenger_talisman'):
        added_coin = 20

    exp_mult = 1 + 0.125 * weapon_enchants.get('experience', 0)
    exp_mult *= 1 + 0.04 * enchanting_level
    if self.has_item('experience_artifact'):
        exp_mult *= 1.25

    damage_recieved_mult = 1
    if name in SEA_CREATURES:
        if self.has_item('sea_creature_artifact'):
            damage_recieved_mult *= 0.85
        elif self.has_item('sea_creature_ring'):
            damage_recieved_mult *= 0.9
        elif self.has_item('sea_creature_talisman'):
            damage_recieved_mult *= 0.95
    if name in ZOMBIES:
        if self.has_item('zombie_talisman'):
            damage_recieved_mult *= 0.95
    if name in SKELETONS:
        if self.has_item('skeleton_talisman'):
            damage_recieved_mult *= 0.95

    if self.has_item('intimidation_talisman') and mob.level <= 1:
        damage_recieved_mult = 0

    if set_bonus == 'pumpkin_buff':
        damage_recieved_mult *= 0.9

    if self.has_item('healing_ring'):
        healing_mult *= 1.1
    elif self.has_item('healing_talisman'):
        healing_mult *= 1.05

    soul_eater = weapon_enchants.get('soul_eater', 0) * 2
    soul_eater_strength = 0

    crit_chance += overload
    crit_damage += overload

    hp = health

    last_cp = Decimal()
    cp_step = Decimal('0.1')

    for count in range(1, iteration + 1):
        actual_speed = speed
        if set_bonus == 'young_blood' and hp >= health / 2:
            actual_speed += 70
        time_cost = 10 / (5 * actual_speed / 100)
        sleep(time_cost)

        width, _ = get_terminal_size()
        width = ceil(width * 0.85)
        aqua(f"{BOLD}{'':-^{width}}")

        healed = round((time_cost // 2) * (1.5 + health / 100), 1)
        if set_bonus == 'holy_blood':
            healed *= 3
        healed *= healing_mult
        hp = min(hp + healed, health)

        attack_time_cost = 1 / (1 + attack_speed / 100)
        sleep(1 / (speed / 100))

        mob_hp = mob.health

        gray(f'Your HP: {GREEN}{format_number(hp)}{GRAY}/'
             f'{GREEN}{format_number(health)}{RED}❤\n'
             f"{mob_name}'s HP: "
             f'{GREEN}{format_number(mob_hp)}{GRAY}'
             f'/{GREEN}{format_number(mob.health)}{RED}❤\n')

        while True:
            if isinstance(weapon, Bow) and infinite_quiver != 10:
                if not self.has_item('arrow', 1):
                    red("You don't have any arrows in your inventory!")
                    return
                if random_bool(1 - infinite_quiver / 10):
                    self.remove_item('arrow', 1)
            strike_count = 0

            killed = False

            strike_chance = 1 + ferocity / 100
            strike_chance = 1 + attack_speed / 100
            strike_chance *= knockback * punch

            sleep(attack_time_cost)

            for _ in range(random_int(strike_chance)):
                damage_dealt = 5 + weapon_dmg

                if strike_count % 3 == 2:
                    damage_dealt += thunderbolt
                    damage_dealt += thunderlord

                is_crit = False
                if random_bool(crit_chance / 100):
                    damage_dealt *= 1 + crit_damage / 100
                    if crit_chance >= 100 and random_bool(overload * 0.1):
                        damage_dealt *= 1.1
                    is_crit = True

                effective_strength = strength + soul_eater_strength
                damage_dealt *= 1 + effective_strength / 100

                if soul_eater_strength != 0:
                    soul_eater_strength = 0

                combat_level = self.get_skill_level('combat')

                effective_enchants = enchants

                if strike_count == 0:
                    effective_enchants += first_strike
                if strike_count < 3:
                    effective_enchants += triple_strike
                effective_enchants += (
                    giant_killer * (min(0.1 * (mob_hp - hp), 5) / 100)
                )
                effective_enchants += (
                    (execute_level / 100) * (mob.health - mob_hp)
                )
                effective_enchants += (
                    min(prosecute_level * (mob_hp / mob.health), 0.35)
                )
                damage_mult = 1 + enchants
                damage_mult += (
                    0.04 * min(combat_level, 50)
                    + 0.01 * max(min(combat_level - 50, 10), 0)
                )
                damage_dealt *= 1 + damage_mult

                damage_dealt += (
                    (2 + fire_aspect_level) * 0.5 *
                    fire_aspect_level * weapon_dmg
                )
                damage_dealt += flame * 15

                mob_hp = max(mob_hp - damage_dealt, 0)
                damage_display = format_number(damage_dealt)
                if is_crit:
                    damage_display = format_crit(damage_display)
                gray(f"You've dealt {YELLOW}{damage_display}{GRAY} damage.")

                healed = 0
                if life_steal != 0:
                    healed += life_steal * health
                if syphon != 0:
                    healed += syphon * health * (crit_damage // 100)
                hp = min(hp + healed, health)

                if mob_hp <= 0:
                    green(f"\nYou've killed a {mob_name}!")
                    soul_eater_strength = mob.damage * soul_eater
                    killed = True
                    break

                strike_count += 1

            if killed:
                break

            actual_defense = defense
            if set_bonus == 'protective_blood':
                actual_defense *= 1 + (1 - hp / health)

            if last_stand != 0 and hp / health < 0.4:
                actual_defense *= last_stand / 100

            damage_recieved = mob.damage / (1 + actual_defense / 100)
            damage_recieved *= damage_recieved_mult
            if damage_recieved != 0:
                hp = max(hp - damage_recieved, 0)
                gray(f"You've recieved {YELLOW}"
                     f"{format_number(damage_recieved)}{GRAY} damage.")

            true_damage_recieved = mob.true_damage / (1 + true_defense / 100)
            true_damage_recieved *= damage_recieved_mult
            if true_damage_recieved != 0:
                hp = max(hp - true_damage_recieved, 0)
                gray(f"You've recieved {YELLOW}"
                     f"{format_number(true_damage_recieved)}{GRAY}"
                     f" true damage.")

            exp_npng = 0
            for npng_chance in no_pain_no_gain:
                if random_bool(npng_chance / 100):
                    exp_npng += 10
            if exp_npng != 0:
                self.add_exp(exp_npng)

            if hp <= 0:
                red(f' ☠ {GRAY}You were killed by {mob_name}.')
                self.die(name)
                return False

            if random_bool(0.5) and thorns != 0:
                thorns_damage = (thorns / 100) * damage_recieved
                mob_hp -= thorns_damage

            mob_hp = max(mob_hp, 0)

            gray(f'Your HP: {GREEN}{format_number(hp)}{GRAY}/'
                 f'{GREEN}{format_number(health)}{RED}❤\n'
                 f"{mob_name}'s HP: "
                 f'{GREEN}{format_number(mob_hp)}{GRAY}'
                 f'/{GREEN}{format_number(mob.health)}{RED}❤\n')

            if mob_hp <= 0:
                green(f"\nYou've killed a {mob_name}!")
                soul_eater_strength = mob.damage * soul_eater
                break

        if 'kills' not in self.stats:
            self.stats['kills'] = 0
        self.stats['kills'] += 1
        self.add_kill(name)

        if vampirism != 0 and hp != health:
            hp += (health - hp) * (vampirism / 100)

        self.add_exp(mob.exp * random_int(exp_mult) + random_int(added_exp))

        for item, loot_amount, rarity, drop_chance in mob.drops:
            drop_chance *= looting
            drop_chance *= 1 + magic_find / 100
            if isinstance(item, Armor):
                drop_chance *= luck

            if not random_bool(drop_chance):
                continue

            loot = validify_item(item)
            if getattr(loot, 'count', 1) != 1:
                loot.count = 1

            amount_pool = random_amount(loot_amount)
            self.recieve_item(loot, amount_pool)
            self.collect(loot.name, amount_pool)

            if rarity not in {'common', 'uncommon'}:
                rarity_str = rarity.replace('_', ' ').upper()
                white(f'{RARITY_COLORS[rarity]}{rarity_str} DROP! '
                      f'{WHITE}({loot.display()}{WHITE})')

        if 'diamond' in name:
            if random_bool(0.01 * (1 + magic_find / 100)):
                loot = get_stone('rare_diamond')
                self.recieve_item(loot)

                rarity_color = RARITY_COLORS['rare']
                white(f'{rarity_color}RARE DROP! '
                      f'{WHITE}({loot.display()}{WHITE})')

        coins_recieved = (mob.coins + scavenger) * coins_mult + added_coin
        self.purse += coins_recieved
        gray(f'+ {GOLD}{format_number(coins_recieved)} Coins')

        if getattr(mob, 'farming_exp', 0) != 0:
            self.add_skill_exp('farming', mob.farming_exp, display=True)
        if getattr(mob, 'combat_exp', 0) != 0:
            self.add_skill_exp('combat', mob.combat_exp, display=True)
        if getattr(mob, 'fishing_exp', 0) != 0:
            self.add_skill_exp('fishing', mob.fishing_exp, display=True)

        phoenix_pool = random()
        if phoenix_pool <= 0.0000008:
            self.recieve_item(get_item('phoenix_pet', rarity='epic'))
            yellow(f'Wow! You found a {RED}Phoenix{YELLOW} pet!')
        elif phoenix_pool <= 0.000001:
            self.recieve_item(get_item('phoenix_pet', rarity='legendary'))
            yellow(f'Wow! You found a {RED}Phoenix{YELLOW} pet!')

        if count >= (last_cp + cp_step) * iteration:
            while count >= (last_cp + cp_step) * iteration:
                last_cp += cp_step
            gray(f'{count} / {iteration} ({(last_cp * 100):.0f}%) killed')

    width, _ = get_terminal_size()
    width = ceil(width * 0.85)
    aqua(f"{BOLD}{'':-^{width}}")

    return True


grind_functions = {
    name: globals()[name] for name in __all__
}
