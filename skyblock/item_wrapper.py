from .constant import (
    RARITY_COLORS,
    CLN, BOLD, F_DARK_RED, F_GOLD, F_GRAY, F_DARK_GRAY, F_GREEN, F_RED, F_WHITE,
)
from .function import roman


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
            return f'{BOLD}{F_WHITE}Empty{CLN}'

        color = RARITY_COLORS[self.rarity]

        if getattr(self, 'modifer', None) is not None:
            modifier = f'{self.modifier.capitalize()} '
        else:
            modifier = ''

        name = ' '.join(word.capitalize() for word in self.name.split('_'))
        count = f' x {self.count}' if getattr(self, 'count', 1) != 1 else ''

        if getattr(self, 'stars', None) is None:
            stars = ''
        elif self.stars <= 5:
            stars = f' {F_GOLD}' + self.stars * '✪'
        else:
            stars = (f' {F_RED}' + (self.stars - 5) * '✪'
                     + F_GOLD + (10 - self.stars) * '✪')

        return f'{color}{modifier}{name}{stars}{color}{count}{CLN}'

    cls.display = display

    # 0;0;170 for enchantments

    def info(self):
        color = RARITY_COLORS[self.rarity]

        if getattr(self, 'modifer', None) is not None:
            modifier = f'{self.modifier.capitalize()} '
        else:
            modifier = ''

        display_name = ' '.join(word.capitalize()
                                for word in self.name.split('_'))

        if getattr(self, 'stars', None) is None:
            stars = ''
        elif self.stars <= 5:
            stars = f' {F_GOLD}' + self.stars * '✪'
        else:
            stars = (f' {F_RED}' + (self.stars - 5) * '✪'
                     + F_GOLD + (10 - self.stars) * '✪')

        info = f'{color}{modifier}{display_name}{stars}{color}'

        if hasattr(self, 'breaking_power'):
            info += (f'\n{F_DARK_GRAY}Breaking Power: {F_RED}+'
                     f'{self.breaking_power}{CLN}\n')

        if hasattr(self, 'mining_speed'):
            info += (f'\n\n{F_GRAY}'
                     f'Mining Speed: {F_GREEN}+{self.mining_speed}{CLN}\n')

        if hasattr(self, 'damage'):
            info += (f'\n{F_GRAY}Damage: {F_RED}+{self.damage}{CLN}')

        if hasattr(self, 'modifier'):
            info += (f'\n\n{F_DARK_GRAY}'
                     f'This item can be reforged!{CLN}')

        if getattr(self, 'combat_skill_req', None) is not None:
            info += (f'\n{F_DARK_RED}❣ {F_RED}Requires '
                     f'{F_GREEN}Combat Skill {self.combat_skill_req}{CLN}')
        if getattr(self, 'dungeon_skill_req', None) is not None:
            info += (f'\n{F_DARK_RED}❣ {F_RED}Requires '
                     f'{F_GREEN}Catacombs Skill {self.dungeon_skill_req}{CLN}')
        if getattr(self, 'dungeon_completion_req', None) is not None:
            info += (f'\n{F_DARK_RED}❣ {F_RED}Requires {F_GREEN}Catacombs Floor '
                     f'{roman(self.dungeon_completion_req)} Completion{CLN}')

        type_name = self.__class__.__name__.upper()
        if getattr(self, 'stars', None) is not None:
            type_name = f'DUNGEON {type_name}'
        info += f'\n{color}{self.rarity.upper()} {type_name}{CLN}'
        while '\n\n\n' in info:
            info = info.replace('\n\n\n', '\n\n')
        return info

    cls.info = info

    return cls
