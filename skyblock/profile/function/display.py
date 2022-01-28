from collections import defaultdict
from math import ceil, floor, radians, tan
from os import get_terminal_size
from random import choice
from time import sleep
from typing import Iterable, Optional, Union

from ...constant.colors import *
from ...constant.main import ARMOR_PARTS
from ...constant.mobs import BESTIARY_ALTER
from ...constant.stat import ALL_STATS, HIDDEN_STATS, PERC_STATS
from ...constant.util import Number
from ...format.function import format_temp
from ...format.template import get_template
from ...function.io import *
from ...function.math import (
    calc_bestiary_upgrade_amount, calc_skill_level_info, display_skill_reward,
    fround,
)
from ...function.util import (
    format_name, format_number, format_roman, format_short, format_zone,
    get, get_family, index,
)
from ...object.collection import COLLECTIONS, get_collection
from ...object.items import get_item
from ...object.mobs import MOBS, get_mob
from ...object.object import *
from ...object.recipes import CRAFTABLES, get_recipe
from ...map.islands import ISLANDS
from ...map.object import *


__all__ = [
    'display_armor', 'display_bestiary', 'display_bestiaries',
    'display_collection_info', 'display_collection', 'display_collections',
    'display_hotm', 'display_item', 'display_inv', 'display_location',
    'display_minion_info', 'display_minions', 'display_money', 'display_pets',
    'display_playtime', 'display_recipe_info', 'display_recipe',
    'display_recipes', 'display_shop', 'display_stat', 'display_stats',
    'display_skill_add', 'display_skill', 'display_skills', 'display_warp',
    'npc_silent', 'npc_speak',
]


def display_armor(self, part: Optional[str] = None, /):
    if part:
        item = self.armor[ARMOR_PARTS.index(part)]
        self.display_item(item)
        return

    for piece, name in zip(self.armor, ARMOR_PARTS):
        gray(f'{format_name(name)}: {piece.display()}')


def display_bestiary(self, name: str, /):
    width, _ = get_terminal_size()
    width = ceil(width * 0.85)

    display = format_name(name)
    family = get_family(name)

    kills = self.stats.get(f'kills_{family}', 0)
    deaths = self.stats.get(f'deaths_{name}', 0)
    lvl = self.get_bestiary_level(family)

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

    if kills == 0:
        red("You haven't unlocked this bestiary family yet!")
        return

    yellow(f"{BOLD}{'':-^{width}}")
    aqua(f'{display} {format_roman(lvl)}\n')
    gray(f'Kills: {GREEN}{kills}')
    gray(f'Deaths: {GREEN}{deaths}')

    for rarity in drop_rarities:
        print(f'\n{RARITY_COLORS[rarity]}{format_name(rarity)} Loot{CLN}')
        required_lvl = {'c': 1, 'u': 3, 'r': 5, 'l': 7, 'p': 9}[rarity[0]]
        if lvl >= required_lvl:
            for drop in drops:
                if drop[2] != rarity:
                    continue
                name = drop[0]['name']
                kwargs = {key: drop[0][key] for key in drop[0]
                        if key not in {'name', 'count'}}
                item = get_item(name, **kwargs)
                if getattr(item, 'count', 1) != 1:
                    item.count = 1
                count = drop[1]
                if count == 1:
                    count_str = ''
                elif isinstance(count, int):
                    count_str = f' x {count}'
                else:
                    count_str = f' x {count[0]}-{count[1]}'
                chance = '' if drop[3] == 1 else f' ({GREEN}{format_number(drop[3] * 100)}%{GRAY})'
                print(f' + {item.display()}{GRAY}{count_str}{chance}{CLN}')
        else:
            for drop in drops:
                if drop[2] == rarity:
                    print(f' + {RED}???{CLN}')

    amt_left, amt_to_next = calc_bestiary_upgrade_amount(kills)

    magic_find = STAT_COLORS['magic_find']
    strength = STAT_COLORS['strength']

    if lvl > 0:
        stat_boost = min(lvl, 5)
        stat_boost += 2 * max(min(lvl - 5, 5), 0)
        stat_boost += 3 * max(lvl - 10, 0)

        xp_orbs, chance = divmod(100 + lvl * 20, 100)
        if chance == 0:
            xp_orbs -= 1
            chance = 100

        aqua(
            f'\n {BOLD}{format_name(name)} Bonuses\n'
            f'{DARK_GRAY}+{AQUA}{stat_boost} {magic_find} Magic Find\n'
            f'{DARK_GRAY}+{RED}{stat_boost} {strength} Strength\n'
            f'{DARK_GRAY}+{GOLD}{lvl}% {GRAY}coin gain\n'
            f'{DARK_GRAY}+{GREEN}{chance}% {GRAY}chance for'
            f' {GREEN}+{xp_orbs}{GRAY} XP orbs\n'
        )

    perc = fround(amt_left / amt_to_next * 100, 2)
    gray(f'Progress to Tier {format_roman(lvl + 1)}: {AQUA}{perc}%')

    bar = min(floor(amt_left / amt_to_next * 20), 20)
    left, right = '-' * bar, '-' * (20 - bar)
    green(f'{BOLD}{left}{GRAY}{BOLD}{right} {AQUA}{format_number(amt_left)}'
          f'{DARK_AQUA}/{AQUA}{format_short(amt_to_next)}')

    gray(f'\nTier {format_roman(lvl + 1)} Rewards:')
    if lvl < 5:
        stat_delta = 1
    elif lvl < 10:
        stat_delta = 2
    else:
        stat_delta = 3
    loot_unlocked = {1: 'common', 3: 'uncommon', 5: 'rare', 7: 'legendary', 9: 'pray_rngesus'}.get(lvl + 1, '')
    if loot_unlocked in drop_rarities:
        loot_str = f'\n  {RARITY_COLORS[loot_unlocked]}{format_name(loot_unlocked)} Loot Info'
    else:
        loot_str = ''
    aqua(
        f'  {DARK_GRAY}+{GREEN}{stat_delta} {AQUA}{display}'
        f' {magic_find} Magic Find\n'
        f'  {DARK_GRAY}+{GREEN}{stat_delta} {AQUA}{display}'
        f' {strength} Strength\n'
        f'  {DARK_GRAY}+{GOLD}1% {AQUA}{display} {GRAY}coins\n'
        f'  {DARK_GRAY}+{GREEN}20% {GRAY}chance for extra XP orbs{loot_str}'
    )

    yellow(f"{BOLD}{'':-^{width}}")


def display_bestiaries(self, /):
    width, _ = get_terminal_size()
    width = ceil(width * 0.85)

    yellow(f"{BOLD}{'':-^{width}}")

    bestiary_total = self.get_bestiary_total()
    bestiary_ms = self.get_bestiary_milestone()
    gold(f'Bestiary Milestone {format_roman(bestiary_ms)}\n')
    gray(
        f'Reach new {GREEN}Milestones {GRAY}in your Bestiary'
        f' by unlocking unique family tiers.'
    )
    if bestiary_ms != 0:
        green(
            f"\nMilestone Bonus\n"
            f"{DARK_GRAY}+{GREEN}{format_number(2 * bestiary_ms)} HP"
            f" {STAT_COLORS['health']} Health"
        )
    gray(f'\nTotal Tiers Unlocked: {GREEN}{format_number(bestiary_total)}')

    ms_progress = bestiary_total % 10
    gray(
        f'\nProgress to Milestone {format_roman(bestiary_ms + 1)}: '
        f'{YELLOW}{ms_progress * 10}%'
    )
    bar = min(floor(ms_progress * 2), 20)
    left, right = '-' * bar, '-' * (20 - bar)
    green(f'{BOLD}{left}{GRAY}{BOLD}{right} {AQUA}{ms_progress}'
          f'{DARK_AQUA}/{AQUA}10')

    combat_xp_reward = 0
    if bestiary_ms + 1 == 2:
        combat_xp_reward = 100
    elif bestiary_ms + 1 == 10:
        combat_xp_reward = 10000
    elif bestiary_ms + 1 == 14:
        combat_xp_reward = 100000
    elif bestiary_ms + 1 == 16:
        combat_xp_reward = 500000
    elif bestiary_ms + 1 > 16:
        combat_xp_reward = 1000000

    gray(
        f"Milestone {format_roman(bestiary_ms + 1)} Reward\n"
        f"  {DARK_GRAY}+{GREEN}2 HP {STAT_COLORS['health']} Health"
    )
    if combat_xp_reward != 0:
        dark_gray(
            f'  +{DARK_AQUA}{format_number(combat_xp_reward)}'
            f' {GRAY}Combat Experience'
        )
    gray()

    displayed_families = []

    for mob in MOBS:
        family = get_family(mob.name)
        if family in displayed_families:
            continue
        displayed_families.append(family)

        bestiary_level = self.get_bestiary_amount(family)
        kills = self.stats.get(f'kills_{family}', 0)
        if kills == 0:
            gray('  unknown')
            continue
        bestiary_level = self.get_bestiary_level(mob.name)
        aqua(f'  {format_name(family)} {format_roman(bestiary_level)}')

    yellow(f"{BOLD}{'':-^{width}}")


def display_collection_info(self, name: str, /):
    width, _ = get_terminal_size()
    width = ceil(width * 0.85)
    yellow(f"{BOLD}{'':-^{width}}")

    coll = get_collection(name)
    lvl = self.get_collection_level(name)
    lvl_str = f' {format_roman(lvl)}' if lvl != 0 else ''
    display = format_name(name)

    current = self.get_collection_amount(name)

    yellow(f'{display}{lvl_str} {DARK_GRAY}({format_short(current)})')
    last_level = 0
    next_level = None
    rewards = None
    past_amount = 0

    for index, (amount, rwds) in enumerate(coll.levels):
        display = display

        if isinstance(rwds, (int, float, str)):
            rwds = [rwds]

        if amount > current and next_level is None:
            next_level = amount - last_level
            rewards = [reward for reward in rwds]
            past_amount = last_level
        last_level = amount

        gray(f'\n{display} {format_roman(index + 1)} Reward:'
             f' {DARK_GRAY}({format_short(amount)})')
        for reward in rwds:
            if isinstance(reward, (float, int)):
                dark_gray(f' +{DARK_AQUA}{reward}{GRAY}'
                          f' {format_name(coll.category)} Experience')
            elif isinstance(reward, str):
                recipe = get_recipe(reward)
                if isinstance(recipe, Recipe):
                    pointer = recipe.result
                    item_name = pointer['name']
                    kwargs = {key: pointer[key] for key in pointer
                              if key not in {'name', 'count'}}
                    item = get_item(item_name, **kwargs)
                    color = RARITY_COLORS[item.rarity]
                    white(f'  {color}{format_name(item_name)} {GRAY}Recipe'
                          f' {DARK_GRAY}({recipe.name})')
                else:
                    white(f'  {format_name(recipe.name)} {GRAY}Recipe'
                          f' {DARK_GRAY}({recipe.name})')

    this_level = current - past_amount
    if next_level is None:
        next_level = 0
        progress = 1
    else:
        progress = min(this_level / next_level, 1)
    bar = floor(progress * 20)
    left, right = '-' * bar, '-' * (20 - bar)
    if rewards is not None:
        gray(f'\nProgress: {YELLOW}{floor(progress * 100)}{GOLD}%')
    green(f'{BOLD}{left}{GRAY}{BOLD}{right} {YELLOW}{format_number(this_level)}'
          f'{GOLD}/{YELLOW}{format_short(next_level)}\n')
    if rewards is not None:
        gray(f'{display} {format_roman(lvl + 1)} Reward:')
        for reward in rewards:
            if isinstance(reward, (float, int)):
                dark_gray(f'  +{DARK_AQUA}{reward}{GRAY}'
                          f' {format_name(coll.category)} Experience')
            elif isinstance(reward, str):
                recipe = get_recipe(reward)
                if isinstance(recipe, Recipe):
                    pointer = recipe.result
                    item_name = pointer['name']
                    kwargs = {key: pointer[key] for key in pointer
                              if key not in {'name', 'count'}}
                    item = get_item(item_name, **kwargs)
                    color = RARITY_COLORS[item.rarity]
                    white(f'  {color}{format_name(item_name)} {GRAY}Recipe'
                          f' {DARK_GRAY}({recipe.name})')
                else:
                    white(f'  {format_name(recipe.name)} {GRAY}Recipe'
                          f' {DARK_GRAY}({recipe.name})')

    yellow(f"{BOLD}{'':-^{width}}")


def display_collection(self, category: str, /, *, end=True):
    width, _ = get_terminal_size()
    width = ceil(width * 0.85)
    yellow(f"{BOLD}{'':-^{width}}")

    green(f'{format_name(category)} Collections')
    colls = [coll for coll in COLLECTIONS if coll.category == category]

    if len(colls) == 0:
        gray('  none')
    else:
        for coll in colls:
            if self.collection[coll.name] == 0:
                gray('  unknown')
                continue
            name = format_name(coll.name)
            lvl = self.get_collection_level(coll.name)
            lvl_str = f' {format_roman(lvl)}' if lvl != 0 else ''
            yellow(f'  {name}{lvl_str}')

    if end:
        yellow(f"{BOLD}{'':-^{width}}")


def display_collections(self, /):
    for category in ('farming', 'mining', 'combat',
                     'foraging', 'fishing'):
        self.display_collection(category, end=False)


def display_hotm(self, /):
    powder_str = format_number(fround(self.mithril_powder))

    dark_green(f'᠅ {GRAY}Mithril Powder: {DARK_GREEN}{powder_str}')


def display_item(self, item: ItemType, /):
    if isinstance(item, Empty):
        gray('empty')
        return

    width, _ = get_terminal_size()
    width = ceil(width * 0.85)
    yellow(f"{BOLD}{'':-^{width}}")
    gray(item.info(self))
    yellow(f"{BOLD}{'':-^{width}}")


def display_inv(self, /):
    length = len(self.inventory)

    digits = len(f'{length}')
    empty_slots = []
    index = 0
    is_empty = True
    while index < length:
        item = self.inventory[index]
        if isinstance(item, Empty):
            while index < length:
                if not isinstance(self.inventory[index], Empty):
                    break
                empty_slots.append(index)
                index += 1
            continue

        is_empty = False
        if empty_slots:
            for empty_index in empty_slots:
                gray(f'{(empty_index + 1):>{digits + 2}}')
            empty_slots.clear()
        gray(f'{(index + 1):>{digits + 2}} {item.display()}')
        index += 1

    if is_empty:
        gray('Your inventory is empty.')


def display_location(self, /):
    island = get(ISLANDS, self.island)
    zone = get(island.zones, self.zone)

    gray('Location:')
    gray(f"  You're at {AQUA}{zone}{GRAY} of {AQUA}{island}{GRAY}.")
    gray('\nNearby places:')
    for conn in island.conns:
        if zone not in conn:
            continue
        other = conn[0] if conn[1] == zone else conn[1]
        sx, sz, ox, oz = zone.x, zone.z, other.x, other.z
        dx, dz = ox - sx, oz - sz
        direc = ''
        if dx == 0:
            direc = 'South' if dz > 0 else 'North'
        elif dz == 0:
            direc = 'East' if dx > 0 else 'West'
        else:
            if dx / dz < tan(radians(66.6)):
                direc += 'South' if dz > 0 else 'North'
            if dz / dx < tan(radians(66.6)):
                direc += 'East' if dx > 0 else 'West'
        gray(f'  {AQUA}{format_zone(other.name)}{GRAY}'
             f' on the {direc} ({other.name}).')

    if len(zone.resources) > 0:
        gray('\nResources:')
        for resource in zone.resources:
            gray(f'  {GREEN}{format_name(resource.name)}{GRAY}'
                 f' ({resource.name}).')

    if len(zone.mobs) > 0:
        gray('\nMobs:')
        for mob in zone.mobs:
            green(f'  {mob.display()}{GRAY} ({mob.name}).')

    if len(zone.npcs) > 0:
        gray('\nNPCs:')
        for npc in zone.npcs:
            gray(f'  {GREEN}{npc}{GRAY} ({npc.name}).')

    if zone.portal is not None:
        gray(f'\nPortal to {AQUA}{format_zone(zone.portal)}{GRAY}'
             f' ({zone.portal})')

    gray()


def display_minion_info(self, slot: int, /):
    minion = self.placed_minions[slot]

    gray(minion.display())

    length = len(minion.inventory)
    digits = len(f'{length}')
    index = 0
    while index < length:
        item = minion.inventory[index]
        if isinstance(item, Empty):
            while index < length:
                if not isinstance(minion.inventory[index], Empty):
                    break
                gray(f'{(index + 1):>{digits + 2}}')
                index += 1
            if index == length:
                break

        gray(f'{(index + 1):>{digits + 2}} {item.display()}')
        index += 1


def display_minions(self, /):
    length = len(self.placed_minions)
    digits = len(f'{length}')

    gray('Your placed minions:')

    for index, minion in enumerate(self.placed_minions):
        if isinstance(minion, Empty):
            gray(f'  {index + 1:>{digits}} empty')
        else:
            gray(f'  {index + 1:>{digits}} {minion.display()}')


def display_money(self, /):
    if (self.has_item({'name': 'piggy_bank'})
            or self.has_item({'name': 'cracked_piggy_bank'})):
        bank_type = 'Piggy'
    else:
        bank_type = 'Purse'

    if self.zone not in {'bank', 'dwarven_village'}:
        white(f'{bank_type}: {GOLD}{format_number(self.purse)} Coins')
        return

    balance_str = format_number(fround(self.balance, 1))
    if '.' not in balance_str:
        balance_str = balance_str + '  '
    purse_str = format_number(fround(self.purse, 1))
    if '.' not in purse_str:
        purse_str = purse_str + '  '
    length = max(len(balance_str), len(purse_str))

    green('Bank Account')
    gray(f'Balance: {GOLD}{balance_str:>{length}} Coins')
    white(f'{bank_type}:   {GOLD}{purse_str:>{length}} Coins')
    gray(f'Bank Level: {GREEN}{format_name(self.bank_level)}')


def display_pets(self, /):
    length = len(self.pets)
    if length == 0:
        gray("You don't have any pets in your pet menu!")
        return

    digits = len(f'{length}')

    gray('Your pets:')

    pet_rarities = defaultdict(int)

    for index, pet in enumerate(self.pets):
        active = f'{AQUA}*{GRAY}' if pet.active else ' '
        gray(f'{active} {index + 1:>{digits}} {pet.display()}')
        pet_rarities[pet.name] = max(pet_rarities[pet.name],
                                     ' curelm'.index(pet.rarity[0]))

    pet_score = sum({**pet_rarities}.values())
    pet_milestones = [10, 25, 50, 75, 100, 130, 175]
    milestone_tier = 0
    for milestone in pet_milestones:
        if pet_score >= milestone:
            milestone_tier += 1
        else:
            break

    green(
        f'\nPet Score Rewards\n'
        f'{GRAY}Pet score is calculated based on how many'
        f' {GREEN}unique {GRAY}pets you have and the {GREEN}rarity'
        f' {GRAY}of these pets.\n'
    )

    for tier, milestone in enumerate(pet_milestones, 1):
        pointer_str = f' {DARK_PURPLE}≪' if tier == milestone_tier else ''
        gold(f'{milestone} Score{GRAY}: +{AQUA}{tier} Magic Find{pointer_str}')

    blue(f'\nYour Pet Score: {WHITE}{pet_score}')


def display_playtime(self, /):
    all_mins = self.play_time // 60
    if all_mins == 0:
        red("You don't have enough playtime"
            " to use this command, try again later!")
        return
    hours, mins = divmod(all_mins, 60)
    green(f'You have {hours} hours and {mins:0>2} minutes playtime!')


def display_recipe_info(self, recipe: Union[Recipe, RecipeGroup], /):
    width, _ = get_terminal_size()
    width = ceil(width * 0.85)
    yellow(f"{BOLD}{'':-^{width}}")

    green(f'{format_name(recipe.name)}'
          f' {DARK_GRAY}({recipe.name})')
    dark_gray(f'{format_name(recipe.category)} Recipe')

    if isinstance(recipe, Recipe):
        recipes = [recipe]
    else:
        recipes = [get_recipe(name) for name in recipe.recipes]

    for index, _recipe in enumerate(recipes):
        if index != 0:
            gray()
        gray('\nIngredients:')
        for pointer in _recipe.ingredients:
            name = pointer['name']
            count = pointer.get('count', 1)
            kwargs = {key: pointer[key] for key in pointer
                      if key not in {'name', 'count'}}
            item = get_item(name, **kwargs)
            if getattr(item, 'count', 1) != 1:
                item.count = 1
            gray(f'  {item.display()}{DARK_GRAY} x {count}')
        gray('\nResult:')
        pointer = _recipe.result
        name = pointer['name']
        count = pointer.get('count', 1)
        kwargs = {key: pointer[key] for key in pointer
                  if key not in {'name', 'count'}}
        item = get_item(name, **kwargs)
        if getattr(item, 'count', 1) != 1:
            item.count = 1
        gray(f'  {item.display()}{DARK_GRAY} x {count}')

    requirements = []

    if recipe.collection_req is not None:
        coll_name, get_collection_level = recipe.collection_req
        lvl = self.get_collection_level(coll_name)
        if lvl < get_collection_level:
            requirements.append(
                f'{DARK_RED}❣ {RED}Requires {GREEN}'
                f'{format_name(coll_name)} Collection'
                f' {format_roman(get_collection_level)}'
            )

    if len(requirements) != 0:
        gray()
        for req in requirements:
            gray(req)

    yellow(f"{BOLD}{'':-^{width}}")


def display_recipe(self, category: Optional[str], /, *,
                   show_all=False, end=True):
    width, _ = get_terminal_size()
    width = ceil(width * 0.85)
    yellow(f"{BOLD}{'':-^{width}}")

    green(f'{format_name(category)} Recipes')
    recipes = [recipe for recipe in CRAFTABLES if recipe.category == category]

    if not show_all:
        recipes_copy = [recipe for recipe in recipes]
        recipes = []
        for recipe in recipes_copy:
            if recipe.collection_req is not None:
                coll_name, get_collection_level = recipe.collection_req
                lvl = self.get_collection_level(coll_name)
                if lvl < get_collection_level:
                    continue

            for pointer in recipe.ingredients:
                if not self.has_item(pointer):
                    break
            else:
                recipes.append(recipe)

    if len(recipes) == 0:
        gray('  none')
    else:
        for recipe in recipes:
            gray(f'  {AQUA}{format_name(recipe.name)}'
                 f' {DARK_GRAY}({recipe.name})')

    if end:
        yellow(f"{BOLD}{'':-^{width}}")


def display_recipes(self, /, *, show_all=False):
    for category in ('farming', 'mining', 'combat', 'foraging', 'fishing',
                     'enchanting', 'forging', 'smelting'):
        self.display_recipe(category, show_all=show_all, end=False)

    width, _ = get_terminal_size()
    width = ceil(width * 0.85)
    yellow(f"{BOLD}{'':-^{width}}")


def display_shop(self, npc: Npc, trade_index: Optional[int] = None, /):
    if trade_index is None:
        gray(f"{npc}'s shop:")
        if len(npc.trades) == 0:
            gray('  none')
            return

        digits = len(f'{len(npc.trades)}')
        for index, (cost, items) in enumerate(npc.trades):
            if not isinstance(items, list):
                items = [items]

            name = items[0]['name']
            kwargs = {key: items[0][key] for key in items[0]
                      if key not in {'name', 'count'}}
            item = get_item(name, **kwargs)
            if item is not None:
                if getattr(item, 'count', 1) != 1:
                    item.count = 1
                gray(f'  {(index + 1):>{digits}} {item.display()}')

            for pointer in items[1:]:
                name = pointer['name']
                kwargs = {key: pointer[key] for key in pointer
                        if key not in {'name', 'count'}}
                item = get_item(name, **kwargs)
                if item is None:
                    continue
                if getattr(item, 'count', 1) != 1:
                    item.count = 1

                gray(f'  {" " * digits} {item.display()}')

            if isinstance(cost, (int, float)):
                cost = [cost]
            for cost_pointer in cost:
                if isinstance(cost_pointer, int):
                    gray(f"  {'':>{digits}}   {GOLD}"
                         f"{format_number(cost_pointer)} coins{GRAY}")
                    continue

                cost_name = cost_pointer['name']
                count = cost_pointer.get('count', 1)
                cost_kwargs = {key: cost_pointer[key] for key in cost_pointer
                               if key not in {'name', 'count'}}
                cost_item = get_item(cost_name, **cost_kwargs)
                if getattr(cost_item, 'count', 1) != 1:
                    cost_item.count = 1
                count_str = '' if count == 1 else f' {GRAY}x {count}'
                gray(f"  {'':>{digits}}   {cost_item.display()}{count_str}")
    else:
        items = npc.trades[trade_index][1]
        if not isinstance(items, list):
            items = [items]
        for pointer in items:
            name = pointer['name']
            count = pointer.get('count', 1)
            kwargs = {key: pointer[key] for key in pointer
                    if key not in {'name', 'count'}}
            item = get_item(name, **kwargs)
            if getattr(item, 'count', 1) != 1:
                item.count = 1
            self.display_item(item)


def display_stat(self, stat_name: str, index: Optional[int] = None, /):
    width, _ = get_terminal_size()
    width = ceil(width * 0.85)

    dark_blue(f"{BOLD}{'':-^{width}}")

    value = floor(self.get_stat(stat_name, index))
    base_value, bonus_value = self.get_stat(stat_name, index, separated=True)
    base_value = floor(base_value)
    bonus_value = floor(bonus_value)
    if stat_name in PERC_STATS:
        ext = '%'
    else:
        ext = ' HP' if stat_name == 'health' else ''
    white(f'{STAT_COLORS[stat_name]} {format_name(stat_name)}'
          f' {WHITE}{format_number(value)}{ext}')

    temp_param = {}
    if stat_name == 'health':
        regen = value * 0.01 + 1.5
        if self.has_item({'name': 'healing_ring'}):
            regen *= 1.1
        elif self.has_item({'name': 'healing_talisman'}):
            regen *= 1.05
        temp_param['amount'] = regen

    desc_str = format_temp(get_template('stats', f'{stat_name}_desc'),
                           temp_param)
    gray(desc_str)

    gray(f'\nBase {format_name(stat_name)}: '
         f'{GREEN}{format_number(base_value)}{ext}')
    base_str = format_temp(get_template('stats', f'{stat_name}_base'))
    dark_gray(f'  {base_str}')

    gray(f'\nBonus {format_name(stat_name)}: '
         f'{DARK_GRAY}+{YELLOW}{format_number(bonus_value)}{ext}')
    bonus_str = format_temp(get_template('stats', f'{stat_name}_bonus'))
    dark_gray(f'  {bonus_str}')

    if stat_name == 'defense':
        if value <= 0:
            reduction = 0
        else:
            reduction = value / (100 + value) * 100

        health = self.get_stat('health', index)
        ehp = health * (1 + value / 100)
        ehp_str = format_number(floor(ehp))
        health_icon = STAT_COLORS['health']
        gray(f'\nDamage Reduction: {GREEN}{reduction:.1f}%')
        gray(f'Effective Health: {RED}{ehp_str}{health_icon}')
    elif stat_name == 'speed':
        gray(f'\nYou are {GREEN}{value - 100:.0f}% {GRAY}faster!')
    elif stat_name == 'intelligence':
        gray(f'\nMagic Damage: +{AQUA}{format_number(value)}%')
        gray(f'Mana Pool: {AQUA}{format_number(value + 100)}')
    elif stat_name.endswith('_fortune'):
        extra = value % 100
        if value <= 100:
            gray(f'Chance for {GREEN}double {GRAY}drops: {GREEN}'
                 f'{format_number(extra)}%')
        elif value <= 200:
            gray(f'Chance for {GREEN}double {GRAY}drops: {GREEN}'
                 f'100%')
            gray(f'Chance for {GOLD}triple {GRAY}drops: {GREEN}'
                 f'{format_number(extra)}%')
        elif value <= 300:
            gray(f'Chance for {GOLD}triple {GRAY}drops: {GREEN}'
                 f'100%')
            gray(f'Chance for {DARK_PURPLE}quadruple {GRAY}drops: {GREEN}'
                 f'{format_number(extra)}%')
        else:
            gray(f'Average drop multiplier: {GREEN}'
                 f'{format_number(value)}%')
    elif stat_name == 'ferocity':
        base, chance = divmod(value, 100)
        chance = floor(chance)
        gray(f'\nBase extra strikes: {RED}{format_number(base)}')
        gray(f'Chance for 1 more: {RED}{format_number(chance)}%')

    dark_blue(f"{BOLD}{'':-^{width}}")


def display_stats(self, index: Optional[int] = None, /):
    width, _ = get_terminal_size()
    width = ceil(width * 0.85)

    dark_blue(f"{BOLD}{'':-^{width}}")

    green('Your SkyBlock Profile')
    for stat_name in ALL_STATS:
        value = floor(self.get_stat(stat_name, index))
        if value == 0 and stat_name in HIDDEN_STATS:
            continue
        if stat_name in PERC_STATS:
            ext = '%'
        else:
            ext = ' HP' if stat_name == 'health' else ''
        white(f'  {STAT_COLORS[stat_name]} {format_name(stat_name)}'
              f' {WHITE}{format_number(value)}{ext}')

    dark_blue(f"{BOLD}{'':-^{width}}")


def display_skill_add(self, name: str, amount: Number, /):
    name_display = format_name(name)

    exp = self.get_skill_exp(name)
    _, exp_left, exp_to_next = calc_skill_level_info(name, exp)

    dark_aqua(f'+ {format_number(amount)} {name_display}'
              f' ({format_number(exp_left)}/{format_number(exp_to_next)})')


def display_skill(self, name: str, /, *,
                  reward: bool = True, end: bool = True):
    width, _ = get_terminal_size()
    width = ceil(width * 0.85)

    yellow(f"{BOLD}{'':-^{width}}")

    exp = self.get_skill_exp(name)
    lvl, exp_left, exp_to_next = calc_skill_level_info(name, exp)
    green(f'{format_name(name)} {format_roman(lvl)}')

    if exp_left < exp_to_next:
        perc = fround(exp_left / exp_to_next * 100, 2)
        gray(f'Progress to level {format_roman(lvl + 1)}: {YELLOW}{perc}%')

    bar = min(floor(exp_left / exp_to_next * 20), 20)
    left, right = '-' * bar, '-' * (20 - bar)
    green(f'{BOLD}{left}{GRAY}{BOLD}{right} {YELLOW}{format_number(exp_left)}'
          f'{GOLD}/{YELLOW}{format_short(exp_to_next)}')

    if reward and exp_left < exp_to_next:
        gray(f'\nLevel {format_roman(lvl + 1)} Rewards:')
        display_skill_reward(name, lvl, lvl + 1)

    if end:
        yellow(f"{BOLD}{'':-^{width}}")


def display_skills(self, /):
    width, _ = get_terminal_size()
    width = ceil(width * 0.85)

    for skill in ('farming', 'mining', 'combat', 'foraging', 'fishing',
                  'enchanting', 'alchemy', 'taming', 'catacombs'):
        self.display_skill(skill, reward=False, end=False)

    yellow(f"{BOLD}{'':-^{width}}")


def display_warp(self, /):
    gray('Unlocked fast travel destinations:')
    if len(self.fast_travel) == 0:
        gray('  none')
        return

    fast_travel = [scroll.copy() for scroll in self.fast_travel]
    fast_travel = sorted(fast_travel, key=lambda item: (
        index(ISLANDS, item[0]),
        index((island := get(ISLANDS, item[0])).zones,
              island.spawn if item[1] is None else item[1]),
    ))

    for island, zone in self.fast_travel:
        i_name = format_zone(island)
        r_name = 'Spawn' if zone is None else format_zone(zone)
        warp_name = island if zone is None else zone
        green(f'  {i_name}{GRAY} - {AQUA}{r_name}')
        dark_gray(f'  /warp {warp_name}')


@staticmethod
def npc_silent(name: str, /):
    npc_name = format_name(name)
    yellow(f'[NPC] {npc_name}{WHITE}: ({npc_name} said nothing)')


@staticmethod
def npc_speak(name: str, dialog: Iterable):
    iterator = iter(dialog)
    npc_name = format_name(name)
    sentence = next(iterator)
    if isinstance(sentence, tuple):
        yellow(f'[NPC] {npc_name}{WHITE}: {choice(sentence)}')
    else:
        yellow(f'[NPC] {npc_name}{WHITE}: {sentence}')
    for sentence in iterator:
        sleep(1.5)
        if isinstance(sentence, tuple):
            yellow(f'[NPC] {npc_name}{WHITE}: {choice(sentence)}')
        else:
            yellow(f'[NPC] {npc_name}{WHITE}: {sentence}')


display_functions = {
    name: globals()[name] for name in __all__
}
