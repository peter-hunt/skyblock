from typing import Optional

from ..constant.color import *
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
        description=f'Smash it open to recieve\nexperience!',
    ),

    NamedAbility(
        id='farm_armor_speed',
        name='Full Set Bonus: Bonus Speed',
        description=(
            f"Increases your {STAT_COLORS['speed']} Speed{GRAY} by"
            f" {GREEN}+25{GRAY} in the {AQUA}Farm{GRAY}, {AQUA}The Barn{GRAY},"
            f" and {YELLOW}Mushroom Desert{GRAY}."
        ),
    ),
    NamedAbility(
        id='farm_suit_speed',
        name='Full Set Bonus: Bonus Speed',
        description=(
            f"Increases your {STAT_COLORS['speed']} Speed{GRAY} by"
            f" {GREEN}+20{GRAY} near farming islands."
        ),
    ),

    NamedAbility(
        id='pumpkin_buff',
        name='Full Set Bonus: Pumpkin Buff',
        description=(
            f'Reduce all taken damage by {GREEN}+10%{GRAY}'
            f' and deal {GREEN}+10%{GRAY} damage.'
        ),
    ),
    NamedAbility(
        id='deflect',
        name='Full Set Bonus: Deflect',
        description=(
            f'Rebound {GREEN}+33.0%{GRAY} of the damage'
            f' you take back at your enemy.'
        ),
    ),
    NamedAbility(
        id='speester_bonus',
        name='Full Set Bonus: Bonus Speed',
        description=(
            f"Increases {STAT_COLORS['speed']} Speed{GRAY}"
            f' by {GREEN}+20{GRAY}.'
        ),
    ),

    NamedAbility(
        id='miners_outfit_haste',
        name='Full Set Bonus: Haste',
        description=(
            f"Grants {GREEN}+40{GRAY}"
            f" {STAT_COLORS['mining_speed']}Mining Speed while worn."
        ),
    ),
    AnonymousAbility(
        id='lapis_armor_exp_bonus',
        description=(
            f'Each piece of this armour grants'
            f'{GREEN}50%{GRAY} bonus experience when mining ores.'
        ),
    ),
    NamedAbility(
        id='lapis_armor_health',
        name='Full Set Bonus: Health',
        description=(
            f"Increases the wearer's maximum"
            f" {STAT_COLORS['health']} Health{GRAY} by {GREEN}60{GRAY}."
        ),
    ),
    NamedAbility(
        id='glacite_expert_miner',
        name='Full Set Bonus: Expert Miner',
        description=(
            f"Grants {GOLD}+2{STAT_COLORS['mining_speed']}"
            f' Mining Speed{GRAY} for each of your mining levels.'
        ),
    ),
    AnonymousAbility(
        id='glacite_double_defense',
        description=(
            'The Defense of this item is doubled while on a mining island.'
        ),
    ),

    AnonymousAbility(
        id='ender_armor',
        description=('All stats of this armor piece are doubled'
                     ' while on the End Island!'),
    ),
    NamedAbility(
        id='protective_blood',
        name='Full Set Bonus: Protective Blood',
        description=(
            f"Increases the defense of each armor piece"
            f" by 1% {STAT_COLORS['defense']} Defense{GRAY}"
            f" for each missing percent of HP.",
        ),
    ),
    NamedAbility(
        id='old_blood',
        name='Full Set Bonus: Old Blood',
        description=(
            f'Increases the strength of {BLUE}Growth{GRAY}, '
            f'{BLUE}Protection{GRAY}, {BLUE}Feather Falling{GRAY}, '
            f'{BLUE}Sugar Rush{GRAY}, and {BLUE}True Protection{GRAY}'
            f' while worn.'
        ),
    ),
    NamedAbility(
        id='holy_blood',
        name='Full Set Bonus: Holy Blood',
        description=(
            f'Increases the natural health regeneration'
            f' of you by {GREEN}3x{GRAY}.'
        ),
    ),
    NamedAbility(
        id='young_blood',
        name='Full Set Bonus: Young Blood',
        description=(
            f'Gain {GREEN}+70{GRAY} Walk Speed while'
            f' you are above {GREEN}50%{GRAY} HP.'
        ),
    ),
    NamedAbility(
        id='strong_blood',
        name='Full Set Bonus: Strong Blood',
        description=(f'Improves the {BLUE}Aspect of the End{GRAY}:\n'
                     f'> {RED}+75 Base Damage{GRAY}'),
    ),
    NamedAbility(
        id='superior_blood',
        name='Full Set Bonus: Superior Blood',
        description=f'Most of your stats are increased by {GREEN}5%{GRAY}',
    ),

    NamedAbility(
        id='fairys_outfit',
        name="Full Set Bonus: Fairy's Outfit",
        description=(f"Increases {STAT_COLORS['speed']} Speed{GRAY}"
                     f' by {GREEN}+10%{GRAY}.'),
    ),

    AnonymousAbility(
        id='jungle_axe',
        description=(f'A powerful Wooden Axe which can'
                     f' break multiple logs in a single hit!\n'
                     f'{DARK_GRAY}Cooldown: {GREEN}2s{GRAY}'),
    ),
    AnonymousAbility(
        id='treecapitator',
        description=(f'A forceful Gold Axe which can'
                     f' break a large amount of logs in a single hit!\n'
                     f'{DARK_GRAY}Cooldown: {GREEN}2s{GRAY}'),
    ),

    AnonymousAbility(
        id='tacticians_sword',
        description=(f'Gains {RED}+15 Damage{GRAY} for each Combat collection'
                     f' of Tier VII and over of its wielder.'),
    ),
    AnonymousAbility(
        id='pure_emerald',
        description=(f'A powerful blade made from pure {GREEN}Emeralds{GRAY}.'
                     f' This blade becomes stronger as you carry more'
                     f' {GOLD}coins{GRAY} in your purse.'),
    ),
    AnonymousAbility(
        id='sword_of_the_stars',
        description=(f'{LIGHT_PURPLE}"Only those with the power to'
                     f' create this world can wield this blade.'),
    ),
    AnonymousAbility(
        id='sword_of_the_universe',
        description=(f"{YELLOW}Oi you! Yes you. What are you looking at?"
                     f" Yes this sword has ∞ damage. Kinda overkill? I'm lazy"
                     f" ok. {RED}(╯°□°)╯{GRAY}︵ ┻━┻"),
    ),

    NamedAbility(
        id='eternal_coins',
        name='Eternal Coins',
        description=f"Don't lose {GOLD}coins{GRAY} from death.",
    ),
]


def get_ability(id: str, /) -> Optional[Ability]:
    for item in ABILITIES:
        if item.id == id:
            break
    else:
        red(f'Ability not found: {id!r}')
        return
    return get(ABILITIES, id=id)
