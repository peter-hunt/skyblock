from typing import Tuple

from ..constant import MINION_CAP


__all__ = ['get_minion_cap', 'get_minion_cap_info']


def get_minion_cap(amount: int) -> int:
    for cap, total in MINION_CAP:
        if amount >= total:
            break
    return cap


def get_minion_cap_info(amount: int) -> Tuple[int, int]:
    for index, (cap, total) in enumerate(MINION_CAP):
        if amount >= total:
            break
    if index == len(MINION_CAP) - 1:
        return cap, 0
    else:
        return cap, MINION_CAP[index + 1][1] - amount
