from ..constant.colors import (
    RARITY_COLORS,
    CLN, BOLD, DARK_RED, GOLD, GRAY, DARK_GRAY, GREEN, RED, YELLOW, WHITE,
)
from ..function.io import white
from ..function.math import dung_stat
from ..function.util import display_name, random_amount, random_bool, roman

__all__ = ['item_type', 'mob_type']


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

    def display(self):
        if self.__class__.__name__ == 'Empty':
            return f'{BOLD}{WHITE}Empty{CLN}'

        color = RARITY_COLORS[self.rarity]

        if getattr(self, 'modifer', None) is not None:
            modifier = f'{self.modifier.capitalize()} '
        else:
            modifier = ''

        name = display_name(self.name)
        count = f' x {self.count}' if getattr(self, 'count', 1) != 1 else ''

        if getattr(self, 'stars', None) is None:
            stars = ''
        elif self.stars <= 5:
            stars = f' {GOLD}' + self.stars * '✪'
        else:
            stars = (f' {RED}' + (self.stars - 5) * '✪'
                     + GOLD + (10 - self.stars) * '✪')

        return f'{color}{modifier}{name}{stars}{DARK_GRAY}{count}{CLN}'

    cls.display = display

    def info(self, cata_lvl=0):
        color = RARITY_COLORS[self.rarity]

        if getattr(self, 'modifer', None) is not None:
            modifier = f'{self.modifier.capitalize()} '
        else:
            modifier = ''

        name = display_name(self.name)

        if getattr(self, 'stars', None) is None:
            stars = ''
        elif self.stars <= 5:
            stars = f' {GOLD}' + self.stars * '✪'
        else:
            stars = (f' {RED}' + (self.stars - 5) * '✪'
                     + GOLD + (10 - self.stars) * '✪')

        info = f'{color}{modifier}{name}{stars}{color}'

        if self.__class__.__name__ == 'Pickaxe':
            info += (f'\n{DARK_GRAY}Breaking Power '
                     f"{getattr(self, 'breaking_power')}{CLN}\n"
                     f'\n{GRAY}Mining Speed: {GREEN}+'
                     f"{getattr(self, 'mining_speed')}{CLN}\n")

        if self.__class__.__name__ in {'Sword', 'Bow'}:
            is_dungeon = self.stars is not None
            basic_stats = []
            for stat_name in ('damage', 'strength', 'crit_chance',
                              'crit_damage', 'attack_speed'):
                if getattr(self, stat_name, 0) == 0:
                    if stat_name[0] not in 'ds' or self.hot_potato == 0:
                        continue

                display_stat = display_name(stat_name)
                perc = '%' if stat_name[0] in 'ac' else ''
                value = getattr(self, stat_name)

                hot_potato = ''
                if stat_name[0] in 'ds' and self.hot_potato != 0:
                    value += self.hot_potato
                    hot_potato = f' {YELLOW}(+{self.hot_potato})'

                dung = ''
                if is_dungeon:
                    dungeon_value = dung_stat(value, cata_lvl, self.stars)
                    if stat_name in {'crit_chance', 'attack_speed'}:
                        dungeon_value = min(dungeon_value, 100)
                    if value != dungeon_value:
                        value_str = f'{dungeon_value:.1f}'
                        if value_str.endswith('.0'):
                            value_str = value_str[:-2]
                        dung = f' {DARK_GRAY}(+{value_str}{perc})'

                basic_stats.append(f'{display_stat}: {RED}'
                                   f'+{value}{perc}{hot_potato}{dung}')

            info += '\n' + '\n'.join(f'{GRAY}{stat}{CLN}'
                                     for stat in basic_stats)

            bonus_stats = []
            for stat_name in ('defense', 'intelligence', 'true_denfense',
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
                        dung = f' {DARK_GRAY}(+{value_str}{perc})'

                bonus_stats.append(f'{display_stat}: {GREEN}'
                                   f'+{value}{dung}')

            info += '\n\n' + '\n'.join(f'{GRAY}{stat}{CLN}'
                                       for stat in bonus_stats)

        elif self.__class__.__name__ == 'Armor':
            is_dungeon = self.stars is not None
            basic_stats = []
            for stat_name in ('strength', 'crit_chance', 'crit_damage'):
                if getattr(self, stat_name, 0) == 0:
                    continue

                display_stat = display_name(stat_name)
                perc = '%' if stat_name[0] in 'ac' else ''
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
                        dung = f' {DARK_GRAY}(+{value_str}{perc})'

                basic_stats.append(f'{display_stat}: {RED}'
                                   f'+{value}{perc}{dung}')

            info += '\n' + '\n'.join(f'{GRAY}{stat}{CLN}'
                                     for stat in basic_stats)

            bonus_stats = []
            for stat_name in ('health', 'defense', 'intelligence', 'speed',
                              'magic_find', 'mining_speed', 'mining_fortune',
                              'true_denfense', 'ferocity',
                              'sea_creature_chance'):
                if getattr(self, stat_name, 0) == 0:
                    if stat_name[0] not in 'dh' or self.hot_potato == 0:
                        continue

                display_stat = display_name(stat_name)
                value = getattr(self, stat_name)

                hot_potato = ''
                if stat_name[0] in 'dh' and self.hot_potato != 0:
                    value += self.hot_potato
                    hot_potato = f' {YELLOW}(+{self.hot_potato})'

                hp = ''
                if stat_name == 'health':
                    hp = ' HP'

                dung = ''
                if is_dungeon:
                    dungeon_value = dung_stat(value, cata_lvl, self.stars)
                    if value != dungeon_value:
                        value_str = f'{dungeon_value:.1f}'
                        if value_str.endswith('.0'):
                            value_str = value_str[:-2]
                        dung = f' {DARK_GRAY}(+{value_str}{perc})'

                bonus_stats.append(f'{display_stat}: {GREEN}'
                                   f'+{value}{hp}{hot_potato}{dung}')

            info += '\n\n' + '\n'.join(f'{GRAY}{stat}{CLN}'
                                       for stat in bonus_stats)

        info += '\n'
        if hasattr(self, 'modifier'):
            info += (f'\n{DARK_GRAY}This item can be reforged!{CLN}')

        if getattr(self, 'combat_skill_req', None) is not None:
            info += (f'\n{DARK_RED}❣ {RED}Requires '
                     f'{GREEN}Combat Skill {self.combat_skill_req}{CLN}')
        if getattr(self, 'dungeon_skill_req', None) is not None:
            info += (f'\n{DARK_RED}❣ {RED}Requires '
                     f'{GREEN}Catacombs Skill {self.dungeon_skill_req}{CLN}')
        if getattr(self, 'dungeon_completion_req', None) is not None:
            info += (f'\n{DARK_RED}❣ {RED}Requires {GREEN}Catacombs Floor '
                     f'{roman(self.dungeon_completion_req)} Completion{CLN}')

        if self.__class__.__name__ == 'Armor':
            type_name = self.part.upper()
        else:
            type_name = self.__class__.__name__.upper()
        if getattr(self, 'stars', None) is not None:
            type_name = f'DUNGEON {type_name}'

        info += f'\n{color}{self.rarity.upper()} {type_name}{CLN}'

        while info.split('\n')[1] == '':
            info = '\n'.join([info.split('\n')[0]] + info.split('\n')[2:])

        while '\n\n\n' in info:
            info = info.replace('\n\n\n', '\n\n')

        return info

    cls.info = info

    return cls


def mob_type(cls):
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

    def drop(self, player):
        player.purse += self.coins
        player.add_skill_exp('combat', self.combat_xp)
        player.add_exp(self.xp_orb)

        for item, amount, rarity, drop_chance in self.drops:
            if not random_bool(drop_chance):
                continue

            loot = item.copy()
            loot.amount = random_amount(amount)
            if rarity == 'common':
                player.recieve(loot)
            else:
                rarity_str = rarity.upper()
                white(f'{RARITY_COLORS[rarity]}{rarity_str} DROP! '
                      f'({item.display()}{WHITE})')

    cls.drop = drop

    return cls
