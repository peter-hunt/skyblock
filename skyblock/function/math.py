from itertools import count
from math import floor, isinf

from ..constant.colors import *
from ..constant.main import (
    DUNGEON_EXP, SKILL_EXP, SKILL_LIMITS, PET_EXP_DIFF, KILL_LEVELS,
)
from ..constant.util import Number

from .io import *
from .util import format_number, format_roman


__all__ = [
    'calc_bestiary_level', 'calc_bestiary_upgrade_amount', 'calc_exp_level',
    'calc_exp', 'calc_pet_exp', 'calc_pet_level', 'calc_pet_upgrade_exp',
    'calc_skill_level', 'calc_skill_level_info', 'display_skill_reward',
    'dung_stat', 'fround',
]


def calc_bestiary_level(amount: int, /) -> int:
    for level, i in enumerate(KILL_LEVELS):
        if i > amount:
            return level
        amount -= i
    return amount // 100000 + 11


def calc_bestiary_upgrade_amount(amount: int, /) -> tuple[int, int]:
    for i in KILL_LEVELS:
        if i > amount:
            return amount, i
        amount -= i
    return amount % 100000, 100000


def calc_exp_level(exp: Number, /) -> int:
    for lvl in range(17):
        if (lvl + 1) ** 2 + 6 * (lvl + 1) > exp:
            return lvl
    for lvl in range(17, 32):
        if 2.5 * (lvl + 1) ** 2 - 40.5 * (lvl + 1) + 360 > exp:
            return lvl
    for lvl in count(32):
        if 4.5 * (lvl + 1) ** 2 - 162.5 * (lvl + 1) + 2220 > exp:
            return lvl


def calc_exp(lvl: int, /) -> int:
    if lvl <= 16:
        return lvl ** 2 + 6 * lvl
    elif lvl <= 31:
        return 2.5 * lvl ** 2 - 40.5 * lvl + 360
    else:
        return 4.5 * lvl ** 2 - 162.5 * lvl + 2220


def calc_pet_exp(rarity: str, level: Number, /) -> int:
    if rarity == 'mythic':
        rarity = 'l'

    diff_list = PET_EXP_DIFF['curel'.index(rarity[0])]
    exp = 0
    for lvl, diff in enumerate(diff_list):
        if lvl <= level:
            exp += diff
        else:
            break
    return exp


def calc_pet_level(rarity: str, exp: Number, /) -> int:
    if rarity == 'mythic':
        rarity = 'l'

    diff_list = PET_EXP_DIFF['curel'.index(rarity[0])]
    for lvl, diff in enumerate(diff_list):
        if exp < diff:
            return lvl
        exp -= diff
    else:
        return 100


def calc_pet_upgrade_exp(rarity: str, exp: Number, /) -> tuple[int, int]:
    if rarity == 'mythic':
        rarity = 'l'

    diff_list = PET_EXP_DIFF['curel'.index(rarity[0])]
    for diff in diff_list:
        if exp < diff:
            return exp, diff
        exp -= diff
    return exp + diff, diff


def calc_skill_level(name: str, exp: Number, /) -> int:
    exp_table = DUNGEON_EXP if name == 'catacombs' else SKILL_EXP
    for line in exp_table:
        lvl, _, cumulative = line[:3]
        if exp < cumulative:
            return lvl - 1
    else:
        return SKILL_LIMITS[name]


def calc_skill_level_info(name: str, exp: Number, /) -> \
        tuple[int, int, int | None]:
    exp_table = DUNGEON_EXP if name == 'catacombs' else SKILL_EXP
    for line in exp_table:
        lvl, _, cumulative = line[:3]
        if exp < cumulative:
            # current, left, next_required, coins
            exp_left = exp - exp_table[lvl - 1][2]
            if name == 'catacombs':
                return lvl - 1, exp_left, line[1]
            else:
                return lvl - 1, exp_left, line[1]
    else:
        exp_left = exp - exp_table[-2][2]
        return SKILL_LIMITS[name], exp_left, 0


def display_skill_reward(name: str, original: Number, current: Number):
    coins_reward = 0
    if name != 'catacombs':
        for lvl in range(original + 1, current + 1):
            coins_reward += SKILL_EXP[lvl][3]

    if name == 'farming':
        bonus_origin = original * 4
        bonus_current = current * 4
        hp_delta = 0
        for lvl in range(original + 1, current + 1):
            if lvl <= 14:
                hp_delta += 2
            elif lvl <= 19:
                hp_delta += 3
            elif lvl <= 25:
                hp_delta += 4
            else:
                hp_delta += 5
        bonus_current = bonus_origin
        for lvl in range(original + 1, current + 1):
            bonus_current += 4 if lvl <= 50 else 1
        yellow(f'  Farmhand {format_roman(current)}')
        farming_fortune = STAT_COLORS['farming_fortune']
        white(f'   Grants {GREEN}+{GRAY}{bonus_origin}->{GREEN}{bonus_current}'
              f' {farming_fortune} Farming Fortune{WHITE},'
              f' which increases your chance for multiple crops.')
        health = STAT_COLORS['health']
        gray(f'  +{GREEN}{hp_delta} HP {health} Health')

    elif name == 'mining':
        bonus_origin = original * 4
        bonus_current = current * 4
        def_delta = 0
        for lvl in range(original + 1, current + 1):
            def_delta += 1 if lvl <= 14 else 2
        yellow(f'  Spelunker {format_roman(current)}')
        mining_fortune = STAT_COLORS['mining_fortune']
        white(f'   Grants {GREEN}+{GRAY}{bonus_origin}->{GREEN}{bonus_current}'
              f' {mining_fortune} Mining Fortune{WHITE},'
              f' which increases your chance for multiple ore drops')
        defense = STAT_COLORS['defense']
        gray(f'  +{GREEN}{def_delta} {defense} Defense')

    elif name == 'combat':
        lvl_delta = current - original
        bonus_origin = 0
        for lvl in range(original + 1):
            bonus_origin += 4 if lvl <= 50 else 1
        bonus_current = bonus_origin
        for lvl in range(original + 1, current + 1):
            bonus_current += 4 if lvl <= 50 else 1
        yellow(f'  Warrior {format_roman(current)}')
        white(f'   Deal {GRAY}{bonus_origin}->{GREEN}{bonus_current}%'
              f' {WHITE}more damage to mobs.')
        crit_chance = STAT_COLORS['crit_chance']
        gray(f'  +{GREEN}{format_number(0.5 * lvl_delta)}%'
             f' {crit_chance} Crit Chance')

    elif name == 'foraging':
        bonus_origin = original * 4
        bonus_current = current * 4
        str_delta = 0
        for lvl in range(original + 1, current + 1):
            str_delta += 1 if lvl <= 14 else 2
        yellow(f'  Logger {format_roman(current)}')
        foraging_fortune = STAT_COLORS['foraging_fortune']
        white(f'   Grants {GREEN}+{GRAY}{bonus_origin}->{GREEN}{bonus_current}'
              f' {foraging_fortune} Foraging Fortune{WHITE},'
              f' which increases your chance for multiple logs drops')
        strength = STAT_COLORS['strength']
        gray(f'  +{GREEN}{str_delta} {strength} Strength')

    elif name == 'fishing':
        bonus_origin = original * 0.2
        bonus_current = current * 0.2
        hp_delta = 0
        for lvl in range(original + 1, current + 1):
            if lvl <= 14:
                hp_delta += 2
            elif lvl <= 19:
                hp_delta += 3
            elif lvl <= 25:
                hp_delta += 4
            else:
                hp_delta += 5
        yellow(f'  Treasure Hunter {format_roman(current)}')
        white(f'   Increases the chance to find treasure when fishing'
              f' by {GREEN}+{GRAY}{format_number(bonus_origin)}->'
              f'{GREEN}{format_number(bonus_current)}%{WHITE}.')
        health = STAT_COLORS['health']
        gray(f'  +{GREEN}{hp_delta} {health} Health')

    elif name == 'enchanting':
        int_delta = 0
        for lvl in range(original + 1, current + 1):
            int_delta += 1 if lvl <= 14 else 2
        yellow(f'  Conjurer {format_roman(current)}')
        white(f'   Gain {GRAY}{original * 4}->{GREEN}{current * 4}%'
              f' {WHITE}more experience orbs from any source.')
        intelligence = STAT_COLORS['intelligence']
        gray(f'  +{GREEN}{format_number(int_delta)}{AQUA}'
             f' {intelligence} Intelligence')

    elif name == 'alchemy':
        int_delta = 0
        for lvl in range(original + 1, current + 1):
            int_delta += 1 if lvl <= 14 else 2
        yellow(f'  Brewer {format_roman(current)}')
        white(f'   Potions that you brew have a {GRAY}{original}->'
              f'{GREEN}{current}% {WHITE}longer duration.')
        intelligence = STAT_COLORS['intelligence']
        gray(f'  +{GREEN}{format_number(int_delta)}{AQUA}'
             f' {intelligence} Intelligence')

    elif name == 'taming':
        bonus_delta = current - original
        yellow(f'  Zoologist {format_roman(current)}')
        white(f'   Gain {GRAY}{original}->'
              f'{GREEN}{current}%{WHITE} extra pet exp.')
        pet_luck = STAT_COLORS['pet_luck']
        gray(f'  +{GREEN}{format_number(bonus_delta)} {pet_luck} Pet Luck')

    elif name == 'catacombs':
        hp_delta = current - original
        gray(f'  +{GREEN}{hp_delta}{RED} ♥ Health')
        if original >= 50:
            return
        bonus_origin = 0
        for i in range(1, original + 1):
            if i < 35:
                bonus_origin += 4 + (i // 5)
            elif i < 45:
                bonus_origin += 10 + 2 * ((i - 35) // 5)
            else:
                bonus_origin += (i - 45) + 16
        bonus_current = bonus_origin
        for i in range(original + 1, current + 1):
            if i < 35:
                bonus_current += 4 + (i // 5)
            elif i < 45:
                bonus_current += 10 + 2 * ((i - 35) // 5)
            else:
                bonus_current += (i - 45) + 16
        white(f'  Increases the base stats of your dungeon items'
              f' from {GRAY}{bonus_origin}%->{RED}{bonus_current}%'
              f' {WHITE}while in {RED}The Catacombs{WHITE}.')

    if name != 'catacombs':
        gray(f'  +{GOLD}{format_number(coins_reward)}{GRAY} Coins')


def dung_stat(value: Number, lvl: int, stars: int, /) -> float:
    mult = 1 + 0.1 * stars

    for i in range(min(lvl, 50)):
        if i < 35:
            mult += 0.01 * (4 + (i // 5))
        elif i < 45:
            mult += 0.01 * (10 + 2 * ((i - 35) // 5))
        else:
            mult += 0.01 * ((i - 45) + 16)

    return value * mult


def fround(number: Number, digit=0, /) -> Number:
    if isinf(number):
        return number
    mult = 10 ** digit
    return floor(number * mult) / mult
