from math import ceil
from os import get_terminal_size
from typing import Optional

from ..constant.color import BOLD, DARK_AQUA, GRAY
from ..constant.main import SKILL_EXP
from ..constant.util import Number
from ..function.math import calc_exp, calc_skill_exp, display_skill_reward
from ..function.io import dark_aqua, red, green, aqua
from ..function.util import display_name, roman
from ..item.object import Empty, Bow, Sword, Axe, Hoe, Pickaxe, Armor

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
                 f'{GRAY}{original}➜{DARK_AQUA}{roman(current_lvl)}\n')
            green(f' {BOLD}REWARDS')
            display_skill_reward(name, original_lvl, current_lvl)
            dark_aqua(f"{BOLD}{'':-^{width}}")

    cls.add_skill_exp = add_skill_exp

    def get_stat(self, name: str, index: Optional[int] = None):
        value = 0

        if index is None:
            item = Empty()

        else:
            item = self.inventory[index]

            if not isinstance(item, (Bow, Sword, Axe, Hoe, Pickaxe)):
                item = Empty()

            item_ench = getattr(item, 'enchantments', {})

            if name == 'strength':
                value += getattr(item, 'hot_potato', 0)
            if name == 'crit_damage':
                value += item_ench.get('critical', 0) * 10
            elif name == 'mining_speed':
                if item_ench.get('efficiency', 0) != 0:
                    value += 10 + item_ench['efficiency'] * 20
            elif name == 'sea_creature_chance':
                value += item_ench.get('expertise', 0) * 0.6
            elif name == 'mining_fortune':
                value += item_ench.get('fortune', 0) * 10
            elif name == 'ferocity':
                value += item_ench.get('vicious', 0)
            elif name == 'farming_fortune':
                value += item_ench.get('cultivating', 0)
                value += item_ench.get('harvesting', 0) * 12.6

        value += getattr(item, name, 0)

        combat_lvl = calc_skill_exp('combat', self.skill_xp_combat)
        farming_lvl = calc_skill_exp('farming', self.skill_xp_farming)
        enchanting_lvl = calc_skill_exp('enchanting', self.skill_xp_enchanting)
        foraging_lvl = calc_skill_exp('foraging', self.skill_xp_foraging)
        mining_lvl = calc_skill_exp('mining', self.skill_xp_mining)

        if name == 'health':
            value += 100
        elif name == 'speed':
            value += 100
        elif name == 'crit_chance':
            value += 30
        elif name == 'crit_damage':
            value += 50
        elif name == 'intelligence':
            value += 100
        elif name == 'sea_creature_chance':
            value += 20

        for piece in self.armor:
            if not isinstance(piece, Armor):
                continue

            value += getattr(piece, name, 0)

            armor_ench = getattr(piece, 'enchantments', {})

            if name == 'health':
                value += piece.hot_potato
                value += armor_ench.get('growth', 0) * 15
            elif name == 'defense':
                value += piece.hot_potato
                value += armor_ench.get('protection', 0) * 3
            elif name == 'true_defense':
                value += armor_ench.get('true_protection', 0) * 3
            elif name == 'speed':
                value += armor_ench.get('sugar_rush', 0) * 2
            elif name == 'intelligence':
                value += armor_ench.get('big_brain', 0) * 5
                value += armor_ench.get('smarty_pants', 0) * 5

        if name == 'health':
            value += min(farming_lvl, 14) * 2
            value += max(min(farming_lvl - 14, 5), 0) * 3
            value += max(min(farming_lvl - 19, 6), 0) * 4
            value += max(min(farming_lvl - 25, 35), 0) * 5
        elif name == 'mining':
            value += min(mining_lvl, 14) * 1
            value += max(min(mining_lvl - 14, 46), 0) * 2
        elif name == 'strength':
            value += min(foraging_lvl, 14) * 1
            value += max(min(foraging_lvl - 14, 36), 0) * 2
        elif name == 'crit_chance':
            value += combat_lvl * 0.5
        elif name == 'intelligence':
            value += min(enchanting_lvl, 14) * 1
            value += max(min(enchanting_lvl - 14, 46), 0) * 2
        elif name == 'mining_fortune':
            value += mining_lvl * 4
        elif name == 'foraging_fortune':
            value += foraging_lvl * 4
        elif name == 'farming_fortune':
            value += farming_lvl * 4

        return value

    cls.get_stat = get_stat

    return cls
