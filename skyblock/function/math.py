from itertools import count
from random import random
from typing import Optional, Tuple

from ..constant.main import DUNGEON_EXP, SKILL_EXP, SKILL_LIMITS
from ..constant.util import Number

__all__ = ['calc_exp', 'calc_skill_exp', 'calc_skill_exp_info',
           'dung_stat', 'random_int']


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
    name: str, amount: Number, /
) -> Tuple[int, int, Optional[int]]:
    exp_table = DUNGEON_EXP if name == 'catacombs' else SKILL_EXP
    for line in exp_table:
        lvl, _, cumulative = line[:3]
        if amount < cumulative:
            # current, left, next_required, coins
            exp_left = amount - exp_table[lvl - 1][2]
            if name == 'catacombs':
                return lvl - 1, exp_left, line[1], None
            else:
                return lvl - 1, exp_left, line[1], line[3]
    else:
        exp_left = amount - exp_table[-2][2]
        return SKILL_LIMITS[name], exp_left, line[1], None


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


def random_int(num: float, /) -> int:
    int_part, float_part = divmod(num, 1)
    return int(int_part + (float_part > random()))
