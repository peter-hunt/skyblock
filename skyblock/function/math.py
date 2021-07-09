from itertools import count
from math import floor, isinf
from random import randint, random
from typing import Optional, Tuple

from ..constant.color import *
from ..constant.main import (
    DUNGEON_EXP, SKILL_EXP, SKILL_LIMITS, PET_EXP_DIFF, KILL_LEVELS,
)
from ..constant.util import Amount, Number

from .io import *
from .util import format_number, format_roman


__all__ = [
    'calc_bestiary_lvl', 'calc_bestiary_upgrade_amount', 'calc_exp_lvl',
    'calc_exp', 'calc_pet_exp', 'calc_pet_lvl', 'calc_pet_upgrade_exp',
    'calc_skill_lvl', 'calc_skill_lvl_info', 'display_skill_reward',
    'dung_stat', 'fround', 'random_amount', 'random_bool', 'random_int',
]


def calc_bestiary_lvl(amount: int, /) -> int:
    """
    Calculate bestiary level from kill amonut.

    Args:
        amount: Kills on the mob.

    Returns:
        An integer of bestiary level.
    """

    for level, i in enumerate(KILL_LEVELS):
        if i > amount:
            return level
        amount -= i
    return amount // 100000 + 11


def calc_bestiary_upgrade_amount(amount: int, /) -> Tuple[int, int]:
    """
    Calculate mob kills needed for an upgrade.

    Args:
        amount: Kills on the mob.

    Returns:
        An tuple of kills left and to the next level.
    """

    for i in KILL_LEVELS:
        if i > amount:
            return amount, i
        amount -= i
    return amount % 100000, 100000


def calc_exp_lvl(exp: Number, /) -> int:
    """
    Calculate vanilla xp level from xp.

    Args:
        exp: An integer or float of the vanilla xp.

    Returns:
        An integer of vanilla xp level.
    """

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
    """
    Calculate vanilla xp from xp level.

    Args:
        lvl: An integer of the vanilla xp level.

    Returns:
        An integer of vanilla xp.
    """

    if lvl <= 16:
        return lvl ** 2 + 6 * lvl

    elif lvl <= 31:
        return 2.5 * lvl ** 2 - 40.5 * lvl + 360

    else:
        return 4.5 * lvl ** 2 - 162.5 * lvl + 2220


def calc_pet_exp(rarity: str, level: Number, /) -> int:
    """
    Calculate pet xp from rarity and level.

    Args:
        rarity: A string of pet rarity.
        int: An integer or float of the pet level.

    Returns:
        An integer of pet xp.
    """

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


def calc_pet_lvl(rarity: str, exp: Number, /) -> int:
    """
    Calculate pet xp level.

    Args:
        rarity: A string of pet rarity.
        exp: An integer or float of the pet xp.

    Returns:
        An integer of pet xp level.
    """

    if rarity == 'mythic':
        rarity = 'l'
    diff_list = PET_EXP_DIFF['curel'.index(rarity[0])]
    for lvl, diff in enumerate(diff_list):
        if exp < diff:
            return lvl
        exp -= diff
    else:
        return 100


def calc_pet_upgrade_exp(rarity: str, exp: Number, /) -> Tuple[int, int]:
    """
    Calculate pet xp needed for an upgrade.

    Args:
        rarity: A string of pet rarity.
        exp: An integer or float of the pet xp.

    Returns:
        An tuple of pet xp left and to the next level.
    """

    if rarity == 'mythic':
        rarity = 'l'
    diff_list = PET_EXP_DIFF['curel'.index(rarity[0])]
    for diff in diff_list:
        if exp < diff:
            return exp, diff
        exp -= diff
    return exp + diff, diff


def calc_skill_lvl(name: str, exp: Number, /) -> int:
    """
    Calculate skill level from xp.

    Args:
        name: A string of the skill.
        exp: An integer or float of the skill xp.

    Returns:
        An integer of skill level.
    """

    exp_table = DUNGEON_EXP if name == 'catacombs' else SKILL_EXP
    for line in exp_table:
        lvl, _, cumulative = line[:3]
        if exp < cumulative:
            return lvl - 1
    else:
        return SKILL_LIMITS[name]


def calc_skill_lvl_info(name: str, exp: Number, /) -> \
        Tuple[int, int, Optional[int]]:
    """
    Calculate skill level from xp.

    Args:
        name: A string of the skill.
        exp: An integer or float of the skill xp.

    Returns:
        An tuple of current level, xp left to the next level,
        xp required to the next level, and coins reward of the next level.
    """

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
        return SKILL_LIMITS[name], exp_left, line[1]


def display_skill_reward(name: str, original: Number, current: Number):
    """
    Display skill upgrade reward.

    Args:
        name: A string of the skill.
        original: An integer or float of the skill level before the upgrade.
        current: An integer or float of the skill level after the upgrade.
    """

    coins_reward = 0
    if name != 'catacombs':
        for lvl in range(original + 1, current + 1):
            coins_reward += SKILL_EXP[lvl][3]

    if name == 'farming':
        fh_origin = original * 4
        fh_current = current * 4

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

        fh_current = fh_origin
        for lvl in range(original + 1, current + 1):
            fh_current += 4 if lvl <= 50 else 1
        yellow(f'  Farmhand {format_roman(current)}')
        farming_fortune = STAT_COLORS['farming_fortune']
        white(f'   Grants {GREEN}+{GRAY}{fh_origin}->{GREEN}{fh_current}'
              f' {farming_fortune} Farming Fortune{WHITE},'
              f' which increases your chance for multiple crops.')
        health = STAT_COLORS['health']
        gray(f'  +{GREEN}{hp_delta} HP {health} Health')

    elif name == 'mining':
        sk_origin = original * 4
        sk_current = current * 4

        def_delta = 0
        for lvl in range(original + 1, current + 1):
            def_delta += 1 if lvl <= 14 else 2

        yellow(f'  Spelunker {format_roman(current)}')
        mining_fortune = STAT_COLORS['mining_fortune']
        white(f'   Grants {GREEN}+{GRAY}{sk_origin}->{GREEN}{sk_current}'
              f' {mining_fortune} Mining Fortune{WHITE},'
              f' which increases your chance for multiple ore drops')
        defense = STAT_COLORS['defense']
        gray(f'  +{GREEN}{def_delta} {defense} Defense')

    elif name == 'combat':
        lvl_delta = current - original

        war_origin = 0
        for lvl in range(original + 1):
            war_origin += 4 if lvl <= 50 else 1
        war_current = war_origin
        for lvl in range(original + 1, current + 1):
            war_current += 4 if lvl <= 50 else 1

        yellow(f'  Warrior {format_roman(current)}')
        white(f'   Deal {GRAY}{war_origin}->{GREEN}{war_current}%'
              f' {WHITE}more damage to mobs.')
        crit_chance = STAT_COLORS['crit_chance']
        gray(f'  +{GREEN}{format_number(0.5 * lvl_delta)}%'
             f' {crit_chance} Crit Chance')

    elif name == 'foraging':
        lg_origin = original * 4
        lg_current = current * 4

        str_delta = 0
        for lvl in range(original + 1, current + 1):
            str_delta += 1 if lvl <= 14 else 2

        yellow(f'  Logger {format_roman(current)}')
        foraging_fortune = STAT_COLORS['foraging_fortune']
        white(f'   Grants {GREEN}+{GRAY}{lg_origin}->{GREEN}{lg_current}'
              f' {foraging_fortune} Foraging Fortune{WHITE},'
              f' which increases your chance for multiple logs drops')
        strength = STAT_COLORS['strength']
        gray(f'  +{GREEN}{str_delta} {strength} Strength')

    elif name == 'fishing':
        th_origin = original * 0.2
        th_current = current * 0.2

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
              f' by {GREEN}+{GRAY}{format_number(th_origin)}->'
              f'{GREEN}{format_number(th_current)}%{WHITE}.')
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
        pl_delta = current - original

        yellow(f'  Zoologist {format_roman(current)}')
        white(f'   Gain {GRAY}{original}->'
              f'{GREEN}{current}%{WHITE} extra pet exp.')
        pet_luck = STAT_COLORS['pet_luck']
        gray(f'  +{GREEN}{format_number(pl_delta)} {pet_luck} Pet Luck')

    elif name == 'catacombs':
        hp_delta = current - original

        dg_origin = 0
        for i in range(1, original + 1):
            if i < 35:
                dg_origin += 4 + (i // 5)
            elif i < 45:
                dg_origin += 10 + 2 * ((i - 35) // 5)
            else:
                dg_origin += (i - 45) + 16

        dg_current = dg_origin
        for i in range(original + 1, current + 1):
            if i < 35:
                dg_current += 4 + (i // 5)
            elif i < 45:
                dg_current += 10 + 2 * ((i - 35) // 5)
            else:
                dg_current += (i - 45) + 16

        gray(f'  +{GREEN}{hp_delta}{RED} ♥ Health')
        white(f'  Increases the base stats of your dungeon items'
              f' from {GRAY}{dg_origin}%->{RED}{dg_current}%'
              f' {WHITE}while in {RED}The Catacombs{WHITE}.')

    if name != 'catacombs':
        gray(f'  +{GOLD}{format_number(coins_reward)}{GRAY} Coins')


# 5l*4% + 5l*5% + 5l*6% + 5l*7% + 5l*8% + 5l*9% +
# 5l*10% + 5l*12% + 5l*14% + 16% + 17% + 18% + 19% + 20%
def dung_stat(value: Number, lvl: int, stars: int) -> float:
    """
    Calculate dungeon item stat bonus based on dungeon level.

    Args:
        value: An integer or float of the stat.
        lvl: An integer of dungeon level.
        stars: An integer of stars on the item.

    Returns:
        A float of stat bonus rate.
    """

    mult = 1 + 0.1 * stars

    for i in range(lvl):
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


def random_amount(amount: Amount = 1, /) -> int:
    """
    Generate random integer based on given range.

    Args:
        amount: An integer or a range of integer.

    Returns:
        A random integer between the range.
    """

    if isinstance(amount, tuple):
        return randint(amount[0], amount[1])
    else:
        return random_int(amount)


def random_bool(chance: float = 0.5, /) -> bool:
    """
    Generate random boolean based on given range.

    Args:
        chance: A float of chance of whether the result will be true.

    Returns:
        A random boolean based on the chance.
    """

    return random() < chance


def random_int(num: Number, /) -> int:
    """
    Generate random integer close to and average to given number.

    Args:
        num: An integer or float of the wanted average.

    Returns:
        A random integer averaging to the given number.
    """

    int_part, float_part = divmod(num, 1)
    return int(int_part + random_bool(float_part))
