from typing import Dict, List, Optional, Tuple

from ..constant.colors import *
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
    description: Tuple[str, Dict[str, Number]]
    values: List[Number] = []


ABILITIES = [
    # misc abilities
    AnonymousAbility(
        id='exp_bottle',
        description=('smash_exp_bottle', {}),
    ),

    # armor abilities
    NamedAbility(
        id='farm_armor_speed',
        name='Full Set Bonus: Bonus Speed',
        description=('increase_region_speed', {'percent': 25, 'place': (
            'farm', 'barn', 'desert',
        )}),
    ),
    NamedAbility(
        id='farm_suit_speed',
        name='Full Set Bonus: Bonus Speed',
        description=('increase_region_speed', {'percent': 20, 'place': (
            'farm', 'barn', 'desert',
        )}),
    ),

    NamedAbility(
        id='pumpkin_buff',
        name='Full Set Bonus: Pumpkin Buff',
        description=('pumpkin_buff', {'reduction': 10, 'increase': 10}),
    ),
    NamedAbility(
        id='deflect',
        name='Full Set Bonus: Deflect',
        description=('damage_rebound', {'percent': 33.3}),
    ),
    NamedAbility(
        id='speester_bonus',
        name='Full Set Bonus: Bonus Speed',
        description=('speed_increase', {'speed': 20}),
    ),

    AnonymousAbility(
        id='lapis_armor_exp_bonus',
        description=('lapis_exp', {'amount': 50}),
    ),
    NamedAbility(
        id='lapis_armor_health',
        name='Full Set Bonus: Health',
        description=('increase_max_hp', {'amount': 60}),
    ),
    NamedAbility(
        id='expert_miner',
        name='Full Set Bonus: Expert Miner',
        description=('expert_miner', {'mining_speed': 2}),
    ),
    AnonymousAbility(
        id='mining_double_defense',
        description=('mining_double_defense', {}),
    ),
    AnonymousAbility(
        id='ender_armor',
        description=('end_double_stat', {}),
    ),
    NamedAbility(
        id='protective_blood',
        name='Full Set Bonus: Protective Blood',
        description=('protective_blood', {'amount': 1}),
    ),
    NamedAbility(
        id='old_blood',
        name='Full Set Bonus: Old Blood',
        description=('old_blood', {'enchants': (
            'growth', 'protection', 'feather_falling',
            'sugar_rush', 'true_protection',
        )}),
    ),
    NamedAbility(
        id='holy_blood',
        name='Full Set Bonus: Holy Blood',
        description=('holy_blood', {'multiplier': 3}),
    ),
    NamedAbility(
        id='young_blood',
        name='Full Set Bonus: Young Blood',
        description=('young_blood',
                     {'amount': 70, 'percent': 70, 'cap': 100}),
    ),
    NamedAbility(
        id='strong_blood',
        name='Full Set Bonus: Strong Blood',
        description=('strong_blood', {'value': 75}),
    ),
    NamedAbility(
        id='superior_blood',
        name='Full Set Bonus: Superior Blood',
        description=('superior_blood', {'percent': 5}),
    ),
    NamedAbility(
        id='fairys_outfit',
        name="Full Set Bonus: Fairy's Outfit",
        description=('speed_increase_perc', {'percent': 10}),
    ),

    # tool abilities
    AnonymousAbility(
        id='jungle_axe',
        description=('jungle_axe_tip', {'time': 2}),
    ),
    AnonymousAbility(
        id='treecapitator',
        description=('treecapitator_tip', {'time': 2}),
    ),

    # weapon abilities
    AnonymousAbility(
        id='raider_coins',
        description=('raider_coins', {'coins': 20}),
    ),
    AnonymousAbility(
        id='tacticians_sword',
        description=('tacticians_sword', {'value': 15}),
    ),
    AnonymousAbility(
        id='pure_emerald',
        description=('pure_emerald', {}),
    ),
    AnonymousAbility(
        id='sword_of_the_stars',
        description=('sword_of_the_stars', {}),
    ),
    AnonymousAbility(
        id='sword_of_the_universe',
        description=('sword_of_the_universe', {}),
    ),

    # pet abilities
    NamedAbility(
        id='omen',
        name='Omen',
        description=('grant_pet_luck', {'amount': 15}),
    ),
    NamedAbility(
        id='supernatural',
        name='Supernatural',
        description=('grant_magic_find', {'amount': 15}),
    ),
    NamedAbility(
        id='hunter',
        name='Hunter',
        description=('hunter', {'value': 100}),
    ),
    NamedAbility(
        id='one_with_the_dragons',
        name='One with the Dragons',
        description=('one_with_the_dragons', {'val1': 50, 'val2': 10}),
    ),
    NamedAbility(
        id='superior',
        name='Superior',
        description=('superior', {'percent': 10}),
    ),
    NamedAbility(
        id='jerry_damage',
        name='Jerry',
        description=('jerry_damage', {'value': 50}),
    ),
    NamedAbility(
        id='common_merciless_swipe',
        name='Merciless Swipe',
        description=('merciless_swipe', {'percent': 15}),
    ),
    NamedAbility(
        id='uncommon_merciless_swipe',
        name='Merciless Swipe',
        description=('merciless_swipe', {'percent': 33}),
    ),
    NamedAbility(
        id='legendary_merciless_swipe',
        name='Merciless Swipe',
        description=('merciless_swipe', {'percent': 50}),
    ),
    NamedAbility(
        id='eternal_coins',
        name='Eternal Coins',
        description=('eternal_coins', {}),
    ),
    NamedAbility(
        id='common_primal_force',
        name='Primal Force',
        description=('primal_force', {'val1': 3, 'val2': 3}),
    ),
    NamedAbility(
        id='uncommon_primal_force',
        name='Primal Force',
        description=('primal_force', {'val1': 5, 'val2': 5}),
    ),
    NamedAbility(
        id='rare_primal_force',
        name='Primal Force',
        description=('primal_force', {'val1': 10, 'val2': 10}),
    ),
    NamedAbility(
        id='epic_primal_force',
        name='Primal Force',
        description=('primal_force', {'val1': 15, 'val2': 15}),
    ),
    NamedAbility(
        id='legendary_primal_force',
        name='Primal Force',
        description=('primal_force', {'val1': 15, 'val2': 15}),
    ),
    NamedAbility(
        id='rare_vine_swing',
        name='Vine Swing',
        description=('gain_region_speed', {'value': 75, 'place': ('park',)}),
    ),
    NamedAbility(
        id='epic_vine_swing',
        name='Vine Swing',
        description=('gain_region_speed', {'value': 100, 'place': ('park',)}),
    ),
    NamedAbility(
        id='evolves_axes',
        name='Evolves Axes',
        description=('evolves_axes', {'percent': 50}),
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
        description=('increase_sea_creature_chance', {'value': 7}),
    ),
    NamedAbility(
        id='epic_echolocation',
        name='Echolocation',
        description=('increase_sea_creature_chance', {'value': 10}),
    ),

    # accessory abilities
    AnonymousAbility(
        id='farming_talisman',
        description=('increase_held_region_speed', {'percent': 10, 'place': (
            'farm', 'barn', 'desert',
        )})
    ),
    AnonymousAbility(
        id='vaccine_talisman',
        description=('poison_immunity', {}),
    ),
    AnonymousAbility(
        id='farmer_orb',
        description=('farmer_orb', {}),
    ),
    AnonymousAbility(
        id='night_vision_charm',
        description=('night_vision_charm', {}),
    ),
    AnonymousAbility(
        id='speed_talisman',
        description=('give_held_speed', {'amount': 1}),
    ),
    AnonymousAbility(
        id='speed_ring',
        description=('give_held_speed', {'amount': 3}),
    ),
    AnonymousAbility(
        id='speed_artifact',
        description=('give_held_speed', {'amount': 5}),
    ),
    AnonymousAbility(
        id='feather_talisman',
        description=('feather_talisman', {}),
    ),
    AnonymousAbility(
        id='feather_ring',
        description=('feather_ring', {}),
    ),
    AnonymousAbility(
        id='feather_artifact',
        description=('feather_artifact', {}),
    ),
    AnonymousAbility(
        id='piggy_bank',
        description=('piggy_bank', {}),
    ),
    AnonymousAbility(
        id='cracked_piggy_bank',
        description=('cracked_piggy_bank', {'percent': 75}),
    ),
    AnonymousAbility(
        id='broken_piggy_bank',
        description=('broken_piggy_bank', {}),
    ),
    AnonymousAbility(
        id='haste_ring',
        description=('grant_mining_speed', {'amount': 50}),
    ),
    AnonymousAbility(
        id='experience_artifact',
        description=('gain_exp', {'percent': 25}),
    ),
    AnonymousAbility(
        id='talisman_of_coins',
        description=('talisman_of_coins', {}),
    ),
    AnonymousAbility(
        id='emerald_ring',
        description=('emerald_ring', {'amount': 1}),
    ),
    AnonymousAbility(
        id='wood_affinity_talisman',
        description=('gain_region_speed', {'value': 100, 'place': (
            'forest', 'graveyard', 'wilderness',
        )}),
    ),
    AnonymousAbility(
        id='healing_talisman',
        description=('increase_healing', {'percent': 5}),
    ),
    AnonymousAbility(
        id='healing_ring',
        description=('increase_healing', {'percent': 10}),
    ),
    AnonymousAbility(
        id='sea_creature_talisman',
        description=('sea_creature_talisman', {'percent': 5}),
    ),
    AnonymousAbility(
        id='sea_creature_ring',
        description=('sea_creature_talisman', {'percent': 10}),
    ),
    AnonymousAbility(
        id='sea_creature_artifact',
        description=('sea_creature_talisman', {'percent': 15}),
    ),
    AnonymousAbility(
        id='titanium_talisman',
        description=('grant_mining_speed', {'amount': 15}),
    ),
    AnonymousAbility(
        id='titanium_ring',
        description=('grant_mining_speed', {'amount': 30}),
    ),
    AnonymousAbility(
        id='titanium_artifact',
        description=('grant_mining_speed', {'amount': 45}),
    ),
    AnonymousAbility(
        id='titanium_relic',
        description=('grant_mining_speed', {'amount': 60}),
    ),
    AnonymousAbility(
        id='skeleton_talisman',
        description=('reduce_damage_taken', {
            'entities': 'skeletons', 'percent': 5,
        }),
    ),
    AnonymousAbility(
        id='wolf_talisman',
        description=('reduce_damage_taken', {
            'entities': 'wolves', 'percent': 5,
        }),
    ),
    AnonymousAbility(
        id='wolf_ring',
        description=('reduce_damage_taken', {
            'entities': 'wolves', 'percent': 10,
        }),
    ),
    AnonymousAbility(
        id='zombie_talisman',
        description=('reduce_damage_taken', {
            'entities': 'zombies', 'percent': 5,
        }),
    ),
    AnonymousAbility(
        id='zombie_ring',
        description=('reduce_damage_taken', {
            'entities': 'zombies', 'percent': 10,
        }),
    ),
    AnonymousAbility(
        id='zombie_artifact',
        description=('reduce_damage_taken', {
            'entities': 'zombies', 'percent': 15,
        }),
    ),
    AnonymousAbility(
        id='village_affinity_talisman',
        description=('increase_held_region_speed', {
            'percent': 10, 'place': ('village',),
        }),
    ),
    AnonymousAbility(
        id='mine_affinity_talisman',
        description=('increase_held_region_speed', {
            'percent': 10, 'place': ('gold', 'deep', 'mines'),
        }),
    ),
    AnonymousAbility(
        id='intimidation_talisman',
        description=('intimidation', {'value': 1}),
    ),
    AnonymousAbility(
        id='intimidation_ring',
        description=('intimidation', {'value': 5}),
    ),
    AnonymousAbility(
        id='intimidation_artifact',
        description=('intimidation', {'value': 25}),
    ),
    AnonymousAbility(
        id='scavenger_talisman',
        description=('scavenger_talisman', {}),
    ),
]


def get_ability(id: str, /, *, warn=True) -> Optional[Ability]:
    for item in ABILITIES:
        if item.id == id:
            return get(ABILITIES, id=id)

    if warn:
        red(f'Ability not found: {id!r}')
