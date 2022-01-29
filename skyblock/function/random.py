from random import random

from ..constant.util import Amount, Number


__all__ = ['random_amount', 'random_bool', 'random_int']


def _randint(lower: Number, upper: Number, /) -> int:
    delta = upper - lower
    return random_int(lower + random() * delta)


def random_amount(amount: Amount = 1, /, *, mult: Number = 1) -> int:
    if isinstance(amount, (tuple, list)):
        return _randint(amount[0] * mult, amount[1] * mult)
    else:
        return random_int(amount * mult)


def random_bool(chance: float = 0.5, /) -> bool:
    return random() < chance


def random_int(num: Number, /) -> int:
    int_part, float_part = divmod(num, 1)
    return int(int_part + random_bool(float_part))
