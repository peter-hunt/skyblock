from typing import List, Optional

from ..constant.color import *
from ..constant.util import Number
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
    values: List[Number] = []


ABILITIES = [
    # misc abilities
    AnonymousAbility(
        id='exp_bottle',
        description=f'Smash it open to recieve\nexperience!',
    ),

    # armor abilities
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
            f' {GREEN}50%{GRAY} bonus experience when mining ores.'
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
        description=(
            'All stats of this armor piece are doubled while on the End Island!'
        ),
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

    # tool abilities
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

    # weapon abilities
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

    # pet abilities
    NamedAbility(
        id='one_with_the_dragons',
        name='One with the Dragons',
        description=(f"Buffs the Aspect of the Dragons sword by"
                     f" {GREEN}%d {STAT_COLORS['strength']} Damage {GRAY}and"
                     f" {GREEN}%d {STAT_COLORS['strength']} Strength{GRAY}."),
        values=[50, 10],
    ),
    NamedAbility(
        id='superior',
        name='Superior',
        description=f'Increases all stats by {GREEN}%d%%{GRAY}.',
        values=[10],
    ),
    NamedAbility(
        id='jerry_damage',
        name='Jerry',
        description=(f'Actually adds {RED}%d {GRAY}damage'
                     f' to the Aspect of the Jerry.'),
        values=[50],
    ),
    NamedAbility(
        id='common_merciless_swipe',
        name='Merciless Swipe',
        description=(f"Gain {RED}+%d%% {STAT_COLORS['ferocity']}"
                     f" Ferocity{GRAY}."),
        values=[15],
    ),
    NamedAbility(
        id='uncommon_merciless_swipe',
        name='Merciless Swipe',
        description=(f"Gain {RED}+%d%% {STAT_COLORS['ferocity']}"
                     f" Ferocity{GRAY}."),
        values=[33],
    ),
    NamedAbility(
        id='legendary_merciless_swipe',
        name='Merciless Swipe',
        description=(f"Gain {RED}+%d%% {STAT_COLORS['ferocity']}"
                     f" Ferocity{GRAY}."),
        values=[50],
    ),
    NamedAbility(
        id='eternal_coins',
        name='Eternal Coins',
        description=f"Don't lose {GOLD}coins{GRAY} from death.",
    ),
    NamedAbility(
        id='common_primal_force',
        name='Primal Force',
        description=(f"Adds +{RED}%d {STAT_COLORS['strength']} Damage {GRAY}and"
                     f" +{RED}%d {STAT_COLORS['strength']} Strength{GRAY}"
                     f" to your weapons."),
        values=[3, 3],
    ),
    NamedAbility(
        id='uncommon_primal_force',
        name='Primal Force',
        description=(f"Adds +{RED}%d {STAT_COLORS['strength']} Damage {GRAY}and"
                     f" +{RED}%d {STAT_COLORS['strength']} Strength{GRAY}"
                     f" to your weapons."),
        values=[5, 5],
    ),
    NamedAbility(
        id='rare_primal_force',
        name='Primal Force',
        description=(f"Adds +{RED}%d {STAT_COLORS['strength']} Damage {GRAY}and"
                     f" +{RED}%d {STAT_COLORS['strength']} Strength{GRAY}"
                     f" to your weapons."),
        values=[10, 10],
    ),
    NamedAbility(
        id='epic_primal_force',
        name='Primal Force',
        description=(f"Adds +{RED}%d {STAT_COLORS['strength']} Damage {GRAY}and"
                     f" +{RED}%d {STAT_COLORS['strength']} Strength{GRAY}"
                     f" to your weapons."),
        values=[15, 15],
    ),
    NamedAbility(
        id='legendary_primal_force',
        name='Primal Force',
        description=(f"Adds +{RED}%d {STAT_COLORS['strength']} Damage {GRAY}and"
                     f" +{RED}%d {STAT_COLORS['strength']} Strength{GRAY}"
                     f" to your weapons."),
        values=[15, 15],
    ),
    NamedAbility(
        id='rare_vine_swing',
        name='Vine Swing',
        description=(f"Gain +{GREEN}%d {STAT_COLORS['speed']} Speed"
                     f" {GRAY}while in The Park."),
        values=[75],
    ),
    NamedAbility(
        id='epic_vine_swing',
        name='Vine Swing',
        description=(f"Gain +{GREEN}%d {STAT_COLORS['speed']} Speed"
                     f" {GRAY}while in The Park."),
        values=[100],
    ),
    NamedAbility(
        id='evolves_axes',
        name='Evolves Axes',
        description=(f'Reduces the cooldown of Jungle Axe and Treecapitator'
                     f' by {GREEN}%d%%{GRAY}.'),
        values=[50],
    ),
    NamedAbility(
        id='archimedes',
        name='Archimedes',
        description=(f"Gain {RED}+%d%% Max {STAT_COLORS['health']}"
                     f"  Health{GRAY}."),
        values=[20],
    ),
    NamedAbility(
        id='rare_echolocation',
        name='Echolocation',
        description=(f'Increases sea creatures catch chance'
                     f' by {GREEN}%d%%{GRAY}.'),
        values=[7],
    ),
    NamedAbility(
        id='epic_echolocation',
        name='Echolocation',
        description=(f'Increases sea creatures catch chance'
                     f' by {GREEN}%d%%{GRAY}.'),
        values=[10],
    ),

    # accessory abilities
    AnonymousAbility(
        id='farming_talisman',
        description=(f"Increases your {STAT_COLORS['speed']} Speed {GRAY}by"
                     f" {GREEN}+10% {GRAY}while held in the {AQUA}Farm{GRAY},"
                     f" {AQUA}The Barn{GRAY},"
                     f" and {AQUA}Mushroom Desert{GRAY}."),
    ),
    AnonymousAbility(
        id='vaccine_talisman',
        description=(f'Provides immunity to {BLUE}Poison'
                     f' {GRAY}damage when held.'),
    ),
    AnonymousAbility(
        id='farmer_orb',
        description=(f'Increases the regrowth rate of nearby crops'
                     f' on the public islands, regrowing an extra crop'
                     f' every {GREEN}3 {GRAY}seconds.'),
    ),
    AnonymousAbility(
        id='night_vision_charm',
        description=('Grants better vision while this item'
                     ' is in your inventory.'),
    ),
    AnonymousAbility(
        id='speed_talisman',
        description=(f"Gives {GREEN}+1 {STAT_COLORS['speed']} Speed"
                     f" {GRAY}when held."),
    ),
    AnonymousAbility(
        id='speed_ring',
        description=(f"Gives {GREEN}+3 {STAT_COLORS['speed']} Speed"
                     f" {GRAY}when held."),
    ),
    AnonymousAbility(
        id='speed_artifact',
        description=(f"Gives {GREEN}+5 {STAT_COLORS['speed']} Speed"
                     f" {GRAY}when held."),
    ),
    AnonymousAbility(
        id='feather_talisman',
        description=f'Reduce little fall damage.',
    ),
    AnonymousAbility(
        id='feather_ring',
        description=f'Reduce fall damage.',
    ),
    AnonymousAbility(
        id='feather_artifact',
        description='Reduce more fall damage.',
    ),
    AnonymousAbility(
        id='piggy_bank',
        description=(f'Saves your coins from death.'
                     f' Only when in player inventory. {RED}Fragile!'),
    ),
    AnonymousAbility(
        id='cracked_piggy_bank',
        description=(f'Saves {RED}75% {GRAY}of your coins from death.'
                     f' Only when in player inventory.'
                     f' {RED}Very fragile!'),
    ),
    AnonymousAbility(
        id='broken_piggy_bank',
        description='It broke!',
    ),
    AnonymousAbility(
        id='haste_ring',
        description=(f"Grants {GREEN}+50 {STAT_COLORS['mining_speed']}"
                     f" Mining Speed{GRAY}."),
    ),
    AnonymousAbility(
        id='experience_artifact',
        description=(f'Increase experience orbs you gain by {GREEN}25% '
                     f'{GRAY}while this item is in your inventory.'),
    ),
    AnonymousAbility(
        id='talisman_of_coins',
        description=('Coins start appearing around you'
                     ' on public islands. Lucky!'),
    ),
    AnonymousAbility(
        id='emerald_ring',
        description=f'Get {GOLD}+1 coin {GRAY}every minute.',
    ),
    AnonymousAbility(
        id='wood_affinity_talisman',
        description=(f"Increases your {STAT_COLORS['speed']} Speed {GRAY}by"
                     f" {GREEN}+10% {GRAY}in {AQUA}Forest{GRAY},"
                     f" {AQUA}Graveyard{GRAY}, {AQUA}Wilderness{GRAY}."),
    ),
    AnonymousAbility(
        id='healing_talisman',
        description=f'Increases healing by {GREEN}5%{GRAY}.',
    ),
    AnonymousAbility(
        id='healing_ring',
        description=f'Increases healing by {GREEN}10%{GRAY}.',
    ),
    AnonymousAbility(
        id='sea_creature_talisman',
        description=f'Take {GREEN}5% {GRAY}less damage from Sea Creatures.',
    ),
    AnonymousAbility(
        id='sea_creature_ring',
        description=f'Take {GREEN}10% {GRAY}less damage from Sea Creatures.',
    ),
    AnonymousAbility(
        id='sea_creature_artifact',
        description=f'Take {GREEN}15% {GRAY}less damage from Sea Creatures.',
    ),
    AnonymousAbility(
        id='titanium_talisman',
        description=(f"Grants {GREEN}+15 {STAT_COLORS['mining_speed']}"
                     f" Mining Speed{GRAY}."),
    ),
    AnonymousAbility(
        id='titanium_ring',
        description=(f"Grants {GREEN}+30 {STAT_COLORS['mining_speed']}"
                     f" Mining Speed{GRAY}."),
    ),
    AnonymousAbility(
        id='titanium_artifact',
        description=(f"Grants {GREEN}+45 {STAT_COLORS['mining_speed']}"
                     f" Mining Speed{GRAY}."),
    ),
    AnonymousAbility(
        id='titanium_relic',
        description=(f"Grants {GREEN}+60 {STAT_COLORS['mining_speed']}"
                     f" Mining Speed{GRAY}."),
    ),
    AnonymousAbility(
        id='zombie_talisman',
        description=(f'Reduce the damage taken from zombies'
                     f' by {GREEN}5%{GRAY}.'),
    ),
    AnonymousAbility(
        id='skeleton_talisman',
        description=(f'Reduce the damage taken from skeletons'
                     f' by {GREEN}5%{GRAY}.'),
    ),
    AnonymousAbility(
        id='village_affinity_talisman',
        description=(f"Increases your {STAT_COLORS['speed']} Speed {GRAY}by"
                     f" {GREEN}+10% {GRAY}while held"
                     f" in the {AQUA}Village{GRAY}."),
    ),
    AnonymousAbility(
        id='mine_affinity_talisman',
        description=(f"Increases your {STAT_COLORS['speed']} Speed {GRAY}by"
                     f" {GREEN}+10% {GRAY}while held"
                     f" in any {AQUA}Mines{GRAY}."),
    ),
    AnonymousAbility(
        id='intimidation_talisman',
        description=f'Level {GREEN}1 {GRAY}monsters will no longer target you.',
    ),
    AnonymousAbility(
        id='scavenger_talisman',
        description='Monsters drop coins will killed.',
    ),
]


def get_ability(id: str, /, *, warn=True) -> Optional[Ability]:
    for item in ABILITIES:
        if item.id == id:
            break
    else:
        if warn:
            red(f'Ability not found: {id!r}')
        return
    return get(ABILITIES, id=id)
