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
    display_id: int
    variables: dict[str, Number] = {}


@init_type
class NamedAbility(Ability):
    id: str
    name: str
    display_id: int
    variables: dict[str, Number] = {}
    values: list[Number] = []


@init_type
class TieredBonus(Ability):
    id: str
    name: str
    display_id: int
    tiered_variables: dict[str, list[Number]] = {}


ABILITIES = [
    # misc abilities
    AnonymousAbility(
        id='exp_bottle',
        display_id='smash_exp_bottle',
    ),
    AnonymousAbility(
        id='undead_catalyst',
        display_id='undead_catalyst',
    ),
    AnonymousAbility(
        id='revenant_catalyst',
        display_id='revenant_catalyst',
    ),
    AnonymousAbility(
        id='shard_of_the_shredded',
        display_id='shard_of_the_shredded',
    ),
    AnonymousAbility(
        id='warden_heart',
        display_id='warden_heart',
    ),
    AnonymousAbility(
        id='red_claw_egg',
        display_id='red_claw_egg',
    ),
    AnonymousAbility(
        id='ender_artifact_upgrader',
        display_id='ender_artifact_upgrader',
    ),

    # armor abilities
    NamedAbility(
        id='death_tax',
        name='Full Set Bonus: Death Tax',
        display_id='death_tax',
    ),
    NamedAbility(
        id='farm_armor_speed',
        name='Full Set Bonus: Bonus Speed',
        display_id='increase_region_speed',
        variables={'percent': 25, 'place': ('farm', 'barn', 'desert')},
    ),
    NamedAbility(
        id='farm_suit_speed',
        name='Full Set Bonus: Bonus Speed',
        display_id='increase_region_speed',
        variables={'percent': 20, 'place': ('farm', 'barn', 'desert')},
    ),

    NamedAbility(
        id='pumpkin_buff',
        name='Full Set Bonus: Pumpkin Buff',
        display_id='pumpkin_buff',
        variables={'reduction': 10, 'increase': 10},
    ),
    NamedAbility(
        id='deflect',
        name='Full Set Bonus: Deflect',
        display_id='damage_rebound',
        variables={'percent': 33.3},
    ),
    NamedAbility(
        id='speester_bonus',
        name='Full Set Bonus: Bonus Speed',
        display_id='speed_increase',
        variables={'speed': 20},
    ),

    AnonymousAbility(
        id='lapis_armor_exp_bonus',
        display_id='lapis_exp',
        variables={'amount': 50},
    ),
    NamedAbility(
        id='lapis_armor_health',
        name='Full Set Bonus: Health',
        display_id='increase_max_hp',
        variables={'amount': 60},
    ),
    NamedAbility(
        id='expert_miner',
        name='Full Set Bonus: Expert Miner',
        display_id='expert_miner',
        variables={'mining_speed': 2},
    ),
    AnonymousAbility(
        id='mining_double_defense',
        display_id='mining_double_defense',
    ),
    NamedAbility(
        id='mithrils_protection',
        name="Mithril's Protection",
        display_id='mithrils_protection',
    ),
    AnonymousAbility(
        id='ender_armor',
        display_id='end_double_stat',
    ),
    NamedAbility(
        id='protective_blood',
        name='Full Set Bonus: Protective Blood',
        display_id='protective_blood',
        variables={'amount': 1},
    ),
    NamedAbility(
        id='old_blood',
        name='Full Set Bonus: Old Blood',
        display_id='old_blood',
        variables={'enchants': (
            'growth', 'protection', 'feather_falling',
            'sugar_rush', 'true_protection',
        )},
    ),
    NamedAbility(
        id='holy_blood',
        name='Full Set Bonus: Holy Blood',
        display_id='holy_blood',
        variables={'multiplier': 3},
    ),
    NamedAbility(
        id='young_blood',
        name='Full Set Bonus: Young Blood',
        display_id='young_blood',
        variables={'amount': 70, 'percent': 70, 'cap': 100},
    ),
    NamedAbility(
        id='strong_blood',
        name='Full Set Bonus: Strong Blood',
        display_id='strong_blood',
        variables={'value': 75},
    ),
    NamedAbility(
        id='superior_blood',
        name='Full Set Bonus: Superior Blood',
        display_id='superior_blood',
        variables={'percent': 5},
    ),
    NamedAbility(
        id='fairys_outfit',
        name="Full Set Bonus: Fairy's Outfit",
        display_id='speed_increase_perc',
        variables={'percent': 10},
    ),

    NamedAbility(
        id='healing_boost',
        name="Ability: Healing Boost",
        display_id='healing_boost',
    ),
    NamedAbility(
        id='disgusting_healing',
        name="Ability: Disgusting Healing",
        display_id='disgusting_healing',
    ),
    NamedAbility(
        id='brute_force',
        name="Ability: Brute Force",
        display_id='brute_force',
    ),

    # tool abilities
    AnonymousAbility(
        id='jungle_axe',
        display_id='jungle_axe_tip',
        variables={'time': 2},
    ),
    AnonymousAbility(
        id='treecapitator',
        display_id='treecapitator_tip',
        variables={'time': 2},
    ),

    # weapon abilities
    AnonymousAbility(
        id='raider_axe',
        display_id='raider_axe',
    ),
    AnonymousAbility(
        id='tacticians_sword',
        display_id='tacticians_sword',
        variables={'value': 15},
    ),
    AnonymousAbility(
        id='pure_emerald',
        display_id='pure_emerald',
    ),

    AnonymousAbility(
        id='undead_sword',
        display_id='damage_undead',
        variables={'value': 100},
    ),
    AnonymousAbility(
        id='spider_sword',
        display_id='damage_spider',
        variables={'value': 100},
    ),
    AnonymousAbility(
        id='end_sword',
        display_id='damage_end',
        variables={'value': 100},
    ),
    AnonymousAbility(
        id='revenant_falchion',
        display_id='damage_zombie',
        variables={'value': 150},
    ),
    AnonymousAbility(
        id='reaper_falchion',
        display_id='reaper_falchion',
    ),
    AnonymousAbility(
        id='axe_of_the_shredded',
        display_id='axe_of_the_shredded',
    ),
    AnonymousAbility(
        id='scorpion_foil',
        display_id='damage_spider',
        variables={'value': 150},
    ),
    AnonymousAbility(
        id='shaman_sword',
        display_id='shaman_sword',
    ),
    AnonymousAbility(
        id='pooch_sword',
        display_id='pooch_sword',
    ),
    AnonymousAbility(
        id='voidwalker_katana',
        display_id='voidwalker_katana',
    ),
    AnonymousAbility(
        id='voidedge_katana',
        display_id='voidedge_katana',
    ),
    AnonymousAbility(
        id='vorpal_katana',
        display_id='vorpal_katana',
    ),
    AnonymousAbility(
        id='atomsplit_katana',
        display_id='atomsplit_katana',
    ),

    AnonymousAbility(
        id='sword_of_the_stars',
        display_id='sword_of_the_stars',
    ),
    AnonymousAbility(
        id='sword_of_the_universe',
        display_id='sword_of_the_universe',
    ),

    # pet abilities
    NamedAbility(
        id='omen',
        name='Omen',
        display_id='grant_pet_luck',
        variables={'amount': 15},
    ),
    NamedAbility(
        id='supernatural',
        name='Supernatural',
        display_id='grant_magic_find',
        variables={'amount': 15},
    ),
    NamedAbility(
        id='hunter',
        name='Hunter',
        display_id='hunter',
        variables={'value': 100},
    ),
    NamedAbility(
        id='one_with_the_dragons',
        name='One with the Dragons',
        display_id='one_with_the_dragons',
        variables={'val1': 50, 'val2': 10},
    ),
    NamedAbility(
        id='superior',
        name='Superior',
        display_id='superior',
        variables={'percent': 10},
    ),
    NamedAbility(
        id='jerry_damage',
        name='Jerry',
        display_id='jerry_damage',
        variables={'value': 50},
    ),
    NamedAbility(
        id='common_merciless_swipe',
        name='Merciless Swipe',
        display_id='merciless_swipe',
        variables={'percent': 15},
    ),
    NamedAbility(
        id='uncommon_merciless_swipe',
        name='Merciless Swipe',
        display_id='merciless_swipe',
        variables={'percent': 33},
    ),
    NamedAbility(
        id='legendary_merciless_swipe',
        name='Merciless Swipe',
        display_id='merciless_swipe',
        variables={'percent': 50},
    ),
    NamedAbility(
        id='eternal_coins',
        name='Eternal Coins',
        display_id='eternal_coins',
    ),
    NamedAbility(
        id='common_primal_force',
        name='Primal Force',
        display_id='primal_force',
        variables={'val1': 3, 'val2': 3},
    ),
    NamedAbility(
        id='uncommon_primal_force',
        name='Primal Force',
        display_id='primal_force',
        variables={'val1': 5, 'val2': 5},
    ),
    NamedAbility(
        id='rare_primal_force',
        name='Primal Force',
        display_id='primal_force',
        variables={'val1': 10, 'val2': 10},
    ),
    NamedAbility(
        id='epic_primal_force',
        name='Primal Force',
        display_id='primal_force',
        variables={'val1': 15, 'val2': 15},
    ),
    NamedAbility(
        id='legendary_primal_force',
        name='Primal Force',
        display_id='primal_force',
        variables={'val1': 20, 'val2': 20},
    ),
    NamedAbility(
        id='rare_vine_swing',
        name='Vine Swing',
        display_id='gain_region_speed',
        variables={'value': 75, 'place': ('park',)},
    ),
    NamedAbility(
        id='epic_vine_swing',
        name='Vine Swing',
        display_id='gain_region_speed',
        variables={'value': 100, 'place': ('park',)},
    ),
    NamedAbility(
        id='evolves_axes',
        name='Evolves Axes',
        display_id='evolves_axes',
        variables={'percent': 50},
    ),
    NamedAbility(
        id='archimedes',
        name='Archimedes',
        display_id='increase_max_hp',
        variables={'amount': 20},
    ),
    NamedAbility(
        id='rare_echolocation',
        name='Echolocation',
        display_id='increase_sea_creature_chance',
        variables={'value': 7},
    ),
    NamedAbility(
        id='epic_echolocation',
        name='Echolocation',
        display_id='increase_sea_creature_chance',
        variables={'value': 10},
    ),
    NamedAbility(
        id='epic_flamvoyant',
        name='Flamvoyant',
        display_id='flamvoyant',
        variables={'level': 15},
    ),
    NamedAbility(
        id='legendary_flamvoyant',
        name='Flamvoyant',
        display_id='flamvoyant',
        variables={'level': 20},
    ),
    NamedAbility(
        id='turtle_tactics',
        name='Turtle Tactics',
        display_id='turtle_tactics',
        variables={'perc': 20},
    ),
    NamedAbility(
        id='rare_grounded',
        name='Grounded',
        display_id='grounded',
        variables={'value': 100},
    ),
    NamedAbility(
        id='rare_burrowing',
        name='Burrowing',
        display_id='burrowing',
        variables={'value': 2.5},
    ),
    NamedAbility(
        id='epic_grounded',
        name='Grounded',
        display_id='grounded',
        variables={'value': 150},
    ),
    NamedAbility(
        id='epic_burrowing',
        name='Burrowing',
        display_id='burrowing',
        variables={'value': 3},
    ),
    NamedAbility(
        id='wormhole',
        name='Wormhole',
        display_id='wormhole',
        variables={'value': 100},
    ),

    NamedAbility(
        id='greed_0',
        name='Greed',
        display_id='greed',
        variables={'coins': '100,000', 'bonus': 0},
    ),
    NamedAbility(
        id='greed_20',
        name='Greed',
        display_id='greed',
        variables={'coins': '1,000,000', 'bonus': 20},
    ),
    NamedAbility(
        id='greed_40',
        name='Greed',
        display_id='greed',
        variables={'coins': '3,500,000', 'bonus': 40},
    ),
    NamedAbility(
        id='greed_60',
        name='Greed',
        display_id='greed',
        variables={'coins': '7,500,000', 'bonus': 60},
    ),
    NamedAbility(
        id='greed_80',
        name='Greed',
        display_id='greed',
        variables={'coins': '17,500,000', 'bonus': 80},
    ),
    NamedAbility(
        id='greed_100',
        name='Greed',
        display_id='greed',
        variables={'coins': '30,000,000', 'bonus': 100},
    ),
    NamedAbility(
        id='greed_120',
        name='Greed',
        display_id='greed',
        variables={'coins': '50,000,000', 'bonus': 120},
    ),

    NamedAbility(
        id='healing_boost',
        name='Healing Boost',
        display_id='healing_boost',
    ),

    # accessory abilities
    AnonymousAbility(
        id='farming_talisman',
        display_id='increase_held_region_speed',
        variables={'percent': 10, 'place': ('farm', 'barn', 'desert')},
    ),
    AnonymousAbility(
        id='vaccine_talisman',
        display_id='poison_immunity',
    ),
    AnonymousAbility(
        id='farmer_orb',
        display_id='farmer_orb',
    ),
    AnonymousAbility(
        id='night_vision_charm',
        display_id='night_vision_charm',
    ),
    AnonymousAbility(
        id='speed_talisman',
        display_id='give_held_speed',
        variables={'amount': 1},
    ),
    AnonymousAbility(
        id='speed_ring',
        display_id='give_held_speed',
        variables={'amount': 3},
    ),
    AnonymousAbility(
        id='speed_artifact',
        display_id='give_held_speed',
        variables={'amount': 5},
    ),
    AnonymousAbility(
        id='feather_talisman',
        display_id='feather_talisman',
    ),
    AnonymousAbility(
        id='feather_ring',
        display_id='feather_ring',
    ),
    AnonymousAbility(
        id='feather_artifact',
        display_id='feather_artifact',
    ),
    AnonymousAbility(
        id='piggy_bank',
        display_id='piggy_bank',
    ),
    AnonymousAbility(
        id='cracked_piggy_bank',
        display_id='cracked_piggy_bank',
        variables={'percent': 75},
    ),
    AnonymousAbility(
        id='broken_piggy_bank',
        display_id='broken_piggy_bank',
    ),
    AnonymousAbility(
        id='haste_ring',
        display_id='grant_mining_speed',
        variables={'amount': 50},
    ),
    AnonymousAbility(
        id='experience_artifact',
        display_id='gain_exp',
        variables={'percent': 25},
    ),
    AnonymousAbility(
        id='talisman_of_coins',
        display_id='talisman_of_coins',
    ),
    AnonymousAbility(
        id='emerald_ring',
        display_id='emerald_ring',
        variables={'amount': 1},
    ),
    AnonymousAbility(
        id='wood_affinity_talisman',
        display_id='gain_region_speed',
        variables={'value': 100, 'place': (
            'forest', 'graveyard', 'wilderness',
        )},
    ),
    AnonymousAbility(
        id='healing_talisman',
        display_id='increase_healing',
        variables={'percent': 5},
    ),
    AnonymousAbility(
        id='healing_ring',
        display_id='increase_healing',
        variables={'percent': 10},
    ),
    AnonymousAbility(
        id='sea_creature_talisman',
        display_id='sea_creature_talisman',
        variables={'percent': 5},
    ),
    AnonymousAbility(
        id='sea_creature_ring',
        display_id='sea_creature_talisman',
        variables={'percent': 10},
    ),
    AnonymousAbility(
        id='sea_creature_artifact',
        display_id='sea_creature_talisman',
        variables={'percent': 15},
    ),
    AnonymousAbility(
        id='titanium_talisman',
        display_id='grant_mining_speed',
        variables={'amount': 15},
    ),
    AnonymousAbility(
        id='titanium_ring',
        display_id='grant_mining_speed',
        variables={'amount': 30},
    ),
    AnonymousAbility(
        id='titanium_artifact',
        display_id='grant_mining_speed',
        variables={'amount': 45},
    ),
    AnonymousAbility(
        id='titanium_relic',
        display_id='grant_mining_speed',
        variables={'amount': 60},
    ),
    AnonymousAbility(
        id='skeleton_talisman',
        display_id='reduce_damage_taken',
        variables={'entities': 'skeletons', 'percent': 5},
    ),
    AnonymousAbility(
        id='wolf_talisman',
        display_id='reduce_damage_taken',
        variables={'entities': 'wolves', 'percent': 5},
    ),
    AnonymousAbility(
        id='wolf_ring',
        display_id='reduce_damage_taken',
        variables={'entities': 'wolves', 'percent': 10},
    ),
    AnonymousAbility(
        id='zombie_talisman',
        display_id='reduce_damage_taken',
        variables={'entities': 'zombies', 'percent': 5},
    ),
    AnonymousAbility(
        id='zombie_ring',
        display_id='reduce_damage_taken',
        variables={'entities': 'zombies', 'percent': 10},
    ),
    AnonymousAbility(
        id='zombie_artifact',
        display_id='reduce_damage_taken',
        variables={'entities': 'zombies', 'percent': 15},
    ),
    AnonymousAbility(
        id='devour_ring',
        display_id='devour_ring'
    ),
    AnonymousAbility(
        id='spider_talisman',
        display_id='reduce_damage_taken',
        variables={'entities': 'spiders', 'percent': 5},
    ),
    AnonymousAbility(
        id='spider_ring',
        display_id='reduce_damage_taken',
        variables={'entities': 'spiders', 'percent': 10},
    ),
    AnonymousAbility(
        id='spider_artifact',
        display_id='reduce_damage_taken',
        variables={'entities': 'spiders', 'percent': 15},
    ),
    AnonymousAbility(
        id='tarantula_talisman',
        display_id='tarantula_talisman'
    ),
    AnonymousAbility(
        id='ender_artifact',
        display_id='reduce_damage_taken',
        variables={'entities': 'end_mobs', 'percent': 20},
    ),
    AnonymousAbility(
        id='ender_relic',
        display_id='reduce_damage_taken',
        variables={'entities': 'end_mobs', 'percent': 25},
    ),
    AnonymousAbility(
        id='wither_artifact',
        display_id='reduce_damage_taken',
        variables={'entities': 'withers', 'percent': 20},
    ),
    AnonymousAbility(
        id='nether_artifact',
        display_id='reduce_damage_taken',
        variables={'entities': 'nether mobs', 'percent': 5},
    ),
    AnonymousAbility(
        id='village_affinity_talisman',
        display_id='increase_held_region_speed',
        variables={'percent': 10, 'place': ('village',)},
    ),
    AnonymousAbility(
        id='mine_affinity_talisman',
        display_id='increase_held_region_speed',
        variables={'percent': 10, 'place': ('gold', 'deep', 'mines')},
    ),
    AnonymousAbility(
        id='intimidation_talisman',
        display_id='intimidation',
        variables={'value': 1},
    ),
    AnonymousAbility(
        id='intimidation_ring',
        display_id='intimidation',
        variables={'value': 5},
    ),
    AnonymousAbility(
        id='intimidation_artifact',
        display_id='intimidation',
        variables={'value': 25},
    ),
    AnonymousAbility(
        id='scavenger_talisman',
        display_id='scavenger_talisman',
    ),
    AnonymousAbility(
        id='hegemony_artifact',
        display_id='hegemony_artifact',
    ),

    # three piece bonus
    NamedAbility(
        id='revenant_trolling_the_reaper',
        name='Full Set Bonus: Trolling The Reaper',
        display_id='revenant_trolling_the_reaper',
    ),
    NamedAbility(
        id='reaper_trolling_the_reaper',
        name='Full Set Bonus: Trolling The Reaper',
        display_id='reaper_trolling_the_reaper',
    ),
    NamedAbility(
        id='absolute_unit',
        name='Full Set Bonus: Absolute Unit',
        display_id='absolute_unit',
    ),

    TieredBonus(
        id='shimmer',
        name='Tiered Armor Bonus: Shimmer',
        display_id='shimmer',
        tiered_variables={'value': [0, 100, 200, 300]},
    ),
]


def get_ability(id: str, /, *, warn=True) -> Ability | None:
    for item in ABILITIES:
        if item.id == id:
            return get(ABILITIES, id=id)

    if warn:
        red(f'Ability not found: {id!r}')
