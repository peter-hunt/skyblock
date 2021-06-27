from typing import Optional

from ..constant.color import (
    GOLD, GRAY, DARK_GRAY, BLUE, GREEN, AQUA, RED, YELLOW, STAT_COLORS)
from ..function.io import red
from ..function.util import get

from .other_wrapper import init_type


__all__ = ['Ability', 'AnonymousAbility', 'NamedAbility',
           'ABILITIES', 'get_ability']


class Ability:
    pass


@init_type
class AnonymousAbility(Ability):
    id: str
    description: str


@init_type
class NamedAbility(Ability):
    id: str
    name: str
    description: str


ABILITIES = [
    AnonymousAbility(
        id='exp_bottle',
        description=f'Smash it open to recieve\nexperience!'),

    NamedAbility(
        id='farm_armor_speed',
        name='Full Set Bonus: Bonus Speed',
        description=(
            f"Increases your {STAT_COLORS['speed']} Speed{GRAY} by\n"
            f'{GREEN}+25{GRAY} in the {AQUA}Farm{GRAY},\n'
            f'{AQUA}The Barn{GRAY}, and {YELLOW}Mushroom\n'
            f'Desert{GRAY}.')),
    NamedAbility(
        id='farm_suit_speed',
        name='Full Set Bonus: Bonus Speed',
        description=(
            f"Increases your {STAT_COLORS['speed']} Speed{GRAY} by\n"
            f'{GREEN}+20{GRAY} near farming islands\n')),

    NamedAbility(
        id='pumpkin_buff',
        name='Full Set Bonus: Pumpkin Buff',
        description=(
            f'Reduce all taken damage by\n'
            f'{GREEN}+10%{GRAY} and deal {GREEN}+10%{GRAY}\n'
            f'damage.')),
    NamedAbility(
        id='deflect',
        name='Full Set Bonus: Deflect',
        description=(
            f'Rebound {GREEN}+33.0%{GRAY} of the damage\n'
            f'you take back at your enemy.')),
    NamedAbility(
        id='speester_bonus',
        name='Full Set Bonus: Bonus Speed',
        description=(
            f"Increases {STAT_COLORS['speed']} Speed{GRAY} by\n"
            f'{GREEN}+20{GRAY}.')),

    NamedAbility(
        id='miners_outfit_haste',
        name='Full Set Bonus: Haste',
        description=(
            f'Grants {GREEN}+40{GRAY}'
            f" {STAT_COLORS['mining_speed']}Mining Speed\nwhile worn.")),
    AnonymousAbility(
        id='lapis_armor_exp_bonus',
        description=(
            f'Each piece of this armour grants'
            f'{GREEN}50%{GRAY} bonus experience when mining ores.')),
    NamedAbility(
        id='lapis_armor_health',
        name='Full Set Bonus: Health',
        description=(
            f"Increases the wearer's maximum\n"
            f"{STAT_COLORS['health']} Health{GRAY} by {GREEN}60{GRAY}.")),
    NamedAbility(
        id='glacite_expert_miner',
        name='Full Set Bonus: Expert Miner',
        description=(
            f"Grants {GOLD}+2{STAT_COLORS['mining_speed']}"
            f' Mining Speed{GRAY} for\neach of your mining levels.')),
    AnonymousAbility(
        id='glacite_double_defense',
        description=(
            'The Defense of this item is\n'
            'doubled while on a mining island.')),

    AnonymousAbility(
        id='ender_armor',
        description=('All stats of this armor\n'
                     'piece are doubled while on the End\nIsland!')),
    NamedAbility(
        id='protective_blood',
        name='Full Set Bonus: Protective Blood',
        description=(
            f'Increases the defense of each\n'
            f"armor piece by 1% {STAT_COLORS['defense']}\n"
            f'Defense {GRAY} for each missing\n'
            f'percent of HP.')),
    NamedAbility(
        id='old_blood',
        name='Full Set Bonus: Old Blood',
        description=(
            f'Increases the strength of\n'
            f'{BLUE}Growth{GRAY}, {BLUE}Protection{GRAY},\n'
            f'{BLUE}Feather Falling{GRAY}, {BLUE}Sugar\n'
            f'Rush{GRAY}, and {BLUE}True Protection{GRAY}\n'
            f'while worn.')),
    NamedAbility(
        id='holy_blood',
        name='Full Set Bonus: Holy Blood',
        description=(
            f'Increases the natural health\n'
            f'regeneration of you by {GREEN}3x{GRAY}.\n')),
    NamedAbility(
        id='young_blood',
        name='Full Set Bonus: Young Blood',
        description=(
            f'Gain {GREEN}+70{GRAY} Walk Speed while\n'
            f'you are above {GREEN}50%{GRAY} HP.\n')),
    NamedAbility(
        id='strong_blood',
        name='Full Set Bonus: Strong Blood',
        description=(f'Improves the {BLUE}Aspect of the End{GRAY}:\n'
                     f'> {RED}+75 Base Damage{GRAY}')),
    NamedAbility(
        id='superior_blood',
        name='Full Set Bonus: Superior Blood',
        description=f'Most of your stats are increased by {GREEN}5%{GRAY}'),

    NamedAbility(
        id='fairys_outfit',
        name="Full Set Bonus: Fairy's Outfit",
        description=(
            f"Increases {STAT_COLORS['speed']} Speed{GRAY} by\n"
            f'{GREEN}+10%{GRAY}.')),

    AnonymousAbility(
        id='jungle_axe',
        description=(f'A powerful Wooden Axe which can\n'
                     f'break multiple logs in a single\nhit!\n'
                     f'{DARK_GRAY}Cooldown: {GREEN}2s{GRAY}')),
    AnonymousAbility(
        id='treecapitator',
        description=(f'A forceful Gold Axe which can\n'
                     f'break a large amount of logs in\na single hit!\n'
                     f'{DARK_GRAY}Cooldown: {GREEN}2s{GRAY}')),
]


def get_ability(id: str, /) -> Optional[Ability]:
    for item in ABILITIES:
        if item.id == id:
            break
    else:
        red(f'Invalid ability: {id!r}')
        return
    return get(ABILITIES, id=id)
