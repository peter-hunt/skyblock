from math import floor, sqrt
from typing import Any, Dict

from ..constant.ability import SET_BONUSES
from ..constant.colors import *
from ..constant.enchanting import ENCH_LVLS, ULTIMATE_ENCHS
from ..constant.util import Number
from ..function.math import (
    calc_pet_level, calc_pet_upgrade_exp, dung_stat, fround,
)
from ..function.reforging import get_modifier
from ..function.util import (
    camel_to_under, format_name, format_number, format_roman, format_short,
    format_zone,
)
from ..format.function import format_temp
from ..format.template import get_template

from .abilities import get_ability


__all__ = ['item_type']


def item_type(cls: type, /) -> type:
    anno = getattr(cls, '__annotations__', {})
    default = {}
    for name in anno:
        if hasattr(cls, name):
            default[name] = getattr(cls, name)

    init_str = 'lambda self'
    for key in anno:
        if key in default:
            init_str += f', {key}={default[key]!r}'
        else:
            init_str += f', {key}'
    init_str += ': ('
    for key in anno:
        init_str += f'setattr(self, {key!r}, {key}), '
    init_str += 'None,)[-1]'

    cls.__init__ = eval(init_str)

    def to_obj(self, /) -> Dict[str, Any]:
        if cls.__name__ == 'Empty':
            return {}

        result = {}
        for key in anno:
            if key in default and default[key] == getattr(self, key, None):
                continue
            if key == 'enchantments':
                enchants = getattr(self, key)
                result[key] = {enchant_name: enchants[enchant_name]
                               for enchant_name in sorted(enchants)}
            else:
                result[key] = getattr(self, key)

        result['type'] = camel_to_under(cls.__name__)
        return result

    cls.to_obj = to_obj

    from_obj_str = 'lambda cls, obj: cls('
    from_obj_str += ', '.join(
        f'obj.get({key!r}, {default[key]!r})' if key in default
        else f'obj[{key!r}]' for key in anno
    )
    from_obj_str += ')'

    cls.from_obj = classmethod(eval(from_obj_str))

    copy_str = 'lambda self: self.__class__('
    copy_str += ', '.join(f'self.{key}' for key in anno)
    copy_str += ')'

    cls.copy = eval(copy_str)

    def __repr__(self):
        string = f'{self.__class__.__name__}('
        args = []
        kwargs = []

        for name in anno:
            if name in default:
                kwargs.append(f'{name}={getattr(self, name)!r}')
            else:
                args.append(f'{getattr(self, name)!r}')

        string += ', '.join(args + kwargs) + ')'
        return string

    cls.__repr__ = __repr__

    def display(self):
        if self.__class__.__name__ == 'Empty':
            return f'{BOLD}{WHITE}Empty{CLN}'

        if self.__class__.__name__ == 'Minion':
            rarity_color = RARITY_COLORS['rare']
        else:
            rarity_color = RARITY_COLORS[self.rarity]

        if self.__class__.__name__ == 'TravelScroll':
            name = f'Travel Scroll to {format_zone(self.island)}'
            if self.zone is not None:
                name += f' {format_zone(self.zone)}'
        elif self.__class__.__name__ == 'Pet':
            name = format_name('_'.join(self.name.split('_')[:-1]))
        elif self.__class__.__name__ == 'ReforgeStone':
            name = format_name(self.name)
        elif getattr(self, 'modifier', None) is not None:
            fullname = f'{self.modifier.capitalize()} {self.name}'
            name = format_name(fullname)
        else:
            name = format_name(self.name)

        count = (f' x {format_number(self.count)}'
                 if getattr(self, 'count', 1) != 1 else '')

        if getattr(self, 'stars', None) is None:
            stars = ''
        elif self.stars <= 5:
            stars = f' {GOLD}' + self.stars * '✪'
        else:
            stars = (f' {RED}' + (self.stars - 5) * '✪'
                     + GOLD + (10 - self.stars) * '✪')

        if self.__class__.__name__ == 'Pet':
            lvl = calc_pet_level(self.rarity, self.exp)
            return f'{GRAY}[Lvl {lvl}] {rarity_color}{name}'
        elif self.__class__.__name__ == 'Minion':
            tier_str = format_roman(self.tier)
            return f'{rarity_color}{name} {tier_str}'
        else:
            return f'{rarity_color}{name}{stars}{DARK_GRAY}{count}{CLN}'

    cls.display = display

    def info(self, profile, /):
        mining_level = profile.get_skill_level('mining')
        combat_level = profile.get_skill_level('combat')
        fishing_level = profile.get_skill_level('fishing')
        catacombs_level = profile.get_skill_level('catacombs')
        if self.__class__.__name__ == 'Minion':
            rarity_color = RARITY_COLORS['rare']
        else:
            rarity_color = RARITY_COLORS[self.rarity]

        modifier = ''
        if self.__class__.__name__ == 'ReforgeStone':
            pass
        elif getattr(self, 'modifier', None) is not None:
            modifier = f'{self.modifier.capitalize()} '

        if self.__class__.__name__ == 'TravelScroll':
            name = f'Travel Scroll to {format_name(self.island)}'
            if self.zone is not None:
                name += f' {format_name(self.zone)}'
        elif self.__class__.__name__ == 'Pet':
            name = format_name('_'.join(self.name.split('_')[:-1]))
        else:
            name = format_name(self.name)

        if getattr(self, 'stars', None) is None:
            stars = ''
        elif self.stars <= 5:
            stars = f' {GOLD}' + self.stars * '✪'
        else:
            stars = (f' {RED}' + (self.stars - 5) * '✪'
                     + GOLD + (10 - self.stars) * '✪')

        if self.__class__.__name__ == 'Pet':
            lvl = calc_pet_level(self.rarity, self.exp)
            info = f'{GRAY}[Lvl {lvl}] {rarity_color}{name}'
        elif self.__class__.__name__ == 'Minion':
            tier_str = format_roman(self.tier)
            info = f'{rarity_color}{name} {tier_str}'
        else:
            info = f'{rarity_color}{modifier}{name}{stars}'

        basic_stats = []
        bonus_stats = []

        if self.__class__.__name__ == 'Accessory':
            if self.modifier is not None:
                modifier_bonus = get_modifier(self.modifier, self.rarity)
            else:
                modifier_bonus = {}

            for stat_name in ('strength', 'crit_chance', 'crit_damage',
                              'attack_speed'):
                display_stat = format_name(stat_name)
                ext = '%' if stat_name[0] in 'ac' else ''

                if stat_name not in modifier_bonus:
                    continue

                value = fround(modifier_bonus[stat_name], 1)
                value_str = format_number(value, sign=True)
                bonus = (f' {BLUE}({format_name(self.modifier)}'
                         f' {value_str}{ext})')

                if value == 0:
                    continue

                basic_stats.append(f'{display_stat}: {RED}'
                                   f'{value_str}{ext}{bonus}')

            if len(basic_stats) != 0:
                info += '\n' + '\n'.join(f'{GRAY}{stat}'
                                         for stat in basic_stats)

            for stat_name in ('health', 'defense', 'intelligence', 'speed'):
                display_stat = format_name(stat_name)
                ext = ' HP' if stat_name[0] == 'h' else ''

                if stat_name not in modifier_bonus:
                    continue

                value = fround(modifier_bonus[stat_name], 1)
                value_str = format_number(value, sign=True)
                bonus = (f' {BLUE}({format_name(self.modifier)}'
                         f' {value_str}{ext})')

                if value == 0:
                    continue

                bonus_stats.append(f'{display_stat}: {GREEN}'
                                   f'{value_str}{ext}{bonus}')

            if len(bonus_stats) != 0:
                if len(basic_stats) != 0:
                    info += '\n'
                info += '\n' + '\n'.join(f'{GRAY}{stat}'
                                         for stat in bonus_stats)

        elif self.__class__.__name__ == 'Armor':
            is_dungeon = self.stars is not None

            if self.modifier is not None:
                modifier_bonus = get_modifier(self.modifier, self.rarity)
            else:
                modifier_bonus = {}

            for stat_name in ('strength', 'crit_chance', 'crit_damage',
                              'attack_speed', 'sea_creature_chance'):
                display_stat = format_name(stat_name)
                ext = ('%' if stat_name[0] in 'ac'
                       or stat_name.startswith('sea') else '')
                value = self.get_stat(stat_name, profile)

                bonus = ''
                if stat_name in modifier_bonus:
                    bonus_value = modifier_bonus[stat_name]
                    bonus_str = format_number(bonus_value, sign=True)
                    bonus += (f' {BLUE}({format_name(self.modifier)}'
                              f' {bonus_str}{ext})')

                if is_dungeon:
                    dung_value = dung_stat(value, catacombs_level, self.stars)
                    if value != dung_value:
                        dung_str = format_number(fround(dung_value, 1),
                                                 sign=True)
                        bonus += f' {DARK_GRAY}({dung_str}{ext})'

                value = fround(value, 1)
                if value == 0:
                    continue

                value_str = format_number(value, sign=True)
                basic_stats.append(f'{display_stat}: {RED}'
                                   f'{value_str}{ext}{bonus}')

            if len(basic_stats) != 0:
                info += '\n' + '\n'.join(f'{GRAY}{stat}'
                                         for stat in basic_stats)

            for stat_name in ('health', 'defense', 'intelligence', 'speed',
                              'magic_find', 'mining_speed', 'mining_fortune',
                              'true_defense', 'ferocity'):
                display_stat = format_name(stat_name)
                ext = ' HP' if stat_name[0] == 'h' else ''
                value = self.get_stat(stat_name, profile)

                bonus = ''

                if stat_name[0] == 'h' and self.hot_potato != 0:
                    bonus += f' {YELLOW}(+{4 * self.hot_potato})'

                if stat_name[0] == 'd' and self.hot_potato != 0:
                    bonus += f' {YELLOW}(+{2 * self.hot_potato})'

                if stat_name in modifier_bonus:
                    bonus_value = modifier_bonus[stat_name]
                    bonus_str = format_number(bonus_value, sign=True)
                    bonus += (f' {BLUE}({format_name(self.modifier)}'
                              f' {bonus_str})')

                if is_dungeon:
                    dung_value = dung_stat(value, catacombs_level, self.stars)
                    if value != dung_value:
                        dung_str = format_number(fround(dung_value, 1),
                                                 sign=True)
                        bonus += f' {DARK_GRAY}({dung_str}{ext})'

                value = fround(value, 1)
                if value == 0:
                    continue

                value_str = format_number(value, sign=True)
                bonus_stats.append(f'{display_stat}: {GREEN}'
                                   f'{value_str}{ext}{bonus}')

            if len(bonus_stats) != 0:
                if len(basic_stats) != 0:
                    info += '\n'
                info += '\n' + '\n'.join(f'{GRAY}{stat}'
                                         for stat in bonus_stats)

        elif self.__class__.__name__ in {'Bow', 'Sword'}:
            is_dungeon = self.stars is not None

            if self.modifier is not None:
                modifier_bonus = get_modifier(self.modifier, self.rarity)
            else:
                modifier_bonus = {}

            for stat_name in ('damage', 'strength', 'crit_chance',
                              'crit_damage', 'attack_speed'):
                display_stat = format_name(stat_name)
                ext = '%' if stat_name[0] in 'ac' else ''
                value = self.get_stat(stat_name, profile)

                bonus = ''
                if stat_name[0] in 'ds' and self.hot_potato != 0:
                    bonus += f' {YELLOW}(+{2 * self.hot_potato})'

                if stat_name in modifier_bonus:
                    bonus_value = modifier_bonus[stat_name]
                    bonus_str = format_number(bonus_value, sign=True)
                    bonus += (f' {BLUE}({format_name(self.modifier)}'
                              f' {bonus_str}{ext})')

                if is_dungeon:
                    dung_value = dung_stat(value, catacombs_level, self.stars)
                    if stat_name == 'crit_chance':
                        dung_value = min(dung_value, 100)
                    if value != dung_value:
                        dung_str = format_number(fround(dung_value, 1),
                                                 sign=True)
                        bonus += f' {DARK_GRAY}({dung_str}{ext})'

                value = fround(value, 1)
                if value == 0:
                    continue

                value_str = format_number(value, sign=True)
                basic_stats.append(f'{display_stat}: {RED}'
                                   f'{value_str}{ext}{bonus}')

            if len(basic_stats) != 0:
                info += '\n' + '\n'.join(f'{GRAY}{stat}'
                                         for stat in basic_stats)

            for stat_name in ('defense', 'intelligence', 'true_defense',
                              'ferocity', 'speed'):
                display_stat = format_name(stat_name)
                value = self.get_stat(stat_name, profile)

                bonus = ''
                if stat_name in modifier_bonus:
                    bonus_value = modifier_bonus[stat_name]
                    bonus_str = format_number(bonus_value, sign=True)
                    bonus += (f' {BLUE}({format_name(self.modifier)}'
                              f' {bonus_str})')

                if is_dungeon:
                    dung_value = dung_stat(value, catacombs_level, self.stars)
                    if value != dung_value:
                        dung_str = format_number(fround(dung_value, 1),
                                                 sign=True)
                        bonus += f' {DARK_GRAY}({dung_str})'

                value = fround(value, 1)
                if value == 0:
                    continue

                value_str = format_number(value, sign=True)
                bonus_stats.append(
                    f'{display_stat}: {GREEN}{value_str}{bonus}')

            if len(bonus_stats) != 0:
                if len(basic_stats) != 0:
                    info += '\n'
                info += '\n' + '\n'.join(f'{GRAY}{stat}'
                                         for stat in bonus_stats)

        elif self.__class__.__name__ in {'Drill', 'Pickaxe'}:
            info += f'\n{DARK_GRAY}Breaking Power {self.breaking_power}\n'

            for stat_name in ('damage', 'defense', 'intelligence'):
                display_stat = format_name(stat_name)
                value = self.get_stat(stat_name, profile)

                value = fround(value, 1)
                if value == 0:
                    continue

                value_str = format_number(value)
                basic_stats.append(f'{display_stat}: {RED}+{value_str}')

            if len(basic_stats) != 0:
                info += '\n' + '\n'.join(f'{GRAY}{stat}'
                                         for stat in basic_stats)

            for stat_name in ('mining_speed', 'mining_fortune'):
                display_stat = format_name(stat_name)
                value = self.get_stat(stat_name, profile)

                if value == 0:
                    continue

                value_str = format_number(fround(value, 1), sign=True)
                bonus_stats.append(f'{display_stat}: {GREEN}{value_str}')

            if len(bonus_stats) != 0:
                if len(basic_stats) != 0:
                    info += '\n'
                info += '\n' + '\n'.join(f'{GRAY}{stat}'
                                         for stat in bonus_stats)

        elif self.__class__.__name__ == 'FishingRod':
            is_dungeon = self.stars is not None

            if self.modifier is not None:
                modifier_bonus = get_modifier(self.modifier, self.rarity)
            else:
                modifier_bonus = {}

            for stat_name in (
                'damage', 'strength', 'crit_chance', 'crit_damage',
                'attack_speed', 'sea_creature_chance',
            ):
                display_stat = format_name(stat_name)
                ext = '%' if 'sea' in stat_name or stat_name[0] in 'ac' else ''
                value = self.get_stat(stat_name, profile)

                bonus = ''
                if stat_name[0] in 'ds' and self.hot_potato != 0:
                    bonus += f' {YELLOW}(+{2 * self.hot_potato})'

                if stat_name in modifier_bonus:
                    bonus_value = modifier_bonus[stat_name]
                    bonus_str = format_number(bonus_value, sign=True)
                    bonus += (f' {BLUE}({format_name(self.modifier)}'
                              f' {bonus_str}{ext})')

                if is_dungeon:
                    dung_value = dung_stat(value, catacombs_level, self.stars)
                    if value != dung_value:
                        dung_str = format_number(fround(dung_value, 1),
                                                 sign=True)
                        bonus += f' {DARK_GRAY}({dung_str}{ext})'

                value = fround(value, 1)
                if value == 0:
                    continue

                value_str = format_number(value, sign=True)
                basic_stats.append(f'{display_stat}: {RED}'
                                   f'{value_str}{ext}{bonus}')

            if len(basic_stats) != 0:
                info += '\n' + '\n'.join(f'{GRAY}{stat}'
                                         for stat in basic_stats)

            for stat_name in ('defense', 'intelligence', 'ferocity', 'speed'):
                display_stat = format_name(stat_name)
                value = self.get_stat(stat_name, profile)

                if stat_name in modifier_bonus:
                    bonus_value = modifier_bonus[stat_name]
                    bonus_str = format_number(bonus_value, sign=True)
                    bonus += (f' {BLUE}({format_name(self.modifier)}'
                              f' {bonus_str})')

                if is_dungeon:
                    dung_value = dung_stat(value, catacombs_level, self.stars)
                    if value != dung_value:
                        dung_str = format_number(fround(dung_value, 1),
                                                 sign=True)
                        bonus += f' {DARK_GRAY}({dung_str})'

                value = fround(value, 1)
                if value == 0:
                    continue

                value_str = format_number(value, sign=True)
                bonus_stats.append(
                    f'{display_stat}: {GREEN}{value_str}{bonus}')

            if len(bonus_stats) != 0:
                if len(basic_stats) != 0:
                    info += '\n'
                info += '\n' + '\n'.join(f'{GRAY}{stat}'
                                         for stat in bonus_stats)

        elif self.__class__.__name__ == 'Hoe':
            for stat_name in ('farming_fortune',):
                display_stat = format_name(stat_name)
                value = getattr(self, stat_name, 0)

                value = fround(value, 1)
                if value == 0:
                    continue

                value_str = format_number(value, sign=True)
                bonus_stats.append(f'{display_stat}: {GREEN}{value_str}')

            if len(bonus_stats) != 0:
                info += '\n' + '\n'.join(f'{GRAY}{stat}'
                                         for stat in bonus_stats)

        if self.__class__.__name__ == 'ReforgeStone':
            if self.category == 'accessory':
                type_str = 'accessories'
            elif self.category == 'melee':
                type_str = 'a melee weapon'
            elif self.category == 'bow':
                type_str = 'a bow'
            elif self.category == 'armor':
                type_str = 'armor'
            elif self.category == 'pickaxe':
                type_str = 'a pickaxe'

            info += (
                f'\n{DARK_GRAY}Reforge Stone\n\n'
                f'{GRAY}Can be used in a Reforge Anvil\n'
                f'or with the Dungeon Blacksmith\n'
                f'to apply the {BLUE}{format_name(self.modifier)}\n'
                f'{GRAY}reforge to {type_str}.'
            )

            if getattr(self, 'mining_skill_req', None) is not None:
                if mining_level < self.mining_skill_req:
                    info += (f'\n\n{GRAY}Requires {GREEN}Mining Skill Level\n'
                             f'{self.mining_skill_req}{GRAY}!{CLN}')

        elif self.__class__.__name__ == 'Pet':
            category = format_name(self.category)
            info += f'\n{DARK_GRAY}{category} Pet'

            pet_level = calc_pet_level(self.rarity, self.exp)
            lvl_mult = pet_level / 100

            stats = []
            for stat_name in (
                'health', 'defense', 'speed', 'true_defense',
                'intelligence', 'strength', 'crit_chance', 'crit_damage',
                'damage', 'magic_find', 'attack_speed', 'ferocity',
                'sea_creature_chance',
            ):
                display_stat = format_name(stat_name)
                value = getattr(self, stat_name) * lvl_mult

                ext = ''
                if stat_name[0] == 'h':
                    ext = ' HP'
                elif stat_name[0] == 'ac' or stat_name.startswith('sea'):
                    ext = '%'

                value = fround(value, 1)
                if value == 0:
                    continue

                value_str = format_number(value, sign=True)
                stats.append(f'{display_stat}: {GREEN}{value_str}{ext}')

            stats_str = '\n'.join(f'{GRAY}{stat}' for stat in stats)
            info += f'\n\n{stats_str}{CLN}'

            if pet_level == 100:
                info += f'\n\n{AQUA}MAX LEVEL'
            else:
                next_level = min(pet_level + 1, 100)
                exp_left, exp_to_next = calc_pet_upgrade_exp(self.rarity,
                                                             self.exp)
                perc = fround(exp_left / exp_to_next * 100, 1)
                bar = min(int(exp_left / exp_to_next * 20), 20)
                left, right = '-' * bar, '-' * (20 - bar)
                info += (
                    f'\n\n{GRAY}Progress to Level {next_level}:'
                    f' {YELLOW}{format_number(perc)}%\n'
                    f'{GREEN}{BOLD}{left}{GRAY}{BOLD}{right}'
                    f' {YELLOW}{format_number(floor(exp_left))}'
                    f'{GOLD}/{YELLOW}{format_short(exp_to_next)}'
                )

        elif self.__class__.__name__ == 'TravelScroll':
            r_name = ('Spawn' if self.zone is None
                      else format_name(self.zone))
            info += (f'\n{GRAY}Consume this item to add its\n'
                     f'destination to your fast travel\noptions.\n\n'
                     f'Island: {GREEN}{format_name(self.island)}{GRAY}\n'
                     f'Teleport: {YELLOW}{r_name}')

        ability_list = []

        if self.__class__.__name__ == 'Pet':
            stat_mult = lvl_mult
        else:
            stat_mult = 1

        item_abilities = getattr(self, 'abilities', [])
        if self.__class__.__name__ == 'Accessory':
            item_abilities = [self.name] + item_abilities
        for ability_id in item_abilities:
            ability = get_ability(ability_id)
            ability_str = ''
            if ability.__class__.__name__ == 'NamedAbility':
                ability_str += f'{GOLD}{ability.name}\n'

            temp_param = ability.variables.copy()
            for param_key, param_value in temp_param.items():
                if isinstance(param_value, (int, float)):
                    temp_param[param_key] = param_value * stat_mult

            temp_str = format_temp(get_template('abilities',
                                                ability.display_id),
                                   temp_param)
            ability_list.append(f'{ability_str}{GRAY}{temp_str}')

        if len(ability_list) != 0:
            if len(basic_stats) + len(bonus_stats) != 0:
                info += '\n'
            elif self.__class__.__name__ == 'Pet':
                info += '\n'
            info += '\n' + '\n\n'.join(ability_list)

        enchant_list = []

        if getattr(self, 'enchantments', {}) != {}:
            enchants = self.enchantments
            enchant_names = [*enchants.keys()]
            ult_ench = []

            for name in enchant_names:
                if name in ULTIMATE_ENCHS:
                    ult_ench = [name]
                    enchant_names.remove(name)
                    break

            enchant_names = ult_ench + sorted(enchant_names)

            while len(enchant_names) != 0:
                if len(enchant_names) == 1:
                    name = enchant_names[0]
                    lvl = enchants[name]
                    if name in ULTIMATE_ENCHS:
                        enchant_color = f'{LIGHT_PURPLE}{BOLD}'
                    elif name in ENCH_LVLS and ENCH_LVLS[name] < lvl:
                        enchant_color = GOLD
                    else:
                        enchant_color = BLUE
                    lvl_str = '' if lvl == 0 else f' {format_roman(lvl)}'
                    enchant_list.append(
                        f'{enchant_color}{format_name(name)}{lvl_str}{CLN}'
                    )
                    break

                name = enchant_names[0]
                lvl = enchants[name]
                if name in ULTIMATE_ENCHS:
                    enchant_color = f'{LIGHT_PURPLE}{BOLD}'
                elif name in ENCH_LVLS and ENCH_LVLS[name] < lvl:
                    enchant_color = GOLD
                else:
                    enchant_color = BLUE
                lvl_str = '' if lvl == 0 else f' {format_roman(lvl)}'
                enchant_str = f'{enchant_color}{format_name(name)}{lvl_str}'

                for i in range(1, 3):
                    if len(enchant_names) <= i:
                        break
                    name = enchant_names[i]
                    lvl = enchants[name]
                    if name in ENCH_LVLS and ENCH_LVLS[name] < lvl:
                        enchant_color = GOLD
                    else:
                        enchant_color = BLUE
                    lvl_str = '' if lvl == 0 else f' {format_roman(lvl)}'
                    enchant_str += (f'{BLUE}, {enchant_color}'
                                    f'{format_name(name)}{lvl_str}')

                enchant_list.append(enchant_str)

                enchant_names = enchant_names[3:]

            if not self.__class__.__name__ in {'EnchantedBook'}:
                info += '\n'
            info += '\n' + '\n'.join(enchant_list)

        footers = []
        if hasattr(self, 'modifier') and self.modifier is None:
            footers.append(f'{DARK_GRAY}This item can be reforged!')

        if getattr(self, 'combat_skill_req', None) is not None:
            if combat_level < self.combat_skill_req:
                footers.append(f'{DARK_RED}❣ {RED}Requires {GREEN}'
                               f'Combat Skill {self.combat_skill_req}')
        if getattr(self, 'dungeon_skill_req', None) is not None:
            if catacombs_level < self.dungeon_skill_req:
                footers.append(f'{DARK_RED}❣ {RED}Requires {GREEN}'
                               f'Catacombs Skill {self.dungeon_skill_req}')
        if getattr(self, 'dungeon_completion_req', None) is not None:
            footers.append(f'{DARK_RED}❣ {RED}Requires {GREEN}'
                           f'Catacombs Floor'
                           f' {format_roman(self.dungeon_completion_req)}'
                           f' Completion')
        if getattr(self, 'fishing_skill_req', None) is not None:
            if fishing_level < self.fishing_skill_req:
                footers.append(f'{DARK_RED}❣ {RED}Requires {GREEN}'
                               f'Fishing Skill {self.fishing_skill_req}')

        if self.__class__.__name__ == 'Minion':
            footers.extend([
                f'{GRAY}Time Between Action: {GREEN}{self.cooldown}s',
                f'{GRAY}Max Storage: {YELLOW}{self.slots * 64}'
            ])

        if self.__class__.__name__ == 'Armor':
            type_name = self.part.upper()
        elif self.__class__.__name__ == 'FishingRod':
            type_name = 'FISHING ROD'
        elif self.__class__.__name__ == 'ReforgeStone':
            type_name = 'REFORGE STONE'
        elif self.__class__.__name__ in {
            'Item', 'Pet', 'TravelScroll', 'EnchantedBook', 'Minion',
        }:
            type_name = ''
        else:
            type_name = self.__class__.__name__.upper()
        if getattr(self, 'stars', None) is not None:
            type_name = f'DUNGEON {type_name}'

        if self.__class__.__name__ == 'Minion':
            pass
        else:
            footers.append(f'{rarity_color}{self.rarity.upper()}'
                           f' {type_name}'.rstrip())

        info += '\n\n' + '\n'.join(footers)

        info += CLN

        return info

    cls.info = info

    def get_stat(self, name: str, profile, /, *, default: int = 0) -> Number:
        value = getattr(self, name, default)
        enchants = getattr(self, 'enchantments', {})
        self_name = getattr(self, 'name', None)
        abilities = getattr(self, 'abilities', [])

        set_bonus = True
        for piece in profile.armor:
            if piece.__class__.__name__ == 'Empty':
                set_bonus = False
                break

            for current_ability in piece.abilities:
                if current_ability in SET_BONUSES:
                    break
            else:
                continue
            if set_bonus is True:
                set_bonus = current_ability
            elif set_bonus is not False:
                if current_ability != set_bonus:
                    set_bonus = False

        active_pet = profile.get_active_pet()
        has_active_pet = active_pet.__class__.__name__ == 'Pet'
        if has_active_pet:
            pet_level = calc_pet_level(active_pet.rarity, active_pet.exp)
            pet_mult = pet_level / 100
        else:
            pet_level = 0
            pet_mult = 0

        if name == 'damage':
            if self_name == 'aspect_of_the_jerry':
                if enchants.get('ultimate_jerry', 0) != 0:
                    value *= enchants['ultimate_jerry'] * 10
                if has_active_pet:
                    if 'jerry_damage' in active_pet.abilities:
                        value += pet_mult * 50

            elif self_name == 'aspect_of_the_dragons':
                if has_active_pet:
                    if 'one_with_the_dragons' in active_pet.abilities:
                        value += pet_mult * 50

            elif self_name == 'aspect_of_the_end':
                if set_bonus == 'strong_blood':
                    value += 75

            elif 'pure_emerald' in abilities:
                value += 2.5 * sqrt(sqrt(profile.purse))

            if 'raider_axe' in abilities:
                kill_count = getattr(self, 'kill_count', 0)
                value += min(35, kill_count // 500)

            if enchants.get('one_for_all', 0) != 0:
                value *= 3.1

            if has_active_pet:
                value += active_pet.damage

                if 'legendary_primal_force' in active_pet.abilities:
                    value += pet_mult * 20
                elif 'epic_primal_force' in active_pet.abilities:
                    value += pet_mult * 15
                elif 'rare_primal_force' in active_pet.abilities:
                    value += pet_mult * 10
                elif 'uncommon_primal_force' in active_pet.abilities:
                    value += pet_mult * 5
                elif 'common_primal_force' in active_pet.abilities:
                    value += pet_mult * 3

        elif name == 'health':
            value += enchants.get('growth', 0) * 15
        elif name == 'defense':
            value += enchants.get('protection', 0) * 3
            if (profile.island in {'gold', 'deep', 'mines'}
                    and 'mining_double_defense' in abilities):
                value *= 2
        elif name == 'true_defense':
            value += enchants.get('true_protection', 0) * 3
        elif name == 'intelligence':
            value += enchants.get('big_brain', 0) * 5
            value += enchants.get('smarty_pants', 0) * 5
        elif name == 'strength':
            if 'raider_axe' in abilities:
                wood_collection = 0
                wood_collection += profile.get_collection_amount('oak_wood')
                wood_collection += profile.get_collection_amount('birch_wood')
                wood_collection += profile.get_collection_amount('spruce_wood')
                wood_collection += profile.get_collection_amount('dark_oak_wood')
                wood_collection += profile.get_collection_amount('acacia_wood')
                wood_collection += profile.get_collection_amount('jungle_wood')
                value += min(100, wood_collection // 500)

            if self_name == 'aspect_of_the_dragons':
                if has_active_pet:
                    if 'one_with_the_dragons' in active_pet.abilities:
                        value += pet_mult * 30

            if has_active_pet:
                if 'legendary_primal_force' in active_pet.abilities:
                    value += pet_mult * 20
                elif 'epic_primal_force' in active_pet.abilities:
                    value += pet_mult * 15
                elif 'rare_primal_force' in active_pet.abilities:
                    value += pet_mult * 10
                elif 'uncommon_primal_force' in active_pet.abilities:
                    value += pet_mult * 5
                elif 'common_primal_force' in active_pet.abilities:
                    value += pet_mult * 3
        elif name == 'speed':
            value += enchants.get('sugar_rush', 0) * 2
        elif name == 'crit_damage':
            value += enchants.get('critical', 0) * 10
        elif name == 'mining_speed':
            if enchants.get('efficiency', 0) != 0:
                value += 10 + 20 * enchants['efficiency']
        elif name == 'sea_creature_chance':
            value += enchants.get('angler', 0)
        elif name == 'ferocity':
            value += enchants.get('vicious', 0)

        if self.__class__.__name__ == 'Armor':
            if name == 'health':
                value += 4 * self.hot_potato
            elif name == 'defense':
                value += 2 * self.hot_potato
        elif self.__class__.__name__ in {'FishingRod', 'Bow', 'Sword'}:
            if name in {'damage', 'strength'}:
                value += 2 * self.hot_potato

        active_pet = profile.get_active_pet()
        has_active_pet = active_pet.__class__.__name__ == 'Pet'
        if has_active_pet and enchants.get('chimera', 0) != 0:
            value += getattr(active_pet, name, 0) * pet_mult * 0.2

        if getattr(self, 'modifier', None) is not None:
            modifier_bonus = get_modifier(self.modifier, self.rarity)
            value += modifier_bonus.get(name, 0)

        return value

    cls.get_stat = get_stat

    return cls
