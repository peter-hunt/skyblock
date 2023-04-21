from bdb import effective
from decimal import Decimal
from math import ceil, floor
from os import get_terminal_size
from random import randint, random, vonmisesvariate
from time import sleep, time

from ...constant.ability import *
from ...constant.colors import *
from ...constant.mobs import *
from ...constant.resource import *
from ...function.io import *
from ...function.math import calc_bestiary_level, calc_pet_level
from ...function.random import random_amount, random_bool, random_int
from ...function.util import (
    checkpoint, format_crit, format_name, format_number, format_rarity, format_roman,
)
from ...object.fishing import FISHING_TABLE, SEA_CREATRUE_TABLE
from ...object.items import get_item
from ...object.mobs import get_mob
from ...object.object import *
from ...object.resources import get_resource


__all__ = ['fish', 'gather', 'slay']



@checkpoint
def _fish_choose_weapon(self) -> int:
    while True:
        green('Please enter the index of weapon to slay the sea creature:')
        cmd = input(']> ').strip()
        index = self.parse_index(cmd)
        if index is not None:
            return index


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
    frail_mult = 1 - 0.05 * enchants.get('frail', 0)
    treasure_chance = 0.05 + 0.01 * enchants.get('luck_of_the_sea', 0)
    treasure_chance += fishing_level * 0.002
    magnet = enchants.get('magnet', 0)

    sea_creature_chance = self.get_stat('sea_creature_chance')

    fishing_exp_mult = 1 + 0.02 * enchants.get('expertise', 0)
    use_expertise = enchants.get('expertise', 0) != 0

    zone = self.zone
    table = FISHING_TABLE
    tables = [
        [line for line in table if line[1] == 'normal'],
        [line for line in table if line[1] == 'good_catch'],
        [line for line in table if line[1] == 'great_catch'],
    ]
    total_weights = [
        sum(line[2] for line in table if line[1] == 'normal'),
        sum(line[2] for line in table if line[1] == 'good_catch'),
        sum(line[2] for line in table if line[1] == 'great_catch'),
    ]

    last_cp = Decimal()
    cp_step = Decimal('0.1')
    for i in range(1, iteration + 1):
        sleep(random_amount((0.5, 3), mult=time_mult))
        if i != 1:
            print()
        is_sc = random_bool(sea_creature_chance / 100)

        if is_sc and fishing_level >= 1:
            avaliable_sc = [line for line in SEA_CREATRUE_TABLE
                            if line[2] <= fishing_level]
            total_sc_weight = sum(line[1] for line in avaliable_sc)

            pool = random() * total_sc_weight
            for mob_name, weight, _, text in avaliable_sc:
                if pool < weight:
                    break
                pool -= weight

            green(text)
            sleep(1)

            mob = get_mob(mob_name).copy()
            mob.health *= frail_mult

            weapon_index = _fish_choose_weapon(self)
            if weapon_index is None:
                continue
            alive = self.slay(mob, weapon_index)
            if not alive:
                return
            if 'sea_creature_killed' not in self.stats:
                self.stats['sea_creature_killed'] = 0
            self.stats['sea_creature_killed'] += 1
            sea_creature_killed = self.stats['sea_creature_killed']
            dolphin_pet_rarity = {250: 'common', 1000: 'uncommon', 2500: 'rare',
                                  5000: 'epic', 10000: 'legendary'}.get(sea_creature_killed, '')
            if dolphin_pet_rarity:
                pet_item = get_item('dolphin_pet', rarity=dolphin_pet_rarity)
                green(f'You reached a new Sea Creature Killed Milestone of {BLUE}{sea_creature_killed} {GREEN}kills!')
                green(f'A wild {pet_item.display()} {GREEN}has decided to befriend you!')
                self.recieve_item(pet_item.to_obj())

            if use_expertise:
                self.inventory[rod_index].expertise_count += 1
                expertise_count = self.inventory[rod_index].expertise_count
                expertise_level = {50: 2, 100: 3, 250: 4, 500: 5,
                                   1000: 6, 2500: 7, 5500: 8, 10000: 9, 15000: 10}.get(expertise_count, 0)
                if expertise_level != 0:
                    self.inventory[rod_index].enchantments['expertise'] = expertise_level
                    fishing_exp_mult = 1 + 0.02 * expertise_level
                    blue(f'Expertise {format_roman(expertise_level - 1)} {YELLOW}on your {rod.display()}'
                         f' {YELLOW}was upgraded to {BLUE}Expertise {format_roman(expertise_level)}{YELLOW}!')

        else:
            if random_bool(0.000_000_066_7):
                rarity = 'outstanding_catch'
                item = get_item('aquamarine_dye')
                white(f'{RARITY_COLORS[rarity]}OUTSTANDING CATCH! {AQUA}'
                        f'You found a {item.display()}{AQUA}.')
                self.recieve_item(item.to_obj())
                continue
            if zone == 'wilderness':
                if random_bool(0.000_000_1):
                    rarity = 'great_catch'
                    item = get_item('nadeshiko_dye')
                    white(f'{RARITY_COLORS[rarity]}GREAT CATCH! {AQUA}'
                            f'You found a {item.display()}{AQUA}.')
                    self.recieve_item(item.to_obj())
                continue
            if self.island == 'jerry':
                if random_bool(0.000_000_1):
                    rarity = 'great_catch'
                    item = get_item('iceberg_dye')
                    white(f'{RARITY_COLORS[rarity]}GREAT CATCH! {AQUA}'
                            f'You found a {item.display()}{AQUA}.')
                    self.recieve_item(item.to_obj())
                continue

            if random_bool(treasure_chance):
                is_treasure = True
                if random_bool(0.1):
                    table, total_weight = tables[2], total_weights[2]
                else:
                    table, total_weight = tables[1], total_weights[1]
            else:
                is_treasure = False
                table, total_weight = tables[0], total_weights[0]
            pool = random() * total_weight
            for drop, rarity, weight, fishing_exp, zone in table:
                if pool < weight:
                    break
                pool -= weight

            if isinstance(drop, (int, float, list)):
                if isinstance(drop, list):
                    drop = random_amount(tuple(drop))
                if random_bool(blessing):
                    green('Your Blessing enchant got you double drops!')
                    drop *= 2

                self.purse += drop

                drop_display = format_number(drop)
                if drop_display.endswith('.0'):
                    drop_display = drop_display[:-2]
                if is_treasure:
                    gray(f'{RARITY_COLORS[rarity]}{format_rarity(rarity)}! {AQUA}'
                         f'You found {GOLD}{format_number(drop)} Coins{AQUA}.')
            else:
                if random_bool(blessing):
                    green('Your Blessing enchant got you double drops!')
                    drop['count'] = 2

                drop_name = drop['name']
                drop_kwargs = {key: drop[key] for key in drop
                               if key not in {'name', 'count'}}
                drop_item = get_item(drop_name, **drop_kwargs)
                if getattr(drop_item, 'count', 1) != 1:
                    drop_item.count = 1

                self.recieve_item(drop)
                self.collect(drop_name, drop.get('count', 1))

                if is_treasure:
                    gray(f'{RARITY_COLORS[rarity]}{format_rarity(rarity)}! {AQUA}'
                         f'You found a {drop_item.display()}{AQUA}.')

            self.add_skill_exp('fishing', random_amount(fishing_exp, mult=fishing_exp_mult), display=True)
            self.add_exp(random_amount(random_amount((1, 6)) + magnet))

        if i >= (last_cp + cp_step) * iteration:
            while i >= (last_cp + cp_step) * iteration:
                last_cp += cp_step
            perc = floor((i / iteration) * 100)
            gray(f'{i} / {iteration} ({perc}%) done')


@checkpoint
def gather(self, name: str, tool_index: int | None,
           iteration: int | None = 1, /):
    resource = get_resource(name)
    tool = Empty() if tool_index is None else self.inventory[tool_index]
    iteration = 1 if iteration is None else iteration

    magic_find = self.get_stat('magic_find', tool_index)
    magic_find_str = f'{AQUA}(+{format_number(magic_find)}% Magic Find!)'

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
        time_cost = 0.1
        if self.has_item({'name': 'farmer_orb'}):
            time_cost -= 0.02

        drop_item = resource.name
        default_amount = resource.amount
        farming_exp_mult = 1 + 0.01 * enchants.get('cultivating', 0)
        use_cultivating = enchants.get('cultivating', 0) != 0

        last_cp = Decimal()
        cp_step = Decimal('0.1')
        for i in range(1, iteration + 1):
            sleep(time_cost)
            farming_fortune = self.get_stat('farming_fortune', tool_index)
            fortune_mult = 1 + farming_fortune / 100

            count_pool = random_amount(default_amount, mult=fortune_mult)

            if use_cultivating:
                self.inventory[tool_index].cultivating_count += 1
                cultivating_count = self.inventory[tool_index].cultivating_count
                cultivating_level = {1000: 2, 5000: 3, 25000: 4, 100000: 5, 300000: 6, 1500000: 7,
                                     5000000: 8, 20000000: 9, 100000000: 10}.get(cultivating_count, 0)
                if cultivating_level != 0:
                    self.inventory[tool_index].enchantments['cultivating'] = cultivating_level
                    farming_exp_mult = 1 + 0.01 * enchants.get('cultivating', 0)
                    blue(f'Cultivating {format_roman(cultivating_level - 1)} {YELLOW}on your {tool.display()}'
                         f' {YELLOW}was upgraded to {BLUE}Cultivating {format_roman(cultivating_level)}{YELLOW}!')

            self.recieve_item({'name': drop_item, 'count': count_pool})
            self.collect(drop_item, count_pool)

            if resource.name == 'wheat':
                seeds_pool = random_amount((0, 3), mult=fortune_mult)
                if seeds_pool != 0:
                    self.recieve_item({'name': 'seeds', 'count': seeds_pool})
                    self.collect('seeds', seeds_pool)

            self.add_skill_exp('farming', random_amount(resource.farming_exp, mult=farming_exp_mult), display=True)

            if random_bool((0.000_000_125) * (1 + magic_find / 100)):
                rarity = 'rngesus'
                item = get_item('wild_strawberry_dye')
                white(f'{RARITY_COLORS[rarity]}{format_rarity(rarity)} DROP! '
                        f'{WHITE}({item.display()}{WHITE}) {magic_find_str}')
                self.recieve_item(item.to_obj())

            if i >= (last_cp + cp_step) * iteration:
                while i >= (last_cp + cp_step) * iteration:
                    last_cp += cp_step
                perc = floor((i / iteration) * 100)
                gray(f'{i} / {iteration} ({perc}%) done')

    elif isinstance(resource, Log):
        is_wood = True

        break_amount = 1
        cooldown = 0
        time_cost = 0.5
        if 'log' not in resource.name:
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

        wood_name = resource.name.replace('_log', '_wood')

        magic_find = self.get_stat('magic_find', tool_index)
        magic_find_str = f'{AQUA}(+{format_number(magic_find)}% Magic Find!)'

        last_cp = Decimal()
        cp_step = Decimal('0.1')
        last_harvest = time()
        for i in range(1, iteration + 1):
            sleep(max(last_harvest - time() + time_cost, 0))

            foraging_fortune = self.get_stat('foraging_fortune', tool_index)
            fortune_mult = 1 + foraging_fortune / 100

            last_harvest = time()
            count_pool = random_int(fortune_mult)

            for i in range(break_amount):
                if i != 0:
                    sleep(0.02)

                self.recieve_item({'name': wood_name, 'count': count_pool})
                if is_wood:
                    self.collect(wood_name, count_pool)
                    if random_amount((1, 5)) == 1:
                        self.recieve_item({'name': f'{wood_name[:-5]}_sapling',
                                           'count': 1})

                self.add_skill_exp('foraging', resource.foraging_exp,
                                   display=True)

                if random_bool((0.000_000_1) * (1 + magic_find / 100)):
                    rarity = 'rngesus'
                    item = get_item('mango_dye')
                    white(f'{RARITY_COLORS[rarity]}{format_rarity(rarity)} DROP! '
                          f'{WHITE}({item.display()}{WHITE}) {magic_find_str}')
                    self.recieve_item(item.to_obj())

            if i >= (last_cp + cp_step) * iteration:
                while i >= (last_cp + cp_step) * iteration:
                    last_cp += cp_step
                gray(f'{i} / {iteration} ({(last_cp * 100):.0f}%) done')

    elif isinstance(resource, Mineral):
        count_ore = resource.name not in {'stone', 'netherrack', 'end_stone'}

        breaking_power = tool.get_stat('breaking_power', self)

        mining_speed = self.get_stat('mining_speed', tool_index)
        is_gemstone = resource.name in GEMSTONES
        if is_gemstone:
            mining_speed += tool.get_stat('gemstone_mining_speed', self)

        if resource.breaking_power > breaking_power:
            red(f'You need a strong tool to mine {format_name(resource.name)}.')
            return

        time_cost = 30 * resource.hardness / mining_speed

        exp_mult = 1
        if getattr(tool, 'modifier') == 'magnetic':
            tool_rarity = tool.rarity[0]
            tool_rarity_index = 'cureldsv'.index(tool_rarity)
            exp_mult *= (1.1, 1.12, 1.14, 1.16, 1.18, 1.2, 1.22, 1.24, 1.26)[tool_rarity_index]

        lapis_exp_bonus = 1

        for piece in self.armor:
            if not isinstance(piece, Armor):
                break

            if piece.name in {'lapis_helmet', 'lapis_chestplate',
                              'lapis_leggings', 'lapis_boots'}:
                lapis_exp_bonus += 0.5

        exp_mult *= lapis_exp_bonus
        mining_exp_mult = 1
        compact_chance = 0
        if getattr(tool, 'modifier') == 'refined':
            tool_rarity = tool.rarity[0]
            tool_rarity_index = 'cureldsv'.index(tool_rarity)
            mining_exp_mult += 0.01 * tool_rarity_index
            compact_chance += 0.0001
        use_compact = enchants.get('compact', 0) != 0
        if use_compact:
            mining_exp_mult += 0.1 * enchants['compact']
            compact_chance += (0.001, 0.002, 0.002, 0.003, 0.003,
                               0.004, 0.004, 0.004, 0.005, 0.006)[enchants['compact'] - 1]

        drop_item = resource.drop
        enchanted_item = 'enchanted_' + resource.drop.rstrip('_block')
        default_amount = resource.amount

        last_cp = Decimal()
        cp_step = Decimal('0.1')
        for i in range(1, iteration + 1):
            sleep(time_cost)
            mining_fortune = self.get_stat('mining_fortune', tool_index)
            if is_gemstone:
                mining_fortune += tool.get_stat('gemstone_mining_fortune', self)
            fortune_mult = 1 + mining_fortune / 100

            if random_amount(compact_chance) == 1:
                self.recieve_item({'name': enchanted_item, 'count': 1})
                self.collect(enchanted_item, 1)
                aqua(f'{BOLD}COMPACT! {CLN}You found a {GREEN}{format_name(enchanted_item)}')
            else:
                count_pool = random_amount(default_amount, mult=fortune_mult)
                self.recieve_item({'name': drop_item, 'count': count_pool})
                self.collect(drop_item, count_pool)

            if use_compact:
                self.inventory[tool_index].compact_count += 1
                compact_count = self.inventory[tool_index].compact_count
                compact_level = {100: 2, 500: 3, 1500: 4, 5000: 5,
                                 15000: 6, 50000: 7, 150000: 8, 500000: 9, 1000000: 10}.get(compact_count, 0)
                if compact_level != 0:
                    self.inventory[tool_index].enchantments['compact'] = compact_level
                    mining_exp_mult = 1
                    compact_chance = 0
                    if getattr(tool, 'modifier') == 'refined':
                        tool_rarity = tool.rarity[0]
                        tool_rarity_index = 'cureldsv'.index(tool_rarity)
                        mining_exp_mult += 0.01 * tool_rarity_index
                        compact_chance += 0.0001
                    if use_compact:
                        mining_exp_mult += 0.1 * enchants['compact']
                        compact_chance += (0.001, 0.002, 0.002, 0.003, 0.003,
                                           0.004, 0.004, 0.004, 0.005, 0.006)[enchants['compact'] - 1]
                    blue(f'Compact {format_roman(compact_level - 1)} {YELLOW}on your {tool.display()}'
                         f' {YELLOW}was upgraded to {BLUE}Compact {format_roman(compact_level)}{YELLOW}!')

            if count_ore:
                if 'ores_mined' not in self.stats:
                    self.stats['ores_mined'] = 0
                self.stats['ores_mined'] += 1
                ores_mined = self.stats['ores_mined']
                rock_pet_rarity = {2500: 'common', 7500: 'uncommon', 20000: 'rare',
                                   100000: 'epic', 250000: 'legendary'}.get(ores_mined, '')
                if rock_pet_rarity:
                    pet_item = get_item('rock_pet', rarity=rock_pet_rarity)
                    green(f'You reached a new Ore Mined Milestone of {BLUE}{ores_mined} {GREEN}ores!')
                    green(f'A wild {pet_item.display()} {GREEN}has decided to befriend you!')
                    self.recieve_item(pet_item.to_obj())

            self.add_exp(random_amount(resource.exp, mult=exp_mult))
            self.add_skill_exp('mining', random_amount(resource.mining_exp, mult=mining_exp_mult), display=True)

            if resource.name == 'end_stone' and random_bool(0.1):
                self.slay(get_mob('endermite', level=37))

            if 'diamond' in resource.name:
                if random_bool(0.01 * (1 + magic_find / 100)):
                    loot = get_item('rare_diamond')
                    self.recieve_item(loot.to_obj())

                    rarity_color = RARITY_COLORS['rare']
                    white(f'{rarity_color}RARE DROP! '
                          f'{WHITE}({loot.display()}{WHITE}) {magic_find_str}')
            elif 'emerald' in resource.name:
                if random_bool((0.000_000_125) * (1 + magic_find / 100)):
                    rarity = 'rngesus'
                    item = get_item('emerald_dye')
                    white(f'{RARITY_COLORS[rarity]}{format_rarity(rarity)} DROP! '
                            f'{WHITE}({item.display()}{WHITE}) {magic_find_str}')
                    self.recieve_item(item.to_obj())

            mithril_powder = random_amount(resource.mithril_powder)
            if mithril_powder != 0:
                self.mithril_powder += mithril_powder
                dark_green(f'+ {format_number(mithril_powder)} Mithril Powder')

            if i >= (last_cp + cp_step) * iteration:
                while i >= (last_cp + cp_step) * iteration:
                    last_cp += cp_step
                perc = floor((i / iteration) * 100)
                gray(f'{i} / {iteration} ({perc}%) done')

            if 'mithril' in resource.name and randint(1, 50) == 1:
                white('Titanium has spawned nearby!')
                self.gather('titanium', tool_index)

    else:
        red('Unknown resource type.')


@checkpoint
def slay(self, mob: Mob, weapon_index: int | None, iteration: int = 1,
         /) -> bool:
    name = mob.name
    mob_name = format_name(name)

    weapon = (Empty() if weapon_index is None
              else self.inventory[weapon_index])

    if isinstance(weapon, (Bow, Sword, FishingRod, Pickaxe, Drill)):
        weapon_name = weapon.name
    else:
        weapon = Empty()
        weapon_name = ''

    active_pet = self.get_active_pet()
    has_active_pet = isinstance(active_pet, Pet)
    if has_active_pet:
        pet_mult = calc_pet_level(active_pet.rarity, active_pet.exp) / 100
    else:
        pet_mult = 0

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
    bestiary_stat += 2 * max(min(bestiary_level - 5, 5), 0) + 3 * max(bestiary_level - 10, 0)

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
    magic_find = self.get_stat('magic_find', weapon_index)
    magic_find += bestiary_stat
    magic_find_str = f'{AQUA}(+{format_number(magic_find)}% Magic Find!)'
    ferocity = self.get_stat('ferocity', weapon_index)

    thorns = 0

    last_stand = 0
    no_pain_no_gain = []

    weapon_abilities = getattr(weapon, 'abilities', {})
    weapon_enchants = getattr(weapon, 'enchantments', {})

    use_mithrils_protection = False
    activate_mithrils_protection = False

    use_kill_count = False
    if weapon_name == 'raider_axe':
        use_kill_count = True

    damage_bonus_mult = 1
    damage_recieved_mult = 1

    if weapon_name == 'axe_of_the_shredded' and name in ZOMBIES:
        damage_bonus_mult *= 3.5
        damage_recieved_mult *= 0.75
    elif weapon_name == 'reaper_falchion' and name in ZOMBIES:
        damage_bonus_mult *= 3
        damage_recieved_mult *= 0.8
    elif weapon_name == 'revenant_falchion' and name in ZOMBIES:
        damage_bonus_mult *= 2.5
    elif weapon_name == 'undead_sword' and name in UNDEADS:
        damage_bonus_mult *= 2

    elif weapon_name == 'scorpion_foil' and name in SPIDERS:
        damage_bonus_mult *= 2.5
    elif weapon_name == 'spider_sword' and name in SPIDERS:
        damage_bonus_mult *= 2

    elif weapon_name == 'pooch_sword' and name in WOLVES:
        damage_recieved_mult *= 0.8
        strength += 150
    elif weapon_name == 'shaman_sword' and name in WOLVES:
        damage_recieved_mult *= 0.8

    elif weapon_name == 'atomsplit_katana' and name in ENDERMEN:
        damage_bonus_mult *= 5.5
        damage_recieved_mult *= 0.88
    elif weapon_name == 'vorpal_katana' and name in ENDERMEN:
        damage_bonus_mult *= 4.5
        damage_recieved_mult *= 0.91
    elif weapon_name == 'voidedge_katana' and name in ENDERMEN:
        damage_bonus_mult *= 3.5
        damage_recieved_mult *= 0.94
    elif weapon_name == 'voidwalker_katana' and name in ENDERMEN:
        damage_bonus_mult *= 2.5
        damage_recieved_mult *= 0.97

    elif weapon_name == 'end_sword' and name in END_MOBS:
        damage_bonus_mult *= 2

    elif weapon_name == 'deathripper_dagger':
        if name in BLAZES:
            damage_bonus_mult *= 2.5
        elif name in SKELETONS:
            damage_bonus_mult *= 1.5
    elif weapon_name == 'pyrochaos_dagger':
        if name in BLAZES:
            damage_bonus_mult *= 2
        elif name in PIGMEN:
            damage_bonus_mult *= 1.5
    elif weapon_name == 'mawdredge_dagger':
        if name in BLAZES:
            damage_bonus_mult *= 2.5
        elif name in SKELETONS:
            damage_bonus_mult *= 1.5
    elif weapon_name == 'kindlebane_dagger':
        if name in BLAZES:
            damage_bonus_mult *= 1.5
        elif name in PIGMEN:
            damage_bonus_mult *= 1.2
    elif weapon_name == 'twilight_dagger':
        if name in BLAZES:
            damage_bonus_mult *= 1.5
        elif name in SKELETONS:
            damage_bonus_mult *= 1.2
    elif weapon_name == 'firedust_dagger':
        if name in BLAZES:
            damage_bonus_mult *= 1.2
        elif name in PIGMEN:
            damage_bonus_mult *= 1.1

    is_bow = isinstance(weapon, Bow)
    ues_arrows = is_bow

    damage_bonus_mult *= 1 + 0.04 * weapon_enchants.get('duplex', 0)
    duplex_fire_mult = 1 + 0.1 * weapon_enchants.get('duplex', 0)

    use_brute_force = 'brute_force' in getattr(self.armor[0], 'abilities', [])

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

        if 'mithrils_protection' in piece.abilities:
            use_mithrils_protection = True
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

        if is_bow:
            if piece.name == 'sniper_helmet':
                damage_bonus_mult *= 1.1
            elif piece.name in {
                'skeleton_grunt_helmet', 'skeleton_grunt_chestplate',
                'skeleton_grunt_leggings', 'skeleton_grunt_boots',
                'skeleton_soldier_helmet', 'skeleton_soldier_chestplate',
                'skeleton_soldier_leggings', 'skeleton_soldier_boots',
                'skeleton_master_helmet', 'skeleton_master_chestplate',
                'skeleton_master_leggings', 'skeleton_master_boots',
            }:
                damage_bonus_mult *= 1.05
            if piece.name == 'skeleton_master_chestplate':
                ues_arrows = False

    if is_bow and set_bonus in {'skeleton_soldier', 'skeleton_master'}:
        damage_bonus_mult *= 1.25

    three_set_bonus = True
    for piece in self.armor:
        if not isinstance(piece, Armor):
            three_set_bonus = False
            break

        if 'mithrils_protection' in piece.abilities:
            use_mithrils_protection = True
        for current_ability in piece.abilities:
            if current_ability in THREE_PIECE_BONUSES:
                break
        else:
            continue
        if three_set_bonus is True:
            three_set_bonus = current_ability
        elif three_set_bonus is not False:
            if current_ability != three_set_bonus:
                three_set_bonus = False

    if three_set_bonus == 'reaper_trolling_the_reaper':
        if name in ZOMBIES:
            defense += 100
            damage_bonus_mult *= 2
        else:
            damage_bonus_mult *= 0.01
    elif three_set_bonus == 'revenant_trolling_the_reaper':
        if name in ZOMBIES:
            defense += 100
    elif three_set_bonus == 'absolute_unit':
        if name in WOLVES:
            damage_recieved_mult *= 0.8

    enchants = 0
    enchants += {1: 0.05, 2: 0.1, 3: 0.15, 4: 0.2, 5: 0.3,
                 6: 0.45, 7: 0.65}.get(weapon_enchants.get('sharpness', 0), 0)
    enchants += {1: 0.08, 2: 0.16, 3: 0.24, 4: 0.32, 5: 0.4,
                 6: 0.5, 7: 0.65}.get(weapon_enchants.get('power', 0), 0)
    if name in UNDEADS:
        enchants += {1: 0.1, 2: 0.2, 3: 0.3, 4: 0.4, 5: 0.6,
                     6: 0.8, 7: 1}.get(weapon_enchants.get('smite', 0), 0)
    if name in SPIDERS:
        enchants += {1: 0.1, 2: 0.2, 3: 0.3, 4: 0.4, 5: 0.6,
                     6: 0.8, 7: 1}.get(weapon_enchants.get('bane_of_arthropods', 0), 0)
    if name in END_MOBS:
        enchants += {1: 0.15, 2: 0.3, 3: 0.45, 4: 0.6, 5: 0.8,
                     6: 1, 7: 1.3}.get(weapon_enchants.get('ender_slayer', 0), 0)
    if name in DRAGONS:
        enchants += 0.08 * weapon_enchants.get('dragon_hunter', 0)
    if name in BLAZES:
        enchants += 0.03 * weapon_enchants.get('smoldering', 0)
    if name in CUBISM_EFT:
        enchants += {1: 0.1, 2: 0.2, 3: 0.3, 4: 0.4, 5: 0.6,
                     6: 0.8}.get(weapon_enchants.get('cubism', 0), 0)
    if name in IMPALING_EFT:
        enchants += 0.125 * weapon_enchants.get('impaling', 0)
    enchants += 0.05 * weapon_enchants.get('spiked_hook', 0)

    healing_mult = 1
    healing_boost = False

    for piece in self.armor:
        if not isinstance(piece, Armor):
            continue

        if 'healing_boost' in piece.abilities:
            healing_boost = True
        piece_enchants = getattr(piece, 'enchantments', {})
        healing_mult += 0.02 + piece_enchants.get('rejuvenate', 0)
        thorns += 3 * piece_enchants.get('thorns', 0)
        last_stand += 5 * piece_enchants.get('last_stand', 0)
        no_pain_no_gain.append(25 * piece_enchants.get('no_pain_no_gain', 0))

        if piece.modifier == 'molten' and name in NETHER_MOBS:
            damage_recieved_mult *= 0.98

    if self.has_item({'name': 'healing_ring'}):
        healing_mult += 0.1
    elif self.has_item({'name': 'healing_talisman'}):
        healing_mult += 0.05
    if self.has_item({'name': 'survivor_cube'}):
        healing_mult += 0.05
    if healing_boost:
        healing_mult *= 2

    if set_bonus == 'deflect':
        thorns += 33

    armor_bonuses = 0
    if set_bonus == 'pumpkin_buff':
        armor_bonuses *= 1.1

    enchanting_level = self.get_skill_level('enchanting')

    execute = {1: 0.2, 2: 0.4, 3: 0.6, 4: 0.8, 5: 1,
               6: 1.25}.get(weapon_enchants.get('execute', 0), 0)
    fire_aspect_level = weapon_enchants.get('fire_aspect_level', 0)
    first_strike = 0.25 * weapon_enchants.get('first_strike', 0)
    flame = weapon_enchants.get('flame', 0)
    giant_killer_perc = {1: 0.001, 2: 0.002, 3: 0.003, 4: 0.004, 5: 0.006,
                         6: 0.009, 7: 0.012}.get(weapon_enchants.get('giant_killer', 0), 0)
    giant_killer_dmg = {1: 0.05, 2: 0.1, 3: 0.15, 4: 0.2, 5: 0.3,
                        6: 0.45, 7: 0.65}.get(weapon_enchants.get('giant_killer', 0), 0)
    infinite_quiver_chnc = 0.03 * weapon_enchants.get('infinite_quiver', 0)
    knockback = 1 + 0.1 * weapon_enchants.get('knockback', 0)
    life_steal = 0.005 * weapon_enchants.get('life_steal', 0)
    if is_bow:
        looting = 1 + 0.15 * weapon_enchants.get('chance', 0)
    elif isinstance(weapon, Sword):
        looting = 1 + 0.15 * weapon_enchants.get('looting', 0)
    else:
        looting = 1
    luck = 1 + 0.05 * weapon_enchants.get('luck', 0)
    overload_chnc = 0.1 * weapon_enchants.get('overload', 0)
    prosecute = {1: 0.1, 2: 0.2, 3: 0.3, 4: 0.4, 5: 0.7,
                 6: 1}.get(weapon_enchants.get('prosecute', 0), 0)
    punch = 1 + 0.08 * weapon_enchants.get('punch', 0)
    scavenger = 0.3 * weapon_enchants.get('scavenger', 0)
    if set_bonus == 'death_tax' and mob.level >= 10:
        scavenger += 5
    if 'raider_axe' in weapon_abilities and mob.level >= 10:
        scavenger += 20
    syphon = {1: 0.2, 2: 0.3, 3: 0.4, 4: 0.5, 5: 0.6}.get(weapon_enchants.get('syphon', 0), 0)
    titan_killer_perc = {1: 0.02, 2: 0.04, 3: 0.06, 4: 0.08, 5: 0.12,
                         6: 0.16, 6: 0.2}.get(weapon_enchants.get('titan_killer', 0), 0)
    titan_killer_dmg = {1: 0.06, 2: 0.12, 3: 0.18, 4: 0.24, 5: 0.4,
                        6: 0.6, 6: 0.8}.get(weapon_enchants.get('titan_killer', 0), 0)
    triple_strike = 0.1 * weapon_enchants.get('triple_strike', 0)
    thunderbolt = {1: 0.04, 2: 0.08, 3: 0.12, 4: 0.16, 5: 0.2,
                   6: 0.25}.get(weapon_enchants.get('thunderbolt', 0), 0)
    thunderlord = {1: 0.08, 2: 0.16, 3: 0.24, 4: 0.32, 5: 0.4,
                   6: 0.5, 7: 0.6}.get(weapon_enchants.get('thunderbolt', 0), 0)
    vampirism = weapon_enchants.get('vampirism', 0)

    coins_mult = 1 + 0.01 * bestiary_level
    added_exp = 0.2 * bestiary_level

    exp_mult = 1 + 0.125 * weapon_enchants.get('experience', 0)
    fishing_exp_mult = 1 + 0.02 * weapon_enchants.get('expertise', 0)

    combat_exp_mult = 1
    if self.has_item({'name': 'hunter_ring'}):
        combat_exp_mult *= 1.05
    elif self.has_item({'name': 'hunter_talisman'}):
        combat_exp_mult *= 1.02

    if name in SEA_CREATURES:
        if self.has_item({'name': 'sea_creature_artifact'}):
            damage_recieved_mult *= 0.85
        elif self.has_item({'name': 'sea_creature_ring'}):
            damage_recieved_mult *= 0.9
        elif self.has_item({'name': 'sea_creature_talisman'}):
            damage_recieved_mult *= 0.95
    if name in ZOMBIES:
        if self.has_item({'name': 'zombie_artifact'}):
            damage_recieved_mult *= 0.85
        elif self.has_item({'name': 'zombie_ring'}):
            damage_recieved_mult *= 0.9
        elif self.has_item({'name': 'zombie_talisman'}):
            damage_recieved_mult *= 0.95
    if name in SPIDERS:
        if self.has_item({'name': 'spider_artifact'}):
            damage_recieved_mult *= 0.85
    elif name in SPIDERS:
        if self.has_item({'name': 'spider_ring'}):
            damage_recieved_mult *= 0.9
    elif name in SPIDERS:
        if self.has_item({'name': 'spider_talisman'}):
            damage_recieved_mult *= 0.95
    if name in SKELETONS:
        if self.has_item({'name': 'skeleton_talisman'}):
            damage_recieved_mult *= 0.95
    if name in END_MOBS:
        if self.has_item({'name': 'ender_relic'}):
            damage_recieved_mult *= 0.75
        elif self.has_item({'name': 'ender_artifact'}):
            damage_recieved_mult *= 0.8
    if name in WITHERS:
        if self.has_item({'name': 'wither_relic'}):
            damage_recieved_mult *= 0.75
        elif self.has_item({'name': 'wither_artifact'}):
            damage_recieved_mult *= 0.8
    if name in NETHER_MOBS:
        if self.has_item({'name': 'nether_artifact'}):
            damage_recieved_mult *= 0.95

    intimidation_level = 0
    if self.has_item({'name': 'intimidation_artifact'}):
        intimidation_level = 25
    elif self.has_item({'name': 'intimidation_ring'}):
        intimidation_level = 5
    elif self.has_item({'name': 'intimidation_talisman'}):
        intimidation_level = 1
    if has_active_pet:
        if 'legendary_flamvoyant' in active_pet.abilities:
            intimidation_level += floor(20 * pet_mult)
        elif 'epic_flamvoyant' in active_pet.abilities:
            intimidation_level += floor(15 * pet_mult)
    if mob.level <= intimidation_level:
        damage_recieved_mult = 0

    burststopper_perc = 1
    if self.has_item({'name': 'burststopper_artifact'}):
        burststopper_perc = 0.9
    elif self.has_item({'name': 'burststopper_talisman'}):
        burststopper_perc = 0.95

    if set_bonus == 'pumpkin_buff':
        damage_recieved_mult *= 0.9

    soul_eater = weapon_enchants.get('soul_eater', 0) * 2
    soul_eater_strength = 0

    hp = health

    last_cp = Decimal()
    cp_step = Decimal('0.1')

    for count in range(1, iteration + 1):
        actual_speed = speed
        if set_bonus == 'young_blood' and hp >= health / 2:
            actual_speed += 70
        time_cost = 3 / actual_speed
        sleep(time_cost)

        width, _ = get_terminal_size()
        width = ceil(width * 0.85)
        aqua(f"{BOLD}{'':-^{width}}")

        healed = round((time_cost // 2) * (1.5 + health / 100), 1)
        if set_bonus == 'holy_blood':
            healed *= 3
        if activate_mithrils_protection:
            healed *= 3
            activate_mithrils_protection = False
        healed *= healing_mult
        hp = min(hp + healed, health)

        attack_time_cost = 0.4 / (1 + attack_speed / 100)
        sleep(1 / actual_speed)

        mob_hp = mob.health

        player_color = GREEN if hp >= health * 0.5 else YELLOW
        mob_color = GREEN if mob_hp >= mob.health * 0.5 else YELLOW
        gray(f'Your HP: {player_color}{format_number(hp)}{GRAY}/'
             f'{GREEN}{format_number(health)}{RED}❤\n'
             f"{mob_name}'s HP: "
             f'{mob_color}{format_number(mob_hp)}{GRAY}'
             f'/{GREEN}{format_number(mob.health)}{RED}❤\n')

        striked = False
        strike_count = 0

        while True:
            weapon_dmg = 0 if isinstance(weapon, Empty) else weapon.get_stat('damage', self)

            if ues_arrows:
                if not self.has_item({'name': 'arrow', 'count': 1}):
                    red("You don't have any arrows in your inventory!")
                    return
                if random_bool(infinite_quiver_chnc):
                    self.remove_item({'name': 'arrow', 'count': 1})

            killed = False

            round_count = 1 + ferocity / 100
            round_count *= 1 + attack_speed / 100
            round_count *= knockback * punch

            if striked:
                sleep(attack_time_cost)
            else:
                striked = True
                if not random_bool((45.75 + 0.625 * (speed / 100)) / 100):
                    round_count = 0

            for _ in range(random_int(round_count)):
                damage_dealt = 5 + weapon_dmg

                if strike_count % 3 == 2:
                    damage_dealt += thunderbolt
                    damage_dealt += thunderlord

                is_crit = False
                if random_bool(crit_chance / 100):
                    damage_dealt *= 1 + crit_damage / 100
                    if crit_chance >= 100 and random_bool(overload_chnc):
                        damage_dealt *= 1.1
                    is_crit = True

                damage_dealt *= 1 + (strength + soul_eater_strength) / 100
                soul_eater_strength = 0

                combat_level = self.get_skill_level('combat')

                effective_enchants = enchants

                if strike_count == 0:
                    effective_enchants += first_strike
                if strike_count < 3:
                    effective_enchants += triple_strike
                effective_enchants += (
                    min(giant_killer_perc * ((mob_hp - hp) / hp / 100), giant_killer_dmg)
                )
                effective_enchants += (
                    min(titan_killer_perc * mob.defense / 100, titan_killer_dmg)
                )
                effective_enchants += (
                    (execute / 100) * (1 - mob_hp / mob.health)
                )
                effective_enchants += prosecute * (mob_hp / mob.health)
                if use_brute_force:
                    effective_enchants += actual_speed / 125
                damage_mult = 1 + effective_enchants
                damage_mult += (
                    0.04 * min(combat_level, 50)
                    + 0.01 * max(min(combat_level - 50, 10), 0)
                )
                damage_dealt *= damage_mult * damage_bonus_mult
                if self.has_item({'name': 'tarantula_talisman'}):
                    if strike_count % 10 == 9:
                        damage_dealt *= 1.1

                damage_dealt *= 1 + fire_aspect_level * 0.03 * duplex_fire_mult
                damage_dealt += flame * 15 * duplex_fire_mult

                if mob.name == 'ice_walker' and isinstance(weapon, Pickaxe):
                    pass
                else:
                    damage_dealt /= 1 + mob.defense / 100

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
                if self.has_item({'name': 'devour_ring'}):
                    healed += 5
                if 'axe_of_the_shredded' in weapon_abilities:
                    healed += 50
                elif 'reaper_falchion' in weapon_abilities:
                    healed += 10
                elif 'love_tap' in weapon_abilities:
                    healed += 10

                hp = min(hp + healed * healing_mult, health)

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
            if use_mithrils_protection:
                damage_recieved = min(damage_recieved, health * 0.4)
            if damage_recieved > 0.5 * hp:
                damage_recieved *= burststopper_perc
            if damage_recieved != 0:
                hp = max(hp - damage_recieved, 0)
                gray(f"You've recieved {YELLOW}"
                     f"{format_number(damage_recieved)}{GRAY} damage.")

            true_damage_recieved = mob.true_damage / (1 + true_defense / 100)
            true_damage_recieved *= damage_recieved_mult
            if use_mithrils_protection:
                true_damage_recieved = min(true_damage_recieved, health * 0.4)
            if true_damage_recieved > 0.5 * hp:
                true_damage_recieved *= burststopper_perc
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
                self.die(mob.name)
                return False

            if random_bool(0.5) and thorns != 0:
                thorns_damage = (thorns / 100) * damage_recieved
                mob_hp -= thorns_damage

            mob_hp = max(mob_hp, 0)

            player_color = GREEN if hp >= health * 0.5 else YELLOW
            mob_color = GREEN if mob_hp >= mob.health * 0.5 else YELLOW
            if damage_recieved != 0 or true_damage_recieved != 0:
                gray(f"Your HP: {player_color}{format_number(hp)}{GRAY}/"
                     f"{GREEN}{format_number(health)}{RED}❤\n"
                     f"{mob_name}'s HP: "
                     f"{mob_color}{format_number(mob_hp)}{GRAY}"
                     f"/{GREEN}{format_number(mob.health)}{RED}❤\n")

            if mob_hp == 0:
                green(f"\nYou've killed a {mob_name}!")
                soul_eater_strength = mob.damage * soul_eater
                break

        if 'kills' not in self.stats:
            self.stats['kills'] = 0
        self.stats['kills'] += 1
        self.add_kill(mob.name)

        if use_kill_count:
            self.inventory[weapon_index].kill_count += 1

        if vampirism != 0 and hp != health:
            hp += (health - hp) * (vampirism / 100)
        if set_bonus == 'death_tax' and mob.level >= 10:
            hp = min(hp + 20, health)

        self.add_exp(random_amount(mob.exp + random_int(added_exp), mult=exp_mult))

        for pointer, loot_amount, rarity, drop_chance in mob.drops:
            loot_name = pointer['name']
            kwargs = {key: pointer[key] for key in pointer
                      if key not in {'name', 'count'}}
            item = get_item(loot_name, **kwargs)
            if isinstance(item, Pet):
                item.exp = 0
            amount_pool = random_amount(loot_amount)
            pointer = item.to_obj()
            pointer['count'] = amount_pool

            drop_chance *= looting
            drop_chance *= 1 + magic_find / 100
            if isinstance(item, Armor):
                drop_chance *= luck

            if not random_bool(drop_chance):
                continue

            self.recieve_item(pointer)
            self.collect(loot_name, amount_pool)

            if rarity not in {'common', 'uncommon'}:
                if getattr(item, 'count', 1) != 1:
                    item.count = 1
                white(f'{RARITY_COLORS[rarity]}{format_rarity(rarity)} DROP! '
                      f'{WHITE}({item.display()}{WHITE}) {magic_find_str}')

        if 'diamond' in mob.name:
            if random_bool(0.01 * (1 + magic_find / 100)):
                self.recieve_item({'name': 'rare_diamond'})

                loot = get_item('rare_diamond')
                if getattr(loot, 'count', 1) != 1:
                    loot.count = 1
                rarity_color = RARITY_COLORS['rare']
                white(f'{rarity_color}RARE DROP! '
                      f'{WHITE}({loot.display()}{WHITE}) {magic_find_str}')

        coins_recieved = (mob.coins + scavenger) * coins_mult
        if self.has_item({'name': 'scavenger_talisman'}):
            coins_recieved += 0.5 * mob.level
        coins_pool = random_int(coins_recieved)
        if coins_pool != 0:
            self.purse += coins_pool
            gray(f'+ {GOLD}{format_number(coins_pool)} Coins')

        if getattr(mob, 'farming_exp', 0) != 0:
            self.add_skill_exp('farming', mob.farming_exp, display=True)
        if getattr(mob, 'combat_exp', 0) != 0:
            self.add_skill_exp('combat', mob.combat_exp * combat_exp_mult, display=True)
        if getattr(mob, 'fishing_exp', 0) != 0:
            self.add_skill_exp('fishing', random_amount(mob.fishing_exp, mult=fishing_exp_mult), display=True)

        phoenix_pool = random()
        if phoenix_pool <= 0.0000008:
            self.recieve_item({'name': 'phoenix_pet', 'rarity': 'epic'})
            yellow(f'Wow! You found a {RED}Phoenix{YELLOW} pet!')
        elif phoenix_pool <= 0.000001:
            self.recieve_item({'name': 'phoenix_pet', 'rarity': 'legendary'})
            yellow(f'Wow! You found a {RED}Phoenix{YELLOW} pet!')

        if count >= (last_cp + cp_step) * iteration:
            while count >= (last_cp + cp_step) * iteration:
                last_cp += cp_step
            perc = floor((count / iteration) * 100)
            gray(f'{count} / {iteration} ({perc}%) killed')

    width, _ = get_terminal_size()
    width = ceil(width * 0.85)
    aqua(f"{BOLD}{'':-^{width}}")

    return True


grind_functions = {
    name: globals()[name] for name in __all__
}
