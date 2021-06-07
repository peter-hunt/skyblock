from itertools import count
from random import randint, random
from typing import Optional, Tuple

from ..constant.color import GOLD, GRAY, BLUE, WHITE, GREEN, RED, AQUA
from ..constant.main import DUNGEON_EXP, SKILL_EXP, SKILL_LIMITS
from ..constant.util import Amount, Number

from .io import gray, yellow, white
from .util import display_int, roman

__all__ = [
    'calc_exp', 'calc_skill_exp', 'calc_skill_exp_info', 'display_skill_reward',
    'dung_stat', 'random_amount', 'random_bool', 'random_int',
]


def calc_exp(amount: Number, /) -> int:
    if amount <= 352:
        for lvl in range(17):
            if (lvl + 1) ** 2 + 6 * (lvl + 1) > amount:
                return lvl

    elif amount <= 1507:
        for lvl in range(17, 32):
            if 2.5 ** (lvl + 1) ** 2 - 40.5 * (lvl + 1) + 360 > amount:
                return lvl

    else:
        for lvl in count(32):
            if 4.5 ** (lvl + 1) ** 2 - 162.5 * (lvl + 1) + 2220 > amount:
                return lvl


def calc_skill_exp(name: str, amount: Number, /) -> int:
    exp_table = DUNGEON_EXP if name == 'catacombs' else SKILL_EXP
    for line in exp_table:
        lvl, _, cumulative = line[:3]
        if amount < cumulative:
            return lvl - 1
    else:
        return SKILL_LIMITS[name]


def calc_skill_exp_info(
    name: str, amount: Number, /,
) -> Tuple[int, int, Optional[int]]:
    exp_table = DUNGEON_EXP if name == 'catacombs' else SKILL_EXP
    for line in exp_table:
        lvl, _, cumulative = line[:3]
        if amount < cumulative:
            # current, left, next_required, coins
            exp_left = amount - exp_table[lvl - 1][2]
            if name == 'catacombs':
                return lvl - 1, exp_left, line[1]
            else:
                return lvl - 1, exp_left, line[1]
    else:
        exp_left = amount - exp_table[-2][2]
        return SKILL_LIMITS[name], exp_left, line[1]


def display_skill_reward(name: str, original: Number, current: Number):
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
        yellow(f'  Farmhand {roman(current)}')
        white(f'   Grants {GREEN}+{GRAY}{fh_origin}->{GREEN}{fh_current}{GOLD}'
              f' ☘ Farming Fortune{WHITE},\n'
              f'   which increases your chance for multiple crops.')
        gray(f'  +{GREEN}{hp_delta} HP{RED} ♥ Health')

    elif name == 'mining':
        sk_origin = original * 4
        sk_current = current * 4

        def_delta = 0
        for lvl in range(original + 1, current + 1):
            def_delta += 1 if lvl <= 14 else 2

        yellow(f'  Spelunker {roman(current)}')
        white(f'   Grants {GREEN}+{GRAY}{sk_origin}->{GREEN}{sk_current}{GOLD}'
              f' ☘ Mining Fortune{WHITE},\n'
              f'   which increases your chance for multiple ore\n'
              f'   drops')
        gray(f'  +{GREEN}{def_delta} ☘ Defense')

    elif name == 'combat':
        lvl_delta = current - original

        war_origin = 0
        for lvl in range(original + 1):
            war_origin += 4 if lvl <= 50 else 1
        war_current = war_origin
        for lvl in range(original + 1, current + 1):
            war_current += 4 if lvl <= 50 else 1

        yellow(f'  Warrior {roman(current)}')
        white(f'   Deal {GRAY}{war_origin}->{GREEN}{war_current}%'
              f' {WHITE}more damage to mobs.')
        gray(f'  +{GREEN}{display_int(0.5 * lvl_delta)}%{BLUE} ☢ Crit Chance')

    elif name == 'foraging':
        lg_origin = original * 4
        lg_current = current * 4

        str_delta = 0
        for lvl in range(original + 1, current + 1):
            str_delta += 1 if lvl <= 14 else 2

        yellow(f'  Logger {roman(current)}')
        white(f'   Grants {GREEN}+{GRAY}{lg_origin}->{GREEN}{lg_current}{GOLD}'
              f' ☘ Foraging Fortune{WHITE},\n'
              f'   which increases your chance for multiple logs\n'
              f'   drops')
        gray(f'  +{GREEN}{str_delta}{RED} ❁ Strength')

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

        yellow(f'  Treasure Hunter {roman(current)}')
        white(f'   Increases the chance to find treasure when\n'
              f'   when fishing by {GREEN}+{GRAY}{display_int(th_origin)}->'
              f'{GREEN}{display_int(th_current)}%{WHITE}.')
        gray(f'  +{GREEN}{hp_delta}{RED} ♥ Health')

    elif name == 'enchanting':
        int_delta = 0
        for lvl in range(original + 1, current + 1):
            int_delta += 1 if lvl <= 14 else 2

        yellow(f'  Conjurer {roman(current)}')
        white(f'   Gain {GRAY}{original * 4}->{GREEN}{current * 4}%'
              f' {WHITE}more experience orbs from\n'
              f'   any source.')
        gray(f'  +{GREEN}{display_int(int_delta)}{AQUA} ✎ Intelligence')

    elif name == 'alchemy':
        int_delta = 0
        for lvl in range(original + 1, current + 1):
            int_delta += 1 if lvl <= 14 else 2

        yellow(f'  Brewer {roman(current)}')
        white(f'   Potions that you brew have a {GRAY}{original}->'
              f'{GREEN}{current}%\n'
              f'   {WHITE}longer duration.')
        gray(f'  +{GREEN}{display_int(int_delta)}{AQUA} ✎ Intelligence')

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
        white(f'  Increases the base stats of your dungeon items\n'
              f'  from {GRAY}{dg_origin}%->{RED}{dg_current}%'
              f' {WHITE}while in {RED}The Catacombs{WHITE}.')

    if name != 'catacombs':
        gray(f'  +{GOLD}{display_int(coins_reward)}{GRAY} Coins')


# 5l*4% + 5l*5% + 5l*6% + 5l*7% + 5l*8% + 5l*9% +
# 5l*10% + 5l*12% + 5l*14% + 16% + 17% + 18% + 19% + 20%
def dung_stat(num: int, lvl: int, stars: int) -> Number:
    mult = 1 + 0.1 * stars
    for i in range(lvl):
        if i < 35:
            mult += 0.01 * (4 + (i // 5))
        elif i < 45:
            mult += 0.01 * (10 + 2 * ((i - 35) // 5))
        else:
            mult += 0.01 * ((i - 45) + 16)
    return num * mult


def random_amount(amount: Amount = 1, /) -> int:
    if isinstance(amount, int):
        return amount
    else:
        return randint(amount[0], amount[1])


def random_bool(chance: float = 0.5, /) -> bool:
    return random() < chance


def random_int(num: float, /) -> int:
    int_part, float_part = divmod(num, 1)
    return int(int_part + (float_part > random()))
