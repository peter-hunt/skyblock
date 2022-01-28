from typing import Tuple

from ..constant.minions import MINION_CAP


__all__ = ['get_minion_cap', 'get_minion_cap_info']


def get_minion_cap(amount: int) -> int:
    last_cap = 5
    for cap, total in MINION_CAP:
        if amount < total:
            break
        last_cap = cap
    return last_cap


def get_minion_cap_info(amount: int) -> Tuple[int, int, bool]:
    last_cap = 5
    new_added = False
    for index, (cap, total) in enumerate(MINION_CAP):
        if amount <= total:
            if amount == total:
                new_added = True
                last_cap += 1
            break
        last_cap = cap
    if index == len(MINION_CAP) - 1:
        return last_cap, -1, False
    else:
        return last_cap, MINION_CAP[index + 1][1] - amount, new_added
