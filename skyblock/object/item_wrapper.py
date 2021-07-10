from math import floor, sqrt
from typing import Any, Dict

from ..constant.ability import SET_BONUSES
from ..constant.color import *
from ..constant.enchanting import ENCH_LVLS, ULTIMATE_ENCHS
from ..constant.util import Number
from ..function.math import (
    calc_pet_lvl, calc_pet_upgrade_exp, dung_stat, fround,
)
from ..function.reforging import get_modifier
from ..function.util import (
    format_name, format_number, format_roman, format_short, format_zone,
)
from .ability import get_ability


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
                ench = getattr(self, key)
                result[key] = {ench_name: ench[ench_name]
                               for ench_name in sorted(ench)}
            else:
                result[key] = getattr(self, key)

        result['type'] = cls.__name__.lower()
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

        color = RARITY_COLORS[self.rarity]

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
            lvl = calc_pet_lvl(self.rarity, self.exp)
            return (f'{GRAY}[Lvl {lvl}] {color}{name}')
        else:
            return f'{color}{name}{stars}{DARK_GRAY}{count}{CLN}'

    cls.display = display

    def info(self, profile, /):
        mining_lvl = profile.get_skill_lvl('mining')
        combat_lvl = profile.get_skill_lvl('combat')
        fishing_lvl = profile.get_skill_lvl('fishing')
        cata_lvl = profile.get_skill_lvl('catacombs')
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
            lvl = calc_pet_lvl(self.rarity, self.exp)
            info = f'{GRAY}[Lvl {lvl}] {rarity_color}{name}'
        else:
            info = f'{rarity_color}{modifier}{name}{stars}'

        basic_stats = []
        bonus_stats = []

        if self.__class__.__name__ == 'ReforgeStone':
            if self.category == 'melee':
                type_str = 'a melee weapon'
            elif self.category == 'bow':
                type_str = 'a bow'
            elif self.category == 'armor':
                type_str = 'armor'

            info += (
                f'\n{DARK_GRAY}Reforge Stone\n\n'
                f'{GRAY}Can be used in a Reforge Anvil\n'
                f'or with the Dungeon Blacksmith\n'
                f'to apply the {BLUE}{format_name(self.modifier)}\n'
                f'{GRAY}reforge to {type_str}.'
            )

            if getattr(self, 'mining_skill_req', None) is not None:
                if mining_lvl < self.mining_skill_req:
                    info += (f'\n\n{GRAY}Requires {GREEN}Mining Skill Level\n'
                             f'{self.mining_skill_req}{GRAY}!{CLN}')

        elif self.__class__.__name__ in {'Pickaxe', 'Drill'}:
            info += f'\n{DARK_GRAY}Breaking Power {self.breaking_power}\n'

            for stat_name in ('damage',):
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

                value_str = format_number(round(value, 1), sign=True)
                bonus_stats.append(f'{display_stat}: {GREEN}{value_str}')

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
                    bonus += f' {YELLOW}(+{self.hot_potato})'

                if stat_name in modifier_bonus:
                    bonus_value = modifier_bonus[stat_name]
                    bonus_str = format_number(bonus_value, sign=True)
                    bonus += (f' {BLUE}({format_name(self.modifier)}'
                              f' {bonus_str}{ext})')

                if is_dungeon:
                    dung_value = dung_stat(value, cata_lvl, self.stars)
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
                    dung_value = dung_stat(value, cata_lvl, self.stars)
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
                    bonus += f' {YELLOW}(+{self.hot_potato})'

                if stat_name in modifier_bonus:
                    bonus_value = modifier_bonus[stat_name]
                    bonus_str = format_number(bonus_value, sign=True)
                    bonus += (f' {BLUE}({format_name(self.modifier)}'
                              f' {bonus_str}{ext})')

                if is_dungeon:
                    dung_value = dung_stat(value, cata_lvl, self.stars)
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
                    dung_value = dung_stat(value, cata_lvl, self.stars)
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

        elif self.__class__.__name__ == 'Armor':
            is_dungeon = self.stars is not None

            if self.modifier is not None:
                modifier_bonus = get_modifier(self.modifier, self.rarity)
            else:
                modifier_bonus = {}

            for stat_name in ('strength', 'crit_chance', 'crit_damage',
                              'attack_speed', 'sea_creature_chance'):
                display_stat = format_name(stat_name)
                ext = '%' if stat_name[0] in 'acs' else ''
                value = self.get_stat(stat_name, profile)

                bonus = ''
                if stat_name in modifier_bonus:
                    bonus_value = modifier_bonus[stat_name]
                    bonus_str = format_number(bonus_value, sign=True)
                    bonus += (f' {BLUE}({format_name(self.modifier)}'
                              f' {bonus_str}{ext})')

                if is_dungeon:
                    dung_value = dung_stat(value, cata_lvl, self.stars)
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

                if stat_name[0] in 'dh' and self.hot_potato != 0:
                    bonus += f' {YELLOW}(+{self.hot_potato})'

                if stat_name in modifier_bonus:
                    bonus_value = modifier_bonus[stat_name]
                    bonus_str = format_number(bonus_value, sign=True)
                    bonus += (f' {BLUE}({format_name(self.modifier)}'
                              f' {bonus_str})')

                if is_dungeon:
                    dung_value = dung_stat(value, cata_lvl, self.stars)
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

        elif self.__class__.__name__ == 'Pet':
            category = format_name(self.category)
            info += f'\n{DARK_GRAY}{category} Pet'

            pet_lvl = calc_pet_lvl(self.rarity, self.exp)
            lvl_mult = pet_lvl / 100

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
                elif stat_name[0] == 'ac':
                    ext = '%'

                value = fround(value, 1)
                if value == 0:
                    continue

                value_str = format_number(value, sign=True)
                stats.append(f'{display_stat}: {GREEN}{value_str}{ext}')

            stats_str = '\n'.join(f'{GRAY}{stat}' for stat in stats)
            info += f'\n\n{stats_str}{CLN}'

            if pet_lvl == 100:
                info += f'\n\n{AQUA}MAX LEVEL'
            else:
                next_level = min(pet_lvl + 1, 100)
                exp_left, exp_to_next = calc_pet_upgrade_exp(self.rarity,
                                                             self.exp)
                perc = round(exp_left / exp_to_next * 100, 1)
                bar = min(int(exp_left / exp_to_next * 20), 20)
                left, right = '-' * bar, '-' * (20 - bar)
                info += (
                    f'\n\n{GRAY}Progress to Level {next_level}:'
                    f' {YELLOW}{format_number(perc)}%\n'
                    f'{GREEN}{BOLD}{left}{GRAY}{BOLD}{right}'
                    f' {YELLOW}{format_number(floor(exp_left))}'
                    f'/{format_short(exp_to_next)}'
                )

        elif self.__class__.__name__ == 'TravelScroll':
            r_name = ('Spawn' if self.zone is None
                      else format_name(self.zone))
            info += (f'\n{GRAY}Consume this item to add its\n'
                     f'destination to your fast travel\noptions.\n\n'
                     f'Island: {GREEN}{format_name(self.island)}{GRAY}\n'
                     f'Teleport: {YELLOW}{r_name}')

        ability_list = []

        for ability_id in getattr(self, 'abilities', []):
            ability = get_ability(ability_id)
            if ability.__class__.__name__ == 'NamedAbility':
                ability_list.append(f'{GOLD}{ability.name}'
                                    f'\n{GRAY}{ability.description}')
            elif ability.__class__.__name__ == 'AnonymousAbility':
                ability_list.append(f'{GRAY}{ability.description}')

        if len(ability_list) != 0:
            if len(basic_stats) + len(bonus_stats) != 0:
                info += '\n'
            elif self.__class__.__name__ == 'Pet':
                info += '\n'
            info += '\n' + '\n\n'.join(ability_list)

        ench_list = []

        if getattr(self, 'enchantments', {}) != {}:
            enchs = self.enchantments
            ench_names = [*enchs.keys()]
            ult_ench = []

            for name in ench_names:
                if name in ULTIMATE_ENCHS:
                    ult_ench = [name]
                    ench_names.remove(name)
                    break

            ench_names = ult_ench + sorted(ench_names)

            while len(ench_names) != 0:
                if len(ench_names) == 1:
                    name = ench_names[0]
                    lvl = enchs[name]
                    if name in ULTIMATE_ENCHS:
                        ench_color = f'{LIGHT_PURPLE}{BOLD}'
                    elif name in ENCH_LVLS and ENCH_LVLS[name] < lvl:
                        ench_color = GOLD
                    else:
                        ench_color = BLUE
                    lvl_str = '' if lvl == 0 else f' {format_roman(lvl)}'
                    ench_list.append(
                        f'{ench_color}{format_name(name)}{lvl_str}{CLN}'
                    )
                    break

                name = ench_names[0]
                lvl = enchs[name]
                if name in ULTIMATE_ENCHS:
                    ench_color = f'{LIGHT_PURPLE}{BOLD}'
                elif name in ENCH_LVLS and ENCH_LVLS[name] < lvl:
                    ench_color = GOLD
                else:
                    ench_color = BLUE
                lvl_str = '' if lvl == 0 else f' {format_roman(lvl)}'
                ench_str = f'{ench_color}{format_name(name)}{lvl_str}'

                for i in range(1, 3):
                    if len(ench_names) <= i:
                        break
                    name = ench_names[i]
                    lvl = enchs[name]
                    if name in ENCH_LVLS and ENCH_LVLS[name] < lvl:
                        ench_color = GOLD
                    else:
                        ench_color = BLUE
                    lvl_str = '' if lvl == 0 else f' {format_roman(lvl)}'
                    ench_str += (f'{BLUE}, {ench_color}'
                                 f'{format_name(name)}{lvl_str}')

                ench_list.append(ench_str)

                ench_names = ench_names[3:]

            if not self.__class__.__name__ in {'EnchantedBook'}:
                info += '\n'
            info += '\n' + '\n'.join(ench_list)

        footers = []
        if hasattr(self, 'modifier') and self.modifier is None:
            footers.append(f'{DARK_GRAY}This item can be reforged!{CLN}')

        if getattr(self, 'combat_skill_req', None) is not None:
            if combat_lvl < self.combat_skill_req:
                footers.append(f'{DARK_RED}❣ {RED}Requires {GREEN}'
                               f'Combat Skill'
                               f' {self.combat_skill_req}{CLN}')
        if getattr(self, 'dungeon_skill_req', None) is not None:
            if cata_lvl < self.dungeon_skill_req:
                footers.append(f'{DARK_RED}❣ {RED}Requires {GREEN}'
                               f'Catacombs Skill'
                               f' {self.dungeon_skill_req}{CLN}')
        if getattr(self, 'dungeon_completion_req', None) is not None:
            footers.append(f'{DARK_RED}❣ {RED}Requires {GREEN}'
                           f'Catacombs Floor'
                           f' {format_roman(self.dungeon_completion_req)}'
                           f' Completion{CLN}')
        if getattr(self, 'fishing_skill_req', None) is not None:
            if fishing_lvl < self.fishing_skill_req:
                footers.append(f'{DARK_RED}❣ {RED}Requires {GREEN}'
                               f'Fishing Skill {self.fishing_skill_req}{CLN}')

        if self.__class__.__name__ == 'Armor':
            type_name = self.part.upper()
        elif self.__class__.__name__ == 'FishingRod':
            type_name = 'FISHING ROD'
        elif self.__class__.__name__ == 'ReforgeStone':
            type_name = 'REFORGE STONE'
        elif self.__class__.__name__ in {
            'Item', 'Pet', 'TravelScroll', 'EnchantedBook',
        }:
            type_name = ''
        else:
            type_name = self.__class__.__name__.upper()
        if getattr(self, 'stars', None) is not None:
            type_name = f'DUNGEON {type_name}'

        footers.append(f'{rarity_color}{self.rarity.upper()}'
                       f' {type_name}'.rstrip())

        info += '\n\n' + '\n'.join(footers)

        info += CLN

        return info

    cls.info = info

    def get_stat(self, name: str, profile, /, *, default: int = 0) -> Number:
        value = getattr(self, name, default)
        ench = getattr(self, 'enchantments', {})

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

        active_pet = None
        for pet in profile.pets:
            if pet.active:
                active_pet = pet
                break

        if name == 'damage':
            if self.name == 'aspect_of_the_jerry':
                if ench.get('ultimate_jerry', 0) != 0:
                    value *= ench.get('ultimate_jerry', 0) * 10
            if self.name == 'aspect_of_the_end':
                if set_bonus == 'strong_blood':
                    value += 75
            elif 'pure_emerald' in getattr(self, 'abilities', []):
                value += 2.5 * sqrt(sqrt(profile.purse))
            if ench.get('one_for_all', 0) != 0:
                value *= 3.1

            if active_pet is not None:
                value += active_pet.damage
        elif name == 'health':
            value += ench.get('growth', 0) * 15
        elif name == 'defense':
            value += ench.get('protection', 0) * 3
        elif name == 'true_defense':
            value += ench.get('true_protection', 0) * 3
        elif name == 'intelligence':
            value += ench.get('big_brain', 0) * 5
            value += ench.get('smarty_pants', 0) * 5
        elif name == 'speed':
            value += ench.get('sugar_rush', 0) * 2
        elif name == 'mining_speed':
            if ench.get('efficiency', 0) != 0:
                value += 10 + 20 * ench['efficiency']
        elif name == 'sea_creature_chance':
            value += ench.get('angler', 0)
        elif name == 'ferocity':
            value += ench.get('vicious', 0)

        if self.__class__.__name__ == 'Armor':
            if name in {'health', 'defense'}:
                value += self.hot_potato
        elif self.__class__.__name__ in {'FishingRod', 'Bow', 'Sword'}:
            if name in {'damage', 'strength'}:
                value += self.hot_potato

        if getattr(self, 'modifier', None) is not None:
            modifier_bonus = get_modifier(self.modifier, self.rarity)
            value += modifier_bonus.get(name, 0)

        return value

    cls.get_stat = get_stat

    return cls
