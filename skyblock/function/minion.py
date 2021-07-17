from typing import Tuple

from ..constant import MINION_CAP


__all__ = ['get_minion_cap', 'get_minion_cap_info']


def get_minion_cap(amount: int) -> int:
    last_cap = 5
    for cap, total in MINION_CAP:
        if amount < total:
            break
        last_cap = cap
    return last_cap


def get_minion_cap_info(amount: int) -> Tuple[int, int]:
    last_cap = 5
    for index, (cap, total) in enumerate(MINION_CAP):
        if amount < total:
            break
        last_cap = cap
    if index == len(MINION_CAP) - 1:
        return last_cap, 0
    else:
        return last_cap, MINION_CAP[index + 1][1] - amount
