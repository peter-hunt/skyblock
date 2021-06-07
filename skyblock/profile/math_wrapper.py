from math import ceil
from os import get_terminal_size

from ..constant.color import BOLD, DARK_AQUA, GRAY
from ..constant.main import SKILL_EXP
from ..constant.util import Number
from ..function.math import calc_exp, calc_skill_exp, display_skill_reward
from ..function.io import dark_aqua, red, green, aqua
from ..function.util import display_name, roman

__all__ = ['profile_math']


def profile_math(cls):
    def add_exp(self, amount: Number, /):
        enchanting_lvl = calc_skill_exp('enchanting', self.skill_xp_enchanting)
        original_lvl = calc_exp(self.experience)
        self.experience += amount * (1 + 0.04 * enchanting_lvl)
        current_lvl = calc_exp(self.experience)
        if current_lvl > original_lvl:
            green(f'Reached XP level {current_lvl}.')

    cls.add_exp = add_exp

    def add_skill_exp(self, name: str, amount: Number, /):
        if not hasattr(self, f'skill_xp_{name}'):
            red(f'Skill not found: {name}')
            return
        exp = getattr(self, f'skill_xp_{name}')
        original_lvl = calc_skill_exp(name, exp)
        exp += amount
        setattr(self, f'skill_xp_{name}', exp)
        current_lvl = calc_skill_exp(name, exp)
        if current_lvl > original_lvl:
            coins_reward = 0
            if name != 'catacombs':
                for lvl in range(original_lvl + 1, current_lvl + 1):
                    coins_reward += SKILL_EXP[lvl][3]

            self.purse += coins_reward

            width, _ = get_terminal_size()
            width = ceil(width * 0.85)

            dark_aqua(f"{BOLD}{'':-^{width}}")
            original = roman(original_lvl) if original_lvl != 0 else '0'
            aqua(f' {BOLD}SKILL LEVEL UP {DARK_AQUA}{display_name(name)} '
                 f'{GRAY}{original}->{DARK_AQUA}{roman(current_lvl)}\n')
            green(f' {BOLD}REWARDS')
            display_skill_reward(name, original_lvl, current_lvl)
            dark_aqua(f"{BOLD}{'':-^{width}}")

    cls.add_skill_exp = add_skill_exp

    return cls
