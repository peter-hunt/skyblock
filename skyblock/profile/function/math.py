from collections import defaultdict
from math import ceil
from os import get_terminal_size
from typing import Optional

from ...constant.ability import SET_BONUSES
from ...constant.colors import *
from ...constant.main import COLL_ALTER, SKILL_EXP
from ...constant.mobs import BESTIARY_ALTER
from ...constant.util import Number
from ...function.math import (
    calc_exp_level, calc_bestiary_level, calc_pet_level, calc_skill_level,
    display_skill_reward,
)
from ...function.io import *
from ...function.reforging import get_modifier
from ...function.util import (
    format_name, format_number, format_roman, get_family, parse_int,
)
from ...object.collection import is_collection, get_collection, calc_coll_level
from ...object.mobs import MOBS, get_mob
from ...object.object import *
from ...object.recipes import get_recipe


__all__ = [
    'add_exp', 'add_kill', 'add_skill_exp', 'get_bestiary_amount',
    'get_bestiary_level', 'get_bestiary_milestone', 'get_bestiary_total',
    'get_collection_amount', 'get_collection_level', 'collect', 'get_skill_exp',
    'get_skill_level', 'get_stat', 'parse_index',
]


def add_exp(self, amount: Number, /):
    enchanting_level = self.get_skill_level('enchanting')
    original_level = calc_exp_level(self.experience)
    self.experience += amount * (1 + 0.04 * enchanting_level)
    current_level = calc_exp_level(self.experience)
    if current_level > original_level:
        green(f'Reached XP level {current_level}.')


def add_kill(self, name: str, value: int = 1):
    family = get_family(name)
    display = format_name(family)

    kills = self.get_bestiary_amount(name)

    if kills == 0 and value > 0:
        dark_aqua(f'{BOLD}BESTIARY FAMILY UNLOCKED {AQUA}{display}')

    original_level = self.get_bestiary_level(name)
    original_ms = self.get_bestiary_milestone()
    self.stats[f'kills_{family}'] = kills + value
    current_level = self.get_bestiary_level(name)
    current_ms = self.get_bestiary_milestone()

    if original_level == current_level:
        return

    width, _ = get_terminal_size()
    width = ceil(width * 0.8)
    dark_aqua(f"{BOLD}{'':-^{width}}")

    original_str = format_roman(original_level) if original_level != 0 else '0'
    dark_aqua(f' {BOLD}BESTIARY {AQUA}{BOLD}{display}'
              f' {DARK_GRAY}{original_str}➜'
              f'{YELLOW}{format_roman(current_level)}\n')

    lvl_delta = current_level - original_level
    original_stat = min(original_level, 5)
    original_stat += 2 * max(min(original_level - 5, 5), 0)
    original_stat += 3 * max(original_level - 10, 0)
    current_stat = min(current_level, 5)
    current_stat += 2 * max(min(current_level - 5, 5), 0)
    current_stat += 3 * max(current_level - 10, 0)
    stat_delta = current_stat - original_stat

    if name in BESTIARY_ALTER:
        mob_names = BESTIARY_ALTER[name]
    else:
        mob_names = [name]
    mobs = [get_mob(mob_name) for mob_name in mob_names]
    drops = []
    for mob in mobs:
        drops += mob.drops
    drops = sorted(drops, key=lambda drop: ('curlp'.index(drop[2][0]), drop[0]['name']))
    drop_rarities = [*{*[drop[2] for drop in drops]}]
    drop_rarities = sorted(drop_rarities, key=lambda rarity: 'curlp'.index(rarity[0]))

    magic_find = STAT_COLORS['magic_find']
    strength = STAT_COLORS['strength']
    loot_unlocked = {1: 'common', 3: 'uncommon', 5: 'rare', 7: 'legendary', 9: 'pray_rngesus'}.get(current_level, '')
    if loot_unlocked in drop_rarities:
        loot_str = f'\n  {RARITY_COLORS[loot_unlocked]}{format_name(loot_unlocked)} Loot Info'
    else:
        loot_str = ''
    aqua(
        f' {BOLD}REWARDS\n'
        f'  {DARK_GRAY}+{GREEN}{stat_delta} {display} {magic_find} Magic Find\n'
        f'  {DARK_GRAY}+{GREEN}{stat_delta} {display} {strength} Strength\n'
        f'  {DARK_GRAY}+{GOLD}{lvl_delta}% {GREEN}{display} {GRAY}coins\n'
        f'  {DARK_GRAY}+{GREEN}{lvl_delta * 20}%'
        f' {GRAY}chance for extra XP orbs{loot_str}'
    )

    if current_ms > original_ms:
        original_ms_str = format_roman(original_ms)
        current_ms_str = format_roman(current_ms)
        ms_delta = current_ms - original_ms
        gold(
            f"\n {BOLD}BESTIARY MILESTONE {DARK_GRAY}{original_ms_str}➜"
            f"{YELLOW}{current_ms_str}\n"
            f"  {DARK_GRAY}+{GREEN}{ms_delta * 2} HP"
            f" {STAT_COLORS['health']} Health"
        )
        combat_xp_reward = 0
        for level in range(original_ms + 1,
                           min(current_ms + 1, 17)):
            if level == 2:
                combat_xp_reward += 100
            elif level == 10:
                combat_xp_reward += 10000
            elif level == 14:
                combat_xp_reward += 100000
            elif level == 16:
                combat_xp_reward += 500000
        combat_xp_reward += 1000000 * max(current_ms - 16, 0)
        if combat_xp_reward != 0:
            combat_xp_str = format_number(combat_xp_reward)
            dark_gray(f'  +{DARK_AQUA}{combat_xp_str} {GRAY}Combat Experience')
            self.add_skill_exp('combat', combat_xp_reward)

    dark_aqua(f"{BOLD}{'':-^{width}}")


def add_skill_exp(self, name: str, amount: Number, /, *, display=False):
    if not hasattr(self, f'experience_skill_{name}'):
        red(f'Skill not found: {name}')
        return

    exp = self.get_skill_exp(name)
    original_level = calc_skill_level(name, exp)
    exp += amount
    setattr(self, f'experience_skill_{name}', exp)
    current_level = calc_skill_level(name, exp)

    if display:
        self.display_skill_add(name, amount)

    if current_level > original_level:
        coins_reward = 0
        if name != 'catacombs':
            for lvl in range(original_level + 1, current_level + 1):
                coins_reward += SKILL_EXP[lvl][3]

        self.purse += coins_reward

        width, _ = get_terminal_size()
        width = ceil(width * 0.8)

        dark_aqua(f"{BOLD}{'':-^{width}}")
        original_str = format_roman(
            original_level) if original_level != 0 else '0'
        aqua(f' {BOLD}SKILL LEVEL UP {DARK_AQUA}{format_name(name)}'
             f' {DARK_GRAY}{original_str}➜'
             f'{DARK_AQUA}{format_roman(current_level)}\n')
        green(f' {BOLD}REWARDS')
        display_skill_reward(name, original_level, current_level)
        dark_aqua(f"{BOLD}{'':-^{width}}")

    if name != 'taming':
        taming_level = self.get_skill_level('taming')

        for pet_index, pet in enumerate(self.pets):
            if pet.active:
                break
        else:
            pet_index = None

        if pet_index is not None:
            pet_exp = pet.exp

            original_pet_level = calc_pet_level(pet.rarity, pet_exp)

            if pet.category == name:
                pass
            elif name in {'alchemy', 'enchanting'}:
                amount /= 12
            else:
                amount /= 4
            amount *= 1 + taming_level / 100

            pet_exp += amount
            self.add_skill_exp('taming', amount / 2)

            self.pets[pet_index].exp = pet_exp
            current_pet_level = calc_pet_level(pet.rarity, pet_exp)

            if current_pet_level > original_pet_level:
                pet_str = pet.display().split(']')[1].lstrip()
                green(f'Your {pet_str}{GREEN} levelled up to'
                      f' level {BLUE}{current_pet_level}{GREEN}!')


def get_bestiary_amount(self, name: str, /) -> int:
    family = get_family(name)
    return self.stats.get(f'kills_{family}', 0)


def get_bestiary_level(self, name: str, /) -> int:
    return calc_bestiary_level(self.get_bestiary_amount(name))


def get_bestiary_milestone(self, /) -> int:
    return self.get_bestiary_total() // 10


def get_bestiary_total(self, /) -> int:
    count = 0
    used_families = {*()}
    for mob in MOBS:
        family = get_family(mob.name)
        if family in used_families:
            continue
        used_families.add(family)
        count += self.get_bestiary_level(family)

    return count


def get_collection_amount(self, name: str, /) -> Optional[int]:
    if not is_collection(name):
        red(f'Unknown collection: {name!r}')
        return
    return self.collection[name]


def get_collection_level(self, name: str, /) -> Optional[int]:
    if not is_collection(name):
        red(f'Unknown collection: {name!r}')
        return
    return calc_coll_level(name, self.collection[name])


def collect(self, name: str, amount: int, /):
    if name in COLL_ALTER:
        alter_name, alter_mult = COLL_ALTER[name]
        self.collect(alter_name, amount * alter_mult)
        return

    if not is_collection(name):
        return

    display = format_name(name)

    original_level = self.get_collection_level(name)

    if self.collection[name] == 0 and amount > 0:
        gold(f' {BOLD}COLLECTION UNLOCKED {YELLOW}{display}')

    self.collection[name] += amount

    current_level = self.get_collection_level(name)

    if current_level <= original_level:
        return

    width, _ = get_terminal_size()
    width = ceil(width * 0.8)
    yellow(f"{BOLD}{'':-^{width}}")

    coll = get_collection(name)

    original = format_roman(original_level) if original_level != 0 else '0'
    gold(f' {BOLD}COLLECTION LEVEL UP {YELLOW}{format_name(name)}'
         f' {GRAY}{original}➜{YELLOW}{format_roman(current_level)}\n')

    rewards = []

    for index, (_, rwds) in enumerate(coll.levels):
        if original_level < index + 1 <= current_level:
            if isinstance(rwds, tuple):
                rewards += rwds
            else:
                rewards.append(rwds)

    green(f' REWARDS')
    for reward in rewards:
        if isinstance(reward, (float, int)):
            dark_gray(f'  +{DARK_AQUA}{reward}{GRAY}'
                      f' {format_name(coll.category)} Experience')
        elif isinstance(reward, str):
            recipe = get_recipe(reward)
            if isinstance(reward, Recipe):
                item = reward.result[0]
                color = RARITY_COLORS[item.rarity]
                white(f'  {color}{format_name(item.name)} {GRAY}Recipe'
                      f' {DARK_GRAY}({recipe.name})')
            else:
                white(f'  {format_name(recipe.name)} {GRAY}Recipe'
                      f' {DARK_GRAY}({recipe.name})')

    yellow(f"{BOLD}{'':-^{width}}")

    for reward in rewards:
        if isinstance(reward, (float, int)):
            self.add_skill_exp(coll.category, reward, display=True)


def get_skill_exp(self, name: str, /) -> int:
    if not hasattr(self, f'experience_skill_{name}'):
        red(f'Skill not found: {name}')
        return

    return getattr(self, f'experience_skill_{name}')


def get_skill_level(self, name: str, /) -> int:
    if not hasattr(self, f'experience_skill_{name}'):
        red(f'Skill not found: {name}')
        return

    return calc_skill_level(name, getattr(self, f'experience_skill_{name}'))


def get_stat(self, name: str, index: Optional[int] = None, /, *,
             separated: bool = False):
    base_value = 0
    bonus_value = 0

    active_pet = self.get_active_pet()
    has_active_pet = isinstance(active_pet, Pet)

    if index is None:
        item = Empty()

    else:
        item = self.inventory[index]

        if not isinstance(item, (Bow, Sword, Axe, Hoe,
                                 Pickaxe, Drill, FishingRod)):
            item = Empty()

    if getattr(item, 'modifier', None) is not None:
        bonus_value += get_modifier(item.modifier, item.rarity).get(name, 0)

    item_ench = getattr(item, 'enchantments', {})

    if name == 'strength':
        if isinstance(item, (Bow, Sword, FishingRod)):
            bonus_value += item.hot_potato * 2
    if name == 'crit_damage':
        bonus_value += item_ench.get('critical', 0) * 10
    elif name == 'mining_speed':
        if item_ench.get('efficiency', 0) != 0:
            bonus_value += 10 + item_ench['efficiency'] * 20
    elif name == 'sea_creature_chance':
        bonus_value += item_ench.get('angler', 0)
        bonus_value += item_ench.get('expertise', 0) * 0.6
    elif name == 'ferocity':
        bonus_value += item_ench.get('vicious', 0)
    elif name == 'mining_fortune':
        bonus_value += item_ench.get('fortune', 0) * 10
    elif name == 'farming_fortune':
        bonus_value += item_ench.get('cultivating', 0)
        bonus_value += item_ench.get('harvesting', 0) * 12.6

    if item is not None and not isinstance(item, Accessory):
        bonus_value += item.get_stat(name, self)

    combat_level = self.get_skill_level('combat')
    farming_level = self.get_skill_level('farming')
    enchanting_level = self.get_skill_level('enchanting')
    foraging_level = self.get_skill_level('foraging')
    fishing_level = self.get_skill_level('fishing')
    mining_level = self.get_skill_level('mining')
    taming_level = self.get_skill_level('taming')
    bestiary_ms = self.get_bestiary_milestone()

    set_bonus = True

    for piece in self.armor:
        if not isinstance(piece, Armor):
            set_bonus = False
            continue

        bonus_value += getattr(piece, name, 0)

        if getattr(piece, 'modifier', None) is not None:
            modifier_bonus = get_modifier(piece.modifier, piece.rarity)
            bonus_value += modifier_bonus.get(name, 0)

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

    for item in self.inventory:
        if isinstance(item, Accessory):
            if item.modifier is not None:
                modifier_bonus = get_modifier(item.modifier, item.rarity)
                if item.name == 'hegemony_artifact':
                    bonus_value += modifier_bonus.get(name, 0) * 2
                else:
                    bonus_value += modifier_bonus.get(name, 0)

    for piece in self.armor:
        if not isinstance(piece, Armor):
            continue

        delta = 0
        armor_ench = getattr(piece, 'enchantments', {})

        if name == 'health':
            delta += piece.hot_potato * 4
            if set_bonus == 'old_blood':
                delta += armor_ench.get('growth', 0) * 25
            else:
                delta += armor_ench.get('growth', 0) * 15
        elif name == 'defense':
            delta += piece.hot_potato * 2
            if set_bonus == 'old_blood':
                delta += armor_ench.get('protection', 0) * 5
            else:
                delta += armor_ench.get('protection', 0) * 3
        elif name == 'true_defense':
            if set_bonus == 'old_blood':
                delta += armor_ench.get('true_protection', 0) * 5
            else:
                delta += armor_ench.get('true_protection', 0) * 3
        elif name == 'speed':
            if set_bonus == 'old_blood':
                delta += armor_ench.get('sugar_rush', 0) * 4
            else:
                delta += armor_ench.get('sugar_rush', 0) * 2
        elif name == 'intelligence':
            delta += armor_ench.get('big_brain', 0) * 5
            delta += armor_ench.get('smarty_pants', 0) * 5

        if set_bonus == 'ender_armor':
            if self.island == 'end':
                delta *= 2
        if set_bonus == 'glacite_expert_miner' and name == 'defense':
            if self.island in {'gold', 'deep', 'mines'}:
                delta *= 2

        bonus_value += delta

    pet_mult = 0

    if has_active_pet:
        pet_mult = calc_pet_level(active_pet.rarity, active_pet.exp) / 100
        bonus_value += getattr(active_pet, name, 0) * pet_mult

    cap = None

    if name == 'health':
        base_value += 100
        base_value += min(farming_level, 14) * 2
        base_value += max(min(farming_level - 14, 5), 0) * 3
        base_value += max(min(farming_level - 19, 6), 0) * 4
        base_value += max(min(farming_level - 25, 35), 0) * 5
        base_value += min(fishing_level, 14) * 2
        base_value += max(min(fishing_level - 14, 5), 0) * 3
        base_value += max(min(fishing_level - 19, 6), 0) * 4
        base_value += max(min(fishing_level - 25, 35), 0) * 5
        base_value += 2 * bestiary_ms
        if set_bonus == 'lapis_armor_health':
            bonus_value += 60
        if has_active_pet:
            if 'archimedes' in active_pet.abilities:
                bonus_value += (base_value + bonus_value) * (0.2 * pet_mult)
    elif name == 'defense':
        base_value += min(mining_level, 14) * 1
        base_value += max(min(mining_level - 14, 46), 0) * 2
        if has_active_pet:
            if 'turtle_tactics' in active_pet.abilities:
                base_value *= 1 + 0.2 * pet_mult
    elif name == 'strength':
        base_value += min(foraging_level, 14) * 1
        base_value += max(min(foraging_level - 14, 36), 0) * 2
    elif name == 'speed':
        cap = 400
        base_value += 100
        if set_bonus == 'speedster_armor':
            bonus_value += 20
        elif set_bonus == 'farm_armor_speed':
            if self.island in {'barn', 'desert'} or self.zone == 'farm':
                bonus_value += 25
        elif set_bonus == 'farm_suit_speed':
            if self.island in {'barn', 'desert'}:
                bonus_value += 20
        elif set_bonus == 'young_blood':
            cap += 100
        if has_active_pet:
            if self.island == 'park':
                if 'epic_vine_swing' in active_pet.abilities:
                    bonus_value += 100 * pet_mult
                elif 'rare_vine_swing' in active_pet.abilities:
                    bonus_value += 75 * pet_mult
            if 'hunter' in active_pet.abilities:
                bonus_value += 100 * pet_mult
                cap += 100 * pet_mult
        if self.has_item({'name': 'speed_artifact'}):
            bonus_value += 5
        elif self.has_item({'name': 'speed_ring'}):
            bonus_value += 3
        elif self.has_item({'name': 'speed_talisman'}):
            bonus_value += 1
        if self.has_item({'name': 'farming_talisman'}):
            if self.island in {'barn', 'desert'} or self.zone == 'farm':
                bonus_value += (base_value + bonus_value) * 0.1
        if self.has_item({'name': 'wood_affinity_talisman'}):
            if self.zone in {'forest', 'graveyard', 'wilderness'}:
                bonus_value += (base_value + bonus_value) * 0.1
        if self.has_item({'name': 'village_affinity_talisman'}):
            if self.zone == 'village':
                bonus_value += (base_value + bonus_value) * 0.1
        if self.has_item({'name': 'mine_affinity_talisman'}):
            if (self.island in {'gold', 'deep', 'mines'}
                    or self.zone == 'coal_mine'):
                bonus_value += (base_value + bonus_value) * 0.1
    elif name == 'crit_chance':
        base_value += 30
        base_value += combat_level * 0.5
    elif name == 'crit_damage':
        base_value += 50
    elif name == 'intelligence':
        base_value += 100
        base_value += min(enchanting_level, 14) * 1
        base_value += max(min(enchanting_level - 14, 46), 0) * 2
    elif name == 'sea_creature_chance':
        base_value += 20
        if has_active_pet:
            if 'epic_echolocation' in active_pet.abilities:
                bonus_value += (base_value + bonus_value) * (0.1 * pet_mult)
            elif 'rare_echolocation' in active_pet.abilities:
                bonus_value += (base_value + bonus_value) * (0.07 * pet_mult)
    elif name == 'magic_find':
        if has_active_pet:
            if 'supernatural' in active_pet.abilities:
                bonus_value += 15 * pet_mult

        pet_rarities = defaultdict(int)

        for index, pet in enumerate(self.pets):
            pet_rarities[pet.name] = max(pet_rarities[pet.name],
                                        ' curelm'.index(pet.rarity[0]))

        pet_score = sum({**pet_rarities}.values())
        pet_milestones = [10, 25, 50, 75, 100, 130, 175]
        for milestone in pet_milestones:
            if pet_score >= milestone:
                base_value += 1
            else:
                break
    elif name == 'pet_luck':
        base_value += taming_level
        if has_active_pet:
            if 'omen' in active_pet.abilities:
                bonus_value += 15 * pet_mult
    elif name == 'mining_speed':
        if set_bonus == 'glacite_armor':
            bonus_value += 2 * mining_level
        if self.has_item({'name': 'haste_ring'}):
            bonus_value += 50
        if self.has_item({'name': 'titanium_relic'}):
            bonus_value += 60
        elif self.has_item({'name': 'titanium_artifact'}):
            bonus_value += 45
        elif self.has_item({'name': 'titanium_ring'}):
            bonus_value += 30
        elif self.has_item({'name': 'titanium_talisman'}):
            bonus_value += 15
    elif name == 'ferocity':
        if has_active_pet:
            if 'legendary_merciless_swipe' in active_pet.abilities:
                bonus_value += (base_value + bonus_value) * (0.5 * pet_mult)
            elif 'uncommon_merciless_swipe' in active_pet.abilities:
                bonus_value += (base_value + bonus_value) * (0.33 * pet_mult)
            elif 'common_merciless_swipe' in active_pet.abilities:
                bonus_value += (base_value + bonus_value) * (0.15 * pet_mult)
    elif name == 'mining_fortune':
        base_value += mining_level * 4
    elif name == 'foraging_fortune':
        base_value += foraging_level * 4
    elif name == 'farming_fortune':
        base_value += farming_level * 4

    if set_bonus == 'superior_dragon_armor':
        bonus_value += (base_value + bonus_value) * 0.05
    if set_bonus == 'fairy_armor' and name == 'speed':
        bonus_value += (base_value + bonus_value) * 0.1

    if has_active_pet:
        if 'superior' in active_pet.abilities:
            bonus_value += (base_value + bonus_value) * (0.1 * pet_mult)

    if cap is not None:
        base_vaule = min(cap, base_value)
        bonus_value = min(cap - base_value, bonus_value)
    elif name in {'defense', 'speed', 'crit_chance'}:
        base_value = max(base_value, 0)
        bonus_value = max(base_value + bonus_value, 0) - base_value

    if separated:
        return base_value, bonus_value
    else:
        return base_value + bonus_value


def parse_index(self, word: str, length: Optional[int] = None,
                /, *, warn: bool = True) -> Optional[int]:
    index = parse_int(word, warn=warn)
    if index is None:
        return
    if length is None:
        length = len(self.inventory)
    if (index <= 0 or index > length) and warn:
        red(f'Index out of bound: {index}')
        return
    return index - 1


math_functions = {
    name: globals()[name] for name in __all__
}
