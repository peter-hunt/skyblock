from math import floor

from ..constant.color import (
    RARITY_COLORS,
    CLN, BOLD, DARK_RED, GOLD, GRAY, DARK_GRAY,
    BLUE, GREEN, RED, LIGHT_PURPLE, YELLOW, WHITE,
)
from ..constant.enchanting import ULTIMATE_ENCHS
from ..function.math import calc_pet_lvl, calc_pet_upgrade_exp, dung_stat
from ..function.util import (
    display_int, display_name, roman, shorten_number,
)

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

    if cls.__name__ == 'Empty':
        to_obj_str = 'lambda self: {}'
    else:
        to_obj_str = 'lambda self: {'
        for key in anno:
            to_obj_str += f'{key!r}: self.{key}, '
        to_obj_str += f"'type': {cls.__name__.lower()!r}}}"

    cls.to_obj = eval(to_obj_str)

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

        if getattr(self, 'modifer', None) is not None:
            modifier = f'{self.modifier.capitalize()} '
        else:
            modifier = ''

        if self.__class__.__name__ == 'TravelScroll':
            name = f'Travel Scroll to {display_name(self.island)}'
            if self.region is not None:
                name += f' {display_name(self.region)}'
        elif self.__class__.__name__ == 'Pet':
            name = display_name('_'.join(self.name.split('_')[:-1]))
        else:
            name = display_name(self.name)

        count = (f' x {display_int(self.count)}'
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
            return f'{color}{modifier}{name}{stars}{DARK_GRAY}{count}{CLN}'

    cls.display = display

    def info(self, /, *, combat_lvl=0, cata_lvl=0):
        rarity_color = RARITY_COLORS[self.rarity]

        if getattr(self, 'modifer', None) is not None:
            modifier = f'{self.modifier.capitalize()} '
        else:
            modifier = ''

        if self.__class__.__name__ == 'TravelScroll':
            name = f'Travel Scroll to {display_name(self.island)}'
            if self.region is not None:
                name += f' {display_name(self.region)}'
        elif self.__class__.__name__ == 'Pet':
            name = display_name('_'.join(self.name.split('_')[:-1]))
        else:
            name = display_name(self.name)

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

        if self.__class__.__name__ in {'Pickaxe', 'Drill'}:
            info += (f'\n{DARK_GRAY}Breaking Power '
                     f"{getattr(self, 'breaking_power')}{CLN}\n"
                     f'\n{GRAY}Mining Speed: {GREEN}+'
                     f"{getattr(self, 'mining_speed')}{CLN}")

        elif self.__class__.__name__ in {'Bow', 'Sword'}:
            enchantments = getattr(self, 'enchantments', {})
            is_dungeon = self.stars is not None

            basic_stats = []
            for stat_name in ('damage', 'strength', 'crit_chance',
                              'crit_damage', 'attack_speed'):
                if getattr(self, stat_name, 0) == 0:
                    if stat_name[0] not in 'ds' or self.hot_potato == 0:
                        continue

                display_stat = display_name(stat_name)
                ext = '%' if stat_name[0] in 'ac' else ''
                value = getattr(self, stat_name)

                hot_potato = ''
                if stat_name[0] in 'ds' and self.hot_potato != 0:
                    value += self.hot_potato
                    hot_potato = f' {YELLOW}(+{self.hot_potato})'

                if stat_name == 'damage':
                    if enchantments.get('one_for_all', 0) != 0:
                        value *= 3.1

                dung = ''
                if is_dungeon:
                    dungeon_value = dung_stat(value, cata_lvl, self.stars)
                    if stat_name in {'crit_chance', 'attack_speed'}:
                        dungeon_value = min(dungeon_value, 100)
                    if value != dungeon_value:
                        value_str = f'{dungeon_value:.1f}'
                        if value_str.endswith('.0'):
                            value_str = value_str[:-2]
                        dung = f' {DARK_GRAY}(+{value_str}{ext})'

                if value < 1:
                    continue

                basic_stats.append(f'{display_stat}: {RED}'
                                   f'+{value:.0f}{ext}{hot_potato}{dung}')

            if len(basic_stats) != 0:
                info += '\n' + '\n'.join(f'{GRAY}{stat}'
                                         for stat in basic_stats)

            bonus_stats = []
            for stat_name in ('defense', 'intelligence', 'true_defense',
                              'ferocity', 'speed'):
                if getattr(self, stat_name, 0) == 0:
                    continue

                display_stat = display_name(stat_name)
                value = getattr(self, stat_name)

                dung = ''
                if is_dungeon:
                    dungeon_value = dung_stat(value, cata_lvl, self.stars)
                    if stat_name in {'crit_chance', 'attack_speed'}:
                        dungeon_value = min(dungeon_value, 100)
                    if value != dungeon_value:
                        value_str = f'{dungeon_value:.1f}'
                        if value_str.endswith('.0'):
                            value_str = value_str[:-2]
                        dung = f' {DARK_GRAY}(+{value_str})'

                bonus_stats.append(f'{display_stat}: {GREEN}'
                                   f'+{value}{dung}')

            if len(bonus_stats) != 0:
                info += '\n' + '\n'.join(f'{GRAY}{stat}'
                                         for stat in bonus_stats)

        elif self.__class__.__name__ == 'Armor':
            enchantments = getattr(self, 'enchantments', {})
            is_dungeon = self.stars is not None

            basic_stats = []
            for stat_name in ('strength', 'crit_chance', 'crit_damage'):
                if getattr(self, stat_name, 0) == 0:
                    continue

                display_stat = display_name(stat_name)
                ext = '%' if stat_name[0] in 'ac' else ''
                value = getattr(self, stat_name)

                dung = ''
                if is_dungeon:
                    dungeon_value = dung_stat(value, cata_lvl, self.stars)
                    if stat_name == 'crit_chance':
                        dungeon_value = min(dungeon_value, 100)
                    if value != dungeon_value:
                        value_str = f'{dungeon_value:.1f}'
                        if value_str.endswith('.0'):
                            value_str = value_str[:-2]
                        dung = f' {DARK_GRAY}(+{value_str}{ext})'

                basic_stats.append(f'{display_stat}: {RED}'
                                   f'+{value}{ext}{dung}')

            if len(basic_stats) != 0:
                info += '\n' + '\n'.join(f'{GRAY}{stat}'
                                         for stat in basic_stats)

            bonus_stats = []
            for stat_name in ('health', 'defense', 'intelligence', 'speed',
                              'magic_find', 'mining_speed', 'mining_fortune',
                              'true_defense', 'ferocity',
                              'sea_creature_chance'):

                display_stat = display_name(stat_name)
                value = getattr(self, stat_name, 0)

                if stat_name == 'health':
                    value += enchantments.get('growth', 0) * 15
                elif stat_name == 'protection':
                    value += enchantments.get('protection', 0) * 3
                elif stat_name == 'mining_speed':
                    if 'efficiency' in enchantments:
                        value += 10 + enchantments['efficiency'] * 20

                hot_potato = ''
                if stat_name[0] in 'dh' and self.hot_potato != 0:
                    value += self.hot_potato
                    hot_potato = f' {YELLOW}(+{self.hot_potato})'

                if value == 0:
                    continue

                ext = ' HP' if stat_name[0] == 'h' else ''

                dung = ''
                if is_dungeon:
                    dungeon_value = dung_stat(value, cata_lvl, self.stars)
                    if value != dungeon_value:
                        value_str = f'{dungeon_value:.1f}'
                        if value_str.endswith('.0'):
                            value_str = value_str[:-2]
                        dung = f' {DARK_GRAY}(+{value_str}{ext})'

                bonus_stats.append(f'{display_stat}: {GREEN}'
                                   f'+{value}{ext}{hot_potato}{dung}')

            if len(bonus_stats) != 0:
                info += '\n' + '\n'.join(f'{GRAY}{stat}'
                                         for stat in bonus_stats)

        elif self.__class__.__name__ == 'Pet':
            category = display_name(self.category)
            info += f'\n{DARK_GRAY}{category} Pet'

            pet_lvl = calc_pet_lvl(self.rarity, self.exp)
            lvl_mult = pet_lvl / 100

            stats = []
            for stat_name in ('health', 'defense', 'speed', 'true_defense',
                              'intelligence', 'strength', 'crit_chance',
                              'crit_damage', 'magic_find', 'attack_speed',
                              'ferocity'):
                if getattr(self, stat_name, 0) == 0:
                    continue

                display_stat = display_name(stat_name)
                value = getattr(self, stat_name) * lvl_mult

                ext = ''
                if stat_name[0] == 'h':
                    ext = ' HP'
                elif stat_name[0] == 'ac':
                    ext = '%'

                stats.append(f'{display_stat}: {GREEN}'
                             f'+{display_int(floor(value))}{ext}')

            stats_str = '\n'.join(f'{GRAY}{stat}' for stat in stats)
            info += f'\n\n{stats_str}{CLN}'

            next_level = min(pet_lvl + 1, 100)
            if pet_lvl == 100:
                exp_left, exp_to_next = calc_pet_upgrade_exp(self.rarity,
                                                             self.exp)
                info += (
                    f"\n\n{GREEN}{BOLD}{'-' * 20}"
                    f' {YELLOW}{display_int(floor(exp_left))}'
                    f'/{shorten_number(exp_to_next)}'
                )
            else:
                exp_left, exp_to_next = calc_pet_upgrade_exp(self.rarity,
                                                             self.exp)
                perc = round(exp_left / exp_to_next * 100, 1)
                bar = min(int(exp_left / exp_to_next * 20), 20)
                left, right = '-' * bar, '-' * (20 - bar)
                info += (
                    f'\n\n{GRAY}Progress to Level {next_level}:'
                    f' {YELLOW}{display_int(perc)}%\n'
                    f'{GREEN}{BOLD}{left}{GRAY}{BOLD}{right}'
                    f' {YELLOW}{display_int(floor(exp_left))}'
                    f'/{shorten_number(exp_to_next)}'
                )

        elif self.__class__.__name__ == 'TravelScroll':
            r_name = ('Spawn' if self.region is None
                      else display_name(self.region))
            info += (f'\n{GRAY}Consume this item to add its\n'
                     f'destination to your fast travel\noptions.\n\n'
                     f'Island: {GREEN}{display_name(self.island)}{GRAY}\n'
                     f'Teleport: {YELLOW}{r_name}')

        while '\n' in info and info.split('\n')[1] == '':
            info = '\n'.join([info.split('\n')[0]] + info.split('\n')[2:])

        if getattr(self, 'enchantments', {}) != {}:
            ench_str_list = []

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
                    ench_color = (f'{LIGHT_PURPLE}{BOLD}'
                                  if name in ULTIMATE_ENCHS else BLUE)
                    lvl = enchs[name]
                    lvl_str = '' if lvl == 0 else f' {roman(lvl)}'
                    ench_str_list.append(
                        f'{ench_color}{display_name(name)}{lvl_str}{CLN}'
                    )
                    break
                name = ench_names[0]
                ench_color = (f'{LIGHT_PURPLE}{BOLD}'
                              if name in ULTIMATE_ENCHS else BLUE)
                lvl = enchs[name]
                lvl_str = '' if lvl == 0 else f' {roman(lvl)}'
                ench_str = f'{ench_color}{display_name(name)}{lvl_str}, '

                name = ench_names[1]
                lvl = enchs[name]
                lvl_str = '' if lvl == 0 else f' {roman(lvl)}'
                ench_str += f'{BLUE}{display_name(name)}{lvl_str}{CLN}'
                ench_str_list.append(ench_str)

                ench_names = ench_names[2:]

            info += '\n\n' + '\n'.join(ench_str_list)

        info += '\n'
        if hasattr(self, 'modifier') and self.modifier is None:
            info += (f'\n{DARK_GRAY}This item can be reforged!{CLN}')

        if getattr(self, 'combat_skill_req', None) is not None:
            if combat_lvl < self.combat_skill_req:
                info += (f'\n{DARK_RED}❣ {RED}Requires '
                         f'{GREEN}Combat Skill {self.combat_skill_req}{CLN}')
        if getattr(self, 'dungeon_skill_req', None) is not None:
            if cata_lvl < self.dungeon_skill_req:
                info += (f'\n{DARK_RED}❣ {RED}Requires '
                         f'{GREEN}Catacombs Skill {self.dungeon_skill_req}{CLN}')
        if getattr(self, 'dungeon_completion_req', None) is not None:
            info += (f'\n{DARK_RED}❣ {RED}Requires {GREEN}Catacombs Floor '
                     f'{roman(self.dungeon_completion_req)} Completion{CLN}')

        if self.__class__.__name__ == 'Armor':
            type_name = self.part.upper()
        elif self.__class__.__name__ in {'Pet', 'TravelScroll'}:
            type_name = ''
        else:
            type_name = self.__class__.__name__.upper()
        if getattr(self, 'stars', None) is not None:
            type_name = f'DUNGEON {type_name}'

        info = info.rstrip('\n')
        if self.__class__.__name__ in {'Pet', 'TravelScroll'}:
            info += '\n'
        info += f'\n{rarity_color}{self.rarity.upper()} {type_name}'.rstrip()
        info += CLN

        # while '\n\n\n' in info:
        #     info = info.replace('\n\n\n', '\n\n')

        return info

    cls.info = info

    return cls
