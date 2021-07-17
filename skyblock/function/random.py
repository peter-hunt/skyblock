from random import randint, random

from ..constant.util import Amount, Number


__all__ = ['random_amount', 'random_bool', 'random_int']


def random_amount(amount: Amount = 1, /) -> int:
    if isinstance(amount, tuple):
        return randint(amount[0], amount[1])
    else:
        return random_int(amount)


def random_bool(chance: float = 0.5, /) -> bool:
    return random() < chance


def random_int(num: Number, /) -> int:
    int_part, float_part = divmod(num, 1)
    return int(int_part + random_bool(float_part))
