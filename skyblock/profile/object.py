from decimal import Decimal
from math import ceil, radians, tan
from os import get_terminal_size
from random import choice, choices
from re import fullmatch
from time import sleep, time
from typing import Dict, Iterable, List, Optional, Tuple

from ..constant.color import (
    RARITY_COLORS, BOLD, DARK_AQUA,
    GOLD, GRAY, BLUE, GREEN, AQUA, RED, YELLOW, WHITE,
)
from ..constant.doc import profile_doc
from ..constant.main import INTEREST_TABLE, SELL_PRICE, SKILL_EXP
from ..constant.mob import ENDER_SLAYER_EFFECTIVE
from ..constant.util import Number
from ..function.io import dark_aqua, gray, red, green, yellow, aqua, white
from ..function.math import (
    calc_exp, calc_skill_exp, calc_skill_exp_info, random_int,
)
from ..function.util import (
    backupable, display_int, display_number, display_name, generate_help,
    get, includes, random_amount, random_bool, roman, shorten_number,
)
from ..item.item import COLLECTION_ITEMS, get_item
from ..item.mob import get_mob
from ..item.object import (
    ItemType, Item, Empty, Pickaxe, Axe,
    Bow, Sword, Armor, Pet, Mineral, Tree, Mob,
)
from ..item.resource import get_resource
from ..map.island import ISLANDS
from ..map.object import Npc, calc_dist, path_find

from .wrapper import profile_type

__all__ = ['Profile']


profile_help = generate_help(profile_doc)


@profile_type
class Profile:
    name: str
    last_update: int = 0

    bank_level: str = 'starter'
    balance: Number = 0.0
    purse: Number = 0.0

    experience: Number = 0

    island: str = 'hub'
    region: str = 'village'

    base_health: int = 100
    base_defense: int = 0
    base_strength: int = 0
    base_speed: int = 100
    base_crit_damage: int = 50
    base_intelligence: int = 100
    base_sea_creature_chance: int = 20

    skill_xp_alchemy: float = 0.0
    skill_xp_carpentry: float = 0.0
    skill_xp_catacombs: float = 0.0
    skill_xp_combat: float = 0.0
    skill_xp_enchanting: float = 0.0
    skill_xp_farming: float = 0.0
    skill_xp_fishing: float = 0.0
    skill_xp_foraging: float = 0.0
    skill_xp_mining: float = 0.0
    skill_xp_taming: float = 0.0
    collection: Dict[str, int] = {}

    crafted_minions: List[str] = []

    death_count: int = 0

    armor: List[Item] = [Empty() for _ in range(4)]
    pets: List[Item] = []
    ender_chest: List[Item] = []
    inventory: List[Item] = [Empty() for _ in range(36)]
    potion_bag: List[Item] = []
    quiver: List[Item] = []
    stash: List[Item] = []
    talisman_bag: List[Item] = []
    wardrobe: List[Item] = []
    wardrobe_slot: Optional[int] = None

    npc_talked: List[str] = []

    def die(self, /):
        lost_coins = self.purse / 2
        self.purse -= lost_coins
        self.death_count += 1
        red(f'You died and lost {display_number(lost_coins)} coins!')
        self.region = get(ISLANDS, self.island).spawn

    def put_stash(self, item: ItemType, count: int, /):
        if isinstance(item, Item):
            for index, slot in enumerate(self.stash):
                if not isinstance(slot, Item):
                    continue
                if slot.name != item.name or slot.rarity != item.rarity:
                    continue
                self.stash[index].count += count
                break
        else:
            for i in range(count):
                self.stash.append(item)

        materials = sum(getattr(item, 'count', 1) for item in self.stash)
        items = 0
        for item in self.stash:
            stack_count = getattr(get_item(item.name), 'count', 1)
            items += ceil(getattr(item, 'count', 1) / stack_count)
        yellow(f'You have {GREEN}{display_int(materials)} materials{YELLOW}'
               f' totalling {AQUA}{display_int(items)} items{YELLOW}'
               f' stashed away!!')
        yellow(f'Use {GOLD}`pickupstash`{YELLOW} to pick it all up!')

    def recieve(self, item: ItemType, count: int, /, *, log: bool = True):
        item = item.copy()
        item_object = get_item(item.name)
        stack_count = getattr(item_object, 'count', 1)

        for index, slot in enumerate(self.inventory):
            if isinstance(slot, Empty):
                if hasattr(item_object, 'count'):
                    delta = min(count, stack_count)
                    item.count = delta
                else:
                    delta = 1
                self.inventory[index] = item
                count -= delta
            elif not isinstance(slot, Item) or not isinstance(item, Item):
                continue
            elif slot.name != item.name or slot.rarity != item.rarity:
                continue
            else:
                delta = min(count, item_object.count - slot.count)
                count -= delta
                self.inventory[index].count += delta
            if count == 0:
                break
        else:
            self.put_stash(item, count)
            return

        if log:
            if count != 0:
                count_str = f' {GRAY}x {display_int(count)}'
            else:
                count_str = ''
            gray(f'+ {item.display()}{count_str}')

    def pickupstash(self, /):
        if len(self.stash) == 0:
            red('Your stash is already empty!')
            return
        stash = [item.copy() for item in self.stash]
        self.stash.clear()
        for item in stash:
            self.recieve(item)

    def add_exp(self, amount: Number, /):
        original_lvl = calc_exp(self.experience)
        self.experience += amount
        current_lvl = calc_exp(self.experience)
        if current_lvl > original_lvl:
            green(f'Reached XP level {current_lvl}.')

    def add_skill_exp(self, name: str, amount: Number, /):
        if not hasattr(self, f'skill_xp_{name}'):
            red(f'Skill not found: {name}')
            return
        exp = getattr(self, f'skill_xp_{name}')
        original_lvl = calc_skill_exp(name, exp)
        exp += amount
        setattr(self, f'skill_xp_{name}', exp)
        current_lvl = calc_skill_exp(name, exp)
        if current_lvl > original_lvl:
            coins_reward = 0
            for lvl in range(original_lvl + 1, current_lvl + 1):
                if name != 'catacombs':
                    coins_reward += SKILL_EXP[lvl][3]

            self.purse += coins_reward

            width, _ = get_terminal_size()
            width = ceil(width * 0.85)

            dark_aqua(f"{BOLD}{'':-^{width}}")
            original = roman(original_lvl) if original_lvl != 0 else '0'
            aqua(f' {BOLD}SKILL LEVEL UP {DARK_AQUA}{display_name(name)} '
                 f'{GRAY}{original}->'
                 f'{DARK_AQUA}{roman(current_lvl)}')
            if name != 'catacombs':
                green(f' {BOLD}REWARDS')
                gray(f'  +{GOLD}{display_int(coins_reward)}{GRAY} Coins')
            dark_aqua(f"{BOLD}{'':-^{width}}")

    def look(self):
        island = get(ISLANDS, self.island)
        if island is None:
            yellow('Invalid island. Using hub as default.')
            island = get(ISLANDS, 'hub')
        region = get(island.regions, self.region)
        if region is None:
            yellow('Invalid region. Using island spawn as default.')
            region = get(island.regions, island.spawn)

        gray('Location:')
        gray(f"  You're at {AQUA}{region}{GRAY} of {AQUA}{island}{GRAY}.")
        gray('\nNearby places:')
        for conn in island.conns:
            if region not in conn:
                continue
            other = conn[0] if conn[1] == region else conn[1]
            sx, sz, ox, oz = region.x, region.z, other.x, other.z
            dx, dz = ox - sx, oz - sz
            direc = ''
            if dx == 0:
                direc = 'South' if dz > 0 else 'North'
            elif dz == 0:
                direc = 'East' if dx > 0 else 'West'
            else:
                if dx / dz < tan(radians(60)):
                    direc += 'South' if dz > 0 else 'North'
                if dz / dx < tan(radians(60)):
                    direc += 'East' if dx > 0 else 'West'
            gray(f'  {AQUA}{other.name}{GRAY} on the {AQUA}{direc}{GRAY}.')

        if len(region.resources) > 0:
            gray('\nResources:')
            for resource in region.resources:
                gray(f'  {GREEN}{resource.name}{GRAY} ({resource.type()})')

        if len(region.mobs) > 0:
            gray('\nMobs:')
            for mob in region.mobs:
                green(f'  {GRAY}Lv{mob.level} {RED}{display_name(mob.name)}'
                      f' {GREEN}{shorten_number(mob.health)}{RED}♥{GREEN}.')

        if len(region.npcs) > 0:
            gray('\nNPCs:')
            for npc in region.npcs:
                gray(f'  {GREEN}{npc}{GRAY} ({npc.name})')

        if region.portal is not None:
            gray(f'\nPortal to {AQUA}{display_name(region.portal)}{GRAY}.')

    def display_skill(self, name, end=True):
        width, _ = get_terminal_size()
        width = ceil(width * 0.85)

        yellow(f"{BOLD}{'':-^{width}}")

        exp = getattr(self, f'skill_xp_{name}')
        lvl, exp_left, exp_to_next, coins = calc_skill_exp_info(name, exp)
        if lvl == 0:
            green(display_name(name))
        else:
            green(f'{display_name(name)} {roman(lvl)}')

        if exp_left < exp_to_next:
            perc = int(exp_left / exp_to_next * 100)
            gray(f'Progress to level {roman(lvl + 1)}: {YELLOW}{perc}%')

        bar = min(int(exp_left / exp_to_next * 20), 20)
        left, right = '-' * bar, '-' * (20 - bar)
        green(f'{left}{GRAY}{right} {YELLOW}{display_int(exp_left)}'
              f'{GOLD}/{YELLOW}{display_int(exp_to_next)}')

        if exp_left < exp_to_next and name != 'catacombs':
            gray(f'\nLevel {roman(lvl + 1)} Rewards:')
            gray(f' +{GOLD}{display_int(coins)}{GRAY} Coins')

        if end:
            yellow(f"{BOLD}{'':-^{width}}")

    def display_skills(self):
        width, _ = get_terminal_size()
        width = ceil(width * 0.85)

        for skill in {'farming', 'mining', 'combat', 'foraging', 'fishing',
                      'enchanting', 'alchemy', 'taming', 'catacombs'}:
            self.display_skill(skill, end=False)

        yellow(f"{BOLD}{'':-^{width}}")

    def money(self):
        if self.region != 'bank':
            if self.purse < 1000:
                shortened_purse = ''
            else:
                shortened_purse = f' {GRAY}({shorten_number(self.purse)})'

            white(f'Purse: {GOLD}{display_number(self.purse)} Coins'
                  f'{shortened_purse}')
            return
        if self.balance < 1000:
            shortened_balance = ''
        else:
            shortened_balance = f' {GRAY}({shorten_number(self.balance)})'

        if self.purse < 1000:
            shortened_purse = ''
        else:
            shortened_purse = f' {GRAY}({shorten_number(self.purse)})'

        green('Bank Account')
        gray(f'Balance: {GOLD}{display_number(self.balance)} Coins'
             f'{shortened_balance}')
        white(f'Purse: {GOLD}{display_number(self.purse)} Coins'
              f'{shortened_purse}')
        gray(f'Bank Level: {GREEN}{display_name(self.bank_level)}')

    @backupable
    def talkto_npc(self, npc: Npc, /) -> Optional[str]:
        if npc.name not in self.npc_talked:
            if npc.init_dialog is not None:
                self.npc_talk(npc.name, npc.init_dialog)
            elif npc.dialog is not None:
                self.npc_talk(npc.name, choice(npc.dialog))
            else:
                sentence = choices((
                    f"{npc} doesn't seem to want to talk to you.",
                    f"{npc} has got nothing to say to you.",
                    f"{npc} is in his peace.",
                    f"{npc} seems tired and sleepy.",
                    f"{npc} stared at you and didn't talk.",
                    f"{npc} smiled mysteriously.",
                    f"{npc} made a strange noise.",
                    f"{npc} spoke a strange language you've never heard before.",
                ), (20, 25, 20, 18, 10, 4, 2, 1))[0]
                yellow(f'[NPC] {display_name(npc.name)}'
                       f'{WHITE}: ({sentence})')
            self.npc_talked.append(npc.name)
            return
        if npc.trades is not None:
            gray(f"{npc}'s shop:")
            digits = len(f'{len(npc.trades)}')
            for index, (price, item) in enumerate(npc.trades):
                gray(f'  {(index + 1):>{digits}} {item.display()}{GRAY} for '
                     f'{GOLD}{display_number(price)} coins{GRAY}.')
            return npc.name
        elif npc.dialog is not None:
            self.npc_talk(choice(npc.dialog))
        else:
            sentence = choices((
                f"{npc} doesn't seem to want to talk to you.",
                f"{npc} has got nothing to say to you.",
                f"{npc} is in his peace.",
                f"{npc} seems tired and sleepy.",
                f"{npc} stared at you and didn't talk.",
                f"{npc} smiled mysteriously.",
                f"{npc} made a strange noise.",
                f"{npc} spoke a strange language you've never heard before.",
            ), (20, 25, 20, 18, 10, 4, 2, 1))[0]
            yellow(f'[NPC] {display_name(npc.name)}{WHITE}: ({sentence})')

    @backupable
    def goto(self, dest: str, /):
        island = get(ISLANDS, self.island)
        region = get(island.regions, self.region)

        if not includes(island.regions, dest):
            red(f'Region not found: {dest!r}')
            return
        if region.name == dest:
            yellow(f'Already at region: {dest!r}')
            return
        path, accum_dist = path_find(region, get(island.regions, dest),
                                     island.conns, island.dists)

        route = ' -> '.join(f'{region}' for region in path)
        aqua(f'Route: {route} ({float(accum_dist):.2f}m)')
        for target in path[1:]:
            if target.skill_req is not None:
                name, level = target.skill_req
                skill_exp = getattr(self, f'skill_xp_{name}')
                exp_lvl = calc_skill_exp(name, skill_exp)
                if exp_lvl < level:
                    red(f'Cannot warp to {dest}!')
                    red(f'Requires {name.capitalize()} level {roman(level)}')
                    return

            dist = calc_dist(region, target)
            time_cost = float(dist) / (5 * (self.base_speed / 100))
            green(f'Going from {region} to {target}...')
            gray(f'(time cost: {time_cost:.2f}s)')
            sleep(time_cost)
            self.region = target.name
            region = get(island.regions, target.name)

    @backupable
    def warp(self, dest: str, /):
        island = get(ISLANDS, self.island)
        region = get(island.regions, self.region)

        if not includes(ISLANDS, dest):
            red(f'Island not found: {dest!r}')
            return
        if dest == self.island:
            yellow(f'Already at island: {dest!r}')
            return

        if region.portal != dest:
            yellow(f'Cannot warp to {dest}')
            return

        last = self.island
        island = get(ISLANDS, dest)

        if island.skill_req is not None:
            name, level = island.skill_req
            skill_exp = getattr(self, f'skill_xp_{name}')
            exp_lvl = calc_skill_exp(name, skill_exp)
            if exp_lvl < level:
                red(f'Cannot warp to {dest}!')
                red(f'Requires {name.capitalize()} level {roman(level)}')
                return

        self.island = dest
        region = get(island.regions, portal=last)
        self.region = region.name
        gray(f'Warped to {AQUA}{region}{GRAY} of {AQUA}{island}{GRAY}.')

    def ls(self):
        length = len(self.inventory)
        if length == 0:
            gray('Your inventory is empty.')
            return

        digits = len(f'{length}')
        index = 0
        while index < length:
            item = self.inventory[index]
            if isinstance(item, Empty):
                while index < length:
                    if not isinstance(self.inventory[index], Empty):
                        break
                    index += 1
                continue
            gray(f'{(index + 1):>{digits * 2 + 1}} {item.display()}')
            index += 1

    def info(self, index: int, /):
        item = self.inventory[index]

        if isinstance(item, Empty):
            gray('Empty')
            return

        cata_lvl = calc_skill_exp('catacombs', self.skill_xp_catacombs)

        width, _ = get_terminal_size()
        width = ceil(width * 0.85)
        yellow(f"{BOLD}{'':-^{width}}")
        gray(item.info(cata_lvl=cata_lvl))
        yellow(f"{BOLD}{'':-^{width}}")

    def collect(self, name: str, amount: int, /):
        if name not in self.collection:
            self.collection[name] = 0
        self.collection[name] += amount

    def buy(self, trade: Tuple[Number, ItemType], amount: int):
        price = trade[0] * amount
        if self.purse < price:
            red('Not enough coins!')
            return

        item = trade[1]

        self.purse -= price
        self.recieve(item, amount)

        green(f"You bought {item.display()}{GREEN} for "
              f"{GOLD}{shorten_number(price)} Coins{GREEN}!")

    def sell(self, index: int, /):
        island = get(ISLANDS, self.island)
        region = get(island.regions, self.region)

        if len(region.npcs) == 0:
            red('No NPCs around to sell the item.')
            return

        item = self.inventory[index]
        if item.name not in SELL_PRICE:
            red(f"Can't sell {item.display()}.")
            return

        delta = SELL_PRICE[item.name] * getattr(item, 'count', 1)
        self.purse += delta
        green(f"You sold {item.display()}{GREEN} for "
              f"{GOLD}{shorten_number(delta)} Coins{GREEN}!")
        self.inventory[index] = Empty()

    def get(self, name: str, tool_index: Optional[int], amount: int, /):
        resource = get_resource(name)
        tool = Empty() if tool_index is None else self.inventory[tool_index]

        if not isinstance(tool, (Empty, Axe, Pickaxe)):
            tool = Empty()

        enchantments = getattr(tool, 'enchantments', {})

        if isinstance(resource, Mineral):
            breaking_power = getattr(tool, 'breaking_power', 0)
            mining_speed = getattr(tool, 'mining_speed', 50)
            mining_speed = tool.mining_speed
            if 'efficiency' in enchantments:
                mining_speed += 10 + 20 * enchantments['efficiency']

            if resource.breaking_power > breaking_power:
                red(f'Insufficient breaking power for {resource.name}.')
                return

            time_cost = 30 * resource.hardness / mining_speed

            mining_lvl = calc_skill_exp('mining', self.skill_xp_mining)

            mining_fortune = (1 + 0.1 * tool.enchantments.get('fortune', 0)
                              + 0.04 * mining_lvl)
            experience = 1 + 0.125 * tool.enchantments.get('experience', 0)
            drop_item = resource.drop
            default_amount = resource.amount

            last_cp = Decimal()
            cp_step = Decimal('0.1')
            is_collection = includes(COLLECTION_ITEMS, drop_item)
            for count in range(1, amount + 1):
                sleep(time_cost)
                drop_pool = random_int(mining_fortune)
                self.recieve(Item(drop_item), default_amount * drop_pool)
                if is_collection:
                    self.collect(drop_item, default_amount * drop_pool)

                self.add_exp(resource.exp * random_int(experience))
                self.add_skill_exp('mining', resource.mining_exp)
                if count >= (last_cp + cp_step) * amount:
                    while count >= (last_cp + cp_step) * amount:
                        last_cp += cp_step
                    gray(f'{count} / {amount} ({(last_cp * 100):.0f}%) done')

        elif isinstance(resource, Tree):
            if isinstance(tool, Axe):
                tool_speed = tool.tool_speed
                if 'efficiency' in tool.enchantments:
                    tool_speed += tool.enchantments['efficiency'] ** 2 + 1
                time_cost = 1.5 * resource.hardness / tool_speed
            else:
                tool_speed = 1
                time_cost = 5 * resource.hardness / tool_speed
            time_cost = ceil(time_cost * 20) / 20

            foraging_lvl = calc_skill_exp('foraging', self.skill_xp_foraging)
            foraging_fortune = 1 + 0.04 * foraging_lvl

            drop_item = resource.drop

            last_cp = Decimal()
            cp_step = Decimal('0.1')
            is_collection = includes(COLLECTION_ITEMS, drop_item)
            for count in range(1, amount + 1):
                sleep(time_cost)
                drop_pool = random_int(foraging_fortune)
                self.recieve(Item(drop_item), drop_pool)
                if is_collection:
                    self.collect(drop_item, drop_pool)

                self.add_skill_exp('foraging', resource.foraging_exp)
                if count >= (last_cp + cp_step) * amount:
                    while count >= (last_cp + cp_step) * amount:
                        last_cp += cp_step
                    gray(f'{count} / {amount} ({(last_cp * 100):.0f}%) done')

        else:
            red('Unknown resource type.')

    def slay(self, name: str, weapon_index: Optional[int], amount: int, /):
        mob = get_mob(name)
        weapon = (Empty() if weapon_index is None
                  else self.inventory[weapon_index])

        if not isinstance(weapon, (Empty, Bow, Sword)):
            weapon = Empty()

        if not isinstance(mob, Mob):
            red('Unknown mob type.')
            return

        health = self.base_health
        defense = self.base_defense
        # true_defense = 0
        strength = self.base_strength
        speed = self.base_speed
        crit_chance = 30
        crit_damage = self.base_crit_damage
        attack_speed = self.base_attack_speed
        # intelligence = self.base_intelligence
        magic_find = self.base_magic_find
        ferocity = 0

        thorns = 0

        combat_lvl = calc_skill_exp('combat', self.skill_xp_combat)
        farming_lvl = calc_skill_exp('farming', self.skill_xp_farming)
        foraging_lvl = calc_skill_exp('foraging', self.skill_xp_foraging)
        mining_lvl = calc_skill_exp('mining', self.skill_xp_mining)

        enchantments = getattr(weapon, 'enchantments', {})

        if isinstance(weapon, (Bow, Sword)):
            damage = weapon.damage + 5 + weapon.hot_potato
            strength += weapon.hot_potato
            crit_chance += weapon.crit_chance
            crit_damage += weapon.crit_damage
            ferocity += weapon.ferocity

            damage *= 1 + 0.08 * enchantments.get('power', 0)
            damage *= 1 + 0.05 * enchantments.get('sharpness', 0)
            if name in ENDER_SLAYER_EFFECTIVE:
                damage *= 1 + 0.12 * enchantments.get('ender_slayer', 0)
            crit_damage += 10 * enchantments.get('critical', 0)
            ferocity += enchantments.get('vicious', 0)
        else:
            damage = 5

        rejuvenate = 0

        for piece in self.armor:
            if not isinstance(piece, Armor):
                continue
            strength += piece.strength
            health += piece.health
            defense += piece.health
            speed += piece.health

            # intelligence += ench.get('big_brain', 0) * 5
            ench = getattr(piece, 'enchantments', {})
            health += ench.get('growth', 0) * 15
            rejuvenate += ench.get('rejuvenate', 0) * 2
            defense += ench.get('protection', 0) * 8
            thorns += ench.get('thorns', 0) * 3
            # true_defense += ench.get('true_protection', 0) * 5

        strength += min(foraging_lvl, 14) * 1
        strength += max(min(foraging_lvl - 14, 36), 0) * 2
        crit_chance += combat_lvl * 0.5
        defense += min(mining_lvl, 14) * 1
        defense += max(min(mining_lvl - 14, 46), 0) * 2
        health += min(foraging_lvl, 14) * 2
        health += max(min(farming_lvl - 14, 5), 0) * 3
        health += max(min(farming_lvl - 19, 6), 0) * 4
        health += max(min(farming_lvl - 25, 35), 0) * 5

        damage *= 1 + (strength / 100)
        damage *= 1 + 0.04 * combat_lvl

        time_cost = 2 / (speed / 100)

        execute = 0.2 * enchantments.get('execute', 0)
        experience = 1 + 0.125 * enchantments.get('experience', 0)
        first_strike = 1 + 0.25 * enchantments.get('first_strike', 0)
        giant_killer = enchantments.get('giant_killer', 0)
        life_steal = 0.5 * enchantments.get('life_steal', 0)
        if isinstance(weapon, Bow):
            looting = 1 + 0.15 * enchantments.get('chance', 0)
        elif isinstance(weapon, Sword):
            looting = 1 + 0.15 * enchantments.get('looting', 0)
        else:
            looting = 1
        luck = 1 + 0.05 * enchantments.get('luck', 0)
        overload = enchantments.get('overload', 0)
        prosecute = 0.1 * enchantments.get('prosecute', 0)
        scavenger = 0.3 * enchantments.get('scavenger', 0)
        if 'syphon' in enchantments:
            syphon = 0.1 + 0.1 * enchantments['syphon']
        else:
            syphon = 0
        triple_strike = 1 + 0.10 * enchantments.get('triple_strike', 0)
        vampirism = enchantments.get('vampirism', 0)

        crit_chance += overload
        crit_damage += overload

        hp = health

        last_cp = Decimal()
        cp_step = Decimal('0.1')
        is_collection = {
            row[0].name: includes(COLLECTION_ITEMS, row[0].name)
            for row in mob.drops
        }
        green(f'Slaying {GRAY}Lv{mob.level} {RED}{display_name(mob.name)}'
              f' {GREEN}{shorten_number(mob.health)}{RED}♥{GREEN}.')
        for count in range(1, amount + 1):
            sleep(time_cost)
            healed = round((time_cost // 2) * (1.5 + health / 100), 1)
            healed *= 1 + (rejuvenate / 100)
            healed = max(health - hp, healed)
            if healed != 0:
                hp += healed
                gray(f'You healed for {GREEN}{shorten_number(healed)}'
                     f'{RED}♥{GRAY}.')

            mob_hp = mob.health
            while True:
                strike_count = 0

                for _ in range(random_int(1 + ferocity / 100)):
                    crit = ''
                    if random_bool(crit_chance / 100):
                        damage_delt = damage * (1 + crit_damage / 100)
                        if crit_chance >= 100 and random_bool(overload * 0.1):
                            damage_delt *= 1.1
                        crit = 'crit '
                    else:
                        damage_delt = damage

                    damage_delt *= (
                        1 + giant_killer * (min(0.1 * (mob_hp - hp), 5) / 100)
                    )

                    if strike_count == 0:
                        damage_delt *= first_strike
                    if strike_count < 3:
                        damage_delt *= triple_strike

                    damage_delt *= 1 + min(prosecute * (mob_hp / mob.health),
                                           0.35)
                    damage_delt += (execute / 100) * (mob.health - mob_hp)

                    mob_hp -= damage_delt
                    gray(f"You delt {YELLOW}{shorten_number(damage_delt)}{GRAY}"
                         f" {crit}damage to the {display_name(mob.name)}!\n")

                    if life_steal != 0:
                        delta = min(health - hp, life_steal * health)
                        hp += delta

                        gray(f"Your {BLUE}Life Steal{GRAY} "
                             f"enchantment healed you for {AQUA}"
                             f"{shorten_number(delta)}{RED}♥{GRAY}!\n")

                    if syphon != 0:
                        delta = min(health - hp,
                                    syphon * health * (crit_damage // 100))
                        if delta != 0:
                            hp += delta

                            gray(f"Your {BLUE}Syphon{GRAY} "
                                 f"enchantment healed you for {AQUA}"
                                 f"{shorten_number(delta)}{RED}♥{GRAY}!\n")

                if mob_hp <= 0:
                    a_an = 'an' if mob.name[0] in 'aeiou' else 'a'
                    green(
                        f"You've killed {a_an} {display_name(mob.name)}!\n\n")
                    break

                damage_recieved = mob.damage * (1 + defense / 100)
                hp -= damage_recieved
                gray(f"You recieved {YELLOW}"
                     f"{shorten_number(damage_recieved)}{GRAY}"
                     f" damage from the {display_name(mob.name)}!\n")

                if hp <= 0:
                    self.die()
                    return

                if random_bool(0.5) and thorns != 0:
                    thorns_damage = (thorns / 100) * damage_recieved
                    mob_hp -= thorns_damage
                    gray(f"Your {BLUE}Thorns{GRAY} enchantment delt {YELLOW}"
                         f"{shorten_number(damage_delt)}{GRAY}"
                         f" {crit}damage to the {display_name(mob.name)}!\n")

                    if mob_hp <= 0:
                        a_an = 'an' if mob.name[0] in 'aeiou' else 'a'
                        green(f"You've killed {a_an} "
                              f"{display_name(mob.name)}!\n")
                        break

                gray(f'Your HP: {AQUA}{shorten_number(hp)}{RED}♥')
                gray(f"{display_name(mob.name)}'s HP: "
                     f"{AQUA}{shorten_number(hp)}{RED}♥\n\n")

                strike_count += 1

            if vampirism != 0 and hp != health:
                delta = (health - hp) * (vampirism / 100)
                hp += delta

                gray(f"Your {BLUE}Vampirism{GRAY} enchantment healed you for "
                     f"{AQUA}{shorten_number(delta)}{RED}♥{GRAY}!\n")

            self.purse += mob.coins + scavenger
            self.add_exp(mob.exp * random_int(experience))
            self.add_skill_exp('combat', mob.combat_xp)

            for item, count, rarity, drop_chance in mob.drops:
                drop_chance *= looting
                drop_chance *= 1 + magic_find / 100
                if isinstance(item, Armor):
                    drop_chance *= luck

                if not random_bool(drop_chance):
                    continue

                loot = item.copy()

                self.recieve(loot, random_amount(count))

                if is_collection[loot.name]:
                    self.collect(loot.name, loot.count)

                if rarity not in {'common', 'uncommon'}:
                    rarity_str = rarity.upper()
                    white(f'{RARITY_COLORS[rarity]}{rarity_str} DROP! '
                          f'({item.display()}{WHITE})')

            if count >= (last_cp + cp_step) * amount:
                while count >= (last_cp + cp_step) * amount:
                    last_cp += cp_step
                gray(f'{count} / {amount} ({(last_cp * 100):.0f}%) killed')

    @staticmethod
    def npc_talk(name: str, dialog: Iterable):
        iterator = iter(dialog)
        yellow(f'[NPC] {display_name(name)}{WHITE}: {next(iterator)}')
        for sentence in iterator:
            sleep(1.5)
            yellow(f'[NPC] {display_name(name)}{WHITE}: {sentence}')

    def update(self):
        now = int(time())
        last = now if self.last_update == 0 else self.last_update
        # dt = now - last

        last_cp = last // (31 * 3600)
        now_cp = now // (31 * 3600)
        if now_cp > last_cp:
            interest = 0
            if self.bank_level not in INTEREST_TABLE:
                red(f'Invalid bank level: {self.bank_level!r}.')
                return
            table = INTEREST_TABLE[self.bank_level]
            for start, end, ratio in table:
                if self.balance > start:
                    interest += ratio * (min(self.balance, end) - start)

            interest *= now_cp - last_cp
            self.balance += interest
            green(f"Since you've been away you earned "
                  f"{GOLD}{display_number(interest)} coins{GREEN} "
                  f"as interest in your personal bank account!")

        self.last_update = now

    def mainloop(self):
        last_shop: Optional[str] = None

        while True:
            island = get(ISLANDS, self.island)
            if island is None:
                yellow('Invalid island. Using hub as default.')
                island = get(ISLANDS, 'hub')
            region = get(island.regions, self.region)
            if region is None:
                yellow('Invalid region. Using island spawn as default.')
                region = get(island.regions, island.spawn)

            if last_shop is not None:
                if not includes(region.npcs, last_shop):
                    last_shop = None

            self.update()

            words = input(':> ').split()

            if len(words) == 0:
                continue

            elif words[0] in {'exit', 'quit'}:
                if len(words) != 1:
                    red(f'Invalid usage of command {words[0]!r}.')
                    continue

                self.dump()
                green('Saved!')
                break

            elif words[0] == 'deathcount':
                yellow(f'Death Counts: {BLUE}'
                       f'{display_number(self.death_count)}')

            elif words[0] in {'deposit', 'withdraw'}:
                if len(words) != 2:
                    red(f'Invalid usage of command {words[0]!r}.')
                    continue

                if self.region != 'bank':
                    red('You can only do that while you are at the bank!')
                    continue

                coins_str = words[1]
                if not fullmatch(r'\d+(\.\d{1,2})?[TtBbMmKk]?', coins_str):
                    red('Invalid amount of coins.')
                    continue
                if coins_str[-1].lower() in 'kmbt':
                    mult = 1000 ** ('kmbt'.index(coins_str[-1].lower()) + 1)
                    coins_str = coins_str[:-1]
                else:
                    mult = 1
                coins = eval(coins_str) * mult

                if words[0] == 'deposit':
                    if self.purse == 0:
                        red("You don't have any coins!")
                        continue
                    if self.purse < coins:
                        coins = self.purse

                    self.purse -= coins
                    self.balance += coins

                    green(f'You have deposited {GOLD}'
                          f'{display_number(coins)} Coins{GREEN}! '
                          f'You now have {GOLD}'
                          f'{display_number(self.balance)} Coins{GREEN} '
                          'in your account!')
                else:
                    if self.balance == 0:
                        red("You don't have any coins in your bank account!")
                        continue
                    if self.balance < coins:
                        coins = self.balance

                    self.balance -= coins
                    self.purse += coins

                    green(f'You have withdrawn {GOLD}'
                          f'{display_number(coins)} Coins{GREEN}! '
                          f'You now have {GOLD}'
                          f'{display_number(self.balance)} Coins{GREEN} '
                          'in your account!')

            elif words[0] == 'help':
                if len(words) == 1:
                    aqua(profile_doc)
                else:
                    phrase = ' '.join(words[1:])
                    if phrase in profile_help:
                        usage, description = profile_help[phrase]
                        aqua(usage)
                        aqua(description)
                    else:
                        red(f'Command not found: {phrase!r}.')

            elif words[0] == 'get':
                if len(words) < 2 or len(words) > 4:
                    red(f'Invalid usage of command {words[0]!r}.')
                    continue

                name = words[1]
                if get_resource(name) is None:
                    red(f'Resource not found: {name!r}')
                    continue
                if get(region.resources, name) is None:
                    red(f'Resource not avaliable at {region}: {name!r}')
                    continue

                tool_index = None

                if len(words) >= 3:
                    tool_str = words[2]
                    if not fullmatch(r'\d+', tool_str):
                        red(f'Invalid number for item index: {tool_str}')
                        continue
                    tool_index = int(tool_str)
                    if tool_index <= 0 or tool_index > len(self.inventory):
                        red(f'Item index out of bound: {tool_index}')
                        continue
                    tool_index -= 1
                    tool_item = self.inventory[tool_index]
                    if not isinstance(tool_item, (Empty, Pickaxe, Axe)):
                        yellow(f'{tool_item.name} item is not tool.\n'
                               f'Using barehand by default.')
                        tool_index = None

                amount = None

                if len(words) == 4:
                    amount_str = words[3]
                    if not fullmatch(r'\d+', amount_str):
                        red(f'Invalid number for amount: {amount_str}')
                        continue
                    amount = int(amount_str)
                    if amount == 0:
                        red(f'Amount must be a positive integer.')
                        continue

                self.get(name, tool_index, amount)

            elif words[0] == 'slay':
                if len(words) < 2 or len(words) > 4:
                    red(f'Invalid usage of command {words[0]!r}.')
                    continue

                name = words[1]
                if get_mob(name) is None:
                    red(f'Mob not found: {name!r}')
                    continue
                if get(region.mobs, name) is None:
                    red(f'Mob not avaliable at {region}: {name!r}')
                    continue

                weapon_index = None

                if len(words) >= 3:
                    weapon_str = words[2]
                    if not fullmatch(r'\d+', weapon_str):
                        red(f'Invalid number for item index: {weapon_str}')
                        continue
                    weapon_index = int(weapon_str)
                    if weapon_index <= 0 or weapon_index > len(self.inventory):
                        red(f'Item index out of bound: {weapon_index}')
                        continue
                    weapon_index -= 1
                    tool_item = self.inventory[weapon_index]
                    if not isinstance(tool_item, (Empty, Bow, Sword)):
                        yellow(f'{tool_item.name} item is not weapon.\n'
                               f'Using barehand by default.')
                        weapon_index = None

                amount = None

                if len(words) == 4:
                    amount_str = words[3]
                    if not fullmatch(r'\d+', amount_str):
                        red(f'Invalid number for amount: {amount_str}')
                        continue
                    amount = int(amount_str)
                    if amount == 0:
                        red(f'Amount must be a positive integer.')
                        continue

                self.slay(name, weapon_index, amount)

            elif words[0] == 'goto':
                if len(words) != 2:
                    red(f'Invalid usage of command {words[0]!r}.')
                    continue

                self.goto(words[1])

            elif words[0] == 'warp':
                if len(words) != 2:
                    red(f'Invalid usage of command {words[0]!r}.')
                    continue

                self.warp(words[1])

            elif words[0] in {'inv', 'inventory', 'list', 'ls'}:
                if len(words) != 1:
                    red(f'Invalid usage of command {words[0]!r}.')
                    continue

                self.ls()

            elif words[0] in {'info', 'information'}:
                if len(words) != 2:
                    red(f'Invalid usage of command {words[0]!r}.')
                    continue

                index_str = words[1]
                if not fullmatch(r'\d+', index_str):
                    red(f'Invalid number for item index: {index_str}')
                    continue
                item_index = int(index_str)
                if item_index <= 0 or item_index > len(self.inventory):
                    red(f'Item index out of bound: {item_index}')
                    continue
                item_index -= 1

                self.info(item_index)

            elif words[0] == 'look':
                if len(words) != 1:
                    red(f'Invalid usage of command {words[0]!r}.')
                    continue

                self.look()

            elif words[0] == 'skills':
                if len(words) > 2:
                    red(f'Invalid usage of command {words[0]!r}.')
                    continue

                if len(words) == 1:
                    self.display_skills()
                    continue

                skill = words[1]
                if skill not in {'farming', 'mining', 'combat', 'foraging',
                                 'fishing', 'enchanting', 'alchemy', 'taming',
                                 'catacombs'}:
                    red(f'Invalid skill: {skill!r}')
                    continue

                self.display_skill(skill)

            elif words[0] == 'money':
                if len(words) != 1:
                    red(f'Invalid usage of command {words[0]!r}.')
                    continue

                self.money()

            elif words[0] == 'save':
                if len(words) != 1:
                    red(f'Invalid usage of command {words[0]!r}.')
                    continue

                self.dump()
                green('Saved!')

            elif words[0] == 'merge':
                if len(words) != 3:
                    red(f'Invalid usage of command {words[0]!r}.')
                    continue

                index_1_str = words[1]
                if not fullmatch(r'\d+', index_1_str):
                    red(f'Invalid number for item index: {index_1_str}')
                    continue
                index_1 = int(index_1_str)
                if index_1 <= 0 or index_1 > len(self.inventory):
                    red(f'Item index out of bound: {index_1}')
                    continue
                index_1 -= 1

                index_2_str = words[2]
                if not fullmatch(r'\d+', index_2_str):
                    red(f'Invalid number for item index: {index_2_str}')
                    continue
                index_2 = int(index_2_str)
                if index_2 <= 0 or index_2 > len(self.inventory):
                    red(f'Item index out of bound: {index_2}')
                    continue
                index_2 -= 1

                item_from = self.inventory[index_1]
                item_to = self.inventory[index_2]
                if not hasattr(item_from, 'count') or not hasattr(item_to, 'count'):
                    red('Cannot merge unstackable items.')
                    continue
                if item_from.name != item_to.name:
                    red('Cannot merge different items.')
                    continue

                item_type = get_item(item_from.name)
                if item_to.count == item_type.count:
                    yellow('Target item is already full as a stack.')
                    continue

                delta = max(item_from.count, item_to.count - item_type.count)
                self.inventory[index_1].count -= delta
                if self.inventory[index_1].count == 0:
                    self.inventory[index_1] = Empty()
                self.inventory[index_2].count += delta

                green(f'Merged {item_type.display()}')

            elif words[0] in {'move', 'switch'}:
                if len(words) != 3:
                    red(f'Invalid usage of command {words[0]!r}.')
                    continue

                index_1_str = words[1]
                if not fullmatch(r'\d+', index_1_str):
                    red(f'Invalid number for item index: {index_1_str}')
                    continue
                index_1 = int(index_1_str)
                if index_1 <= 0 or index_1 > len(self.inventory):
                    red(f'Item index out of bound: {index_1}')
                    continue
                index_1 -= 1

                index_2_str = words[2]
                if not fullmatch(r'\d+', index_2_str):
                    red(f'Invalid number for item index: {index_2_str}')
                    continue
                index_2 = int(index_2_str)
                if index_2 <= 0 or index_2 > len(self.inventory):
                    red(f'Item index out of bound: {index_2}')
                    continue
                index_2 -= 1

                self.inventory[index_1], self.inventory[index_2] = (
                    self.inventory[index_2], self.inventory[index_1])
                gray(f'Switched {self.inventory[index_2].display()}{GRAY}'
                     f' and {self.inventory[index_1].display()}')

            elif words[0] == 'buy':
                if len(words) < 2 or len(words) > 3:
                    red(f'Invalid usage of command {words[0]!r}.')
                    continue

                if last_shop is None:
                    red("You haven't talked to an NPC "
                        "with trades in this region yet!")
                    continue

                trades = get(region.npcs, last_shop).trades

                trade_str = words[1]
                if not fullmatch(r'\d+', trade_str):
                    red(f'Invalid number for trade index: {trade_str}')
                    continue
                trade_index = int(trade_str)
                if trade_index <= 0 or trade_index > len(trades):
                    red(f'Trade index out of bound: {trade_index}')
                    continue
                chosen_trade = trades[trade_index - 1]

                if len(words) == 3:
                    amount_str = words[2]
                    if not fullmatch(r'\d+', amount_str):
                        red(f'Invalid number for trade index: {amount_str}')
                        continue
                    amount = int(amount_str)
                    if amount <= 0:
                        red('Can only buy positive amount of item')
                        continue
                else:
                    amount = 1

                self.buy(chosen_trade, amount)

            elif words[0] == 'sell':
                if len(words) != 2:
                    red(f'Invalid usage of command {words[0]!r}.')
                    continue

                index_str = words[1]
                if not fullmatch(r'\d+', index_str):
                    red(f'Invalid number for item index: {index_str}')
                    continue
                item_index = int(index_str)
                if item_index <= 0 or item_index > len(self.inventory):
                    red(f'Item index out of bound: {item_index}')
                    continue
                item_index -= 1

                self.sell(item_index)

            elif words[0] == 'split':
                if len(words) != 4:
                    red(f'Invalid usage of command {words[0]!r}.')
                    continue

                index_1_str = words[1]
                if not fullmatch(r'\d+', index_1_str):
                    red(f'Invalid number for item index: {index_1_str}')
                    continue
                index_1 = int(index_1_str)
                if index_1 <= 0 or index_1 > len(self.inventory):
                    red(f'Item index out of bound: {index_1}')
                    continue
                index_1 -= 1

                index_2_str = words[2]
                if not fullmatch(r'\d+', index_2_str):
                    red(f'Invalid number for item index: {index_2_str}')
                    continue
                index_2 = int(index_2_str)
                if index_2 <= 0 or index_2 > len(self.inventory):
                    red(f'Item index out of bound: {index_2}')
                    continue
                index_2 -= 1

                amount_str = words[3]
                if not fullmatch(r'\d+', amount_str):
                    red(f'Invalid number for item index: {amount_str}')
                    continue
                amount = int(amount_str)

                item_1 = self.inventory[index_1]
                item_2 = self.inventory[index_2]

                if (not hasattr(item_1, 'count')
                        or isinstance(item_1, (Bow, Sword, Armor, Axe, Pickaxe, Pet))):
                    red('Cannot split unstackable items.')
                    continue

                if item_1.count < amount:
                    red('Cannot split more than the original amount.')
                    continue

                if isinstance(item_2, Empty):
                    self.inventory[index_1].count -= amount
                    self.inventory[index_2] = item_1
                    self.inventory[index_2].count = amount
                    gray(f'Splitted {amount} item from '
                         f'slot {index_1 + 1} to slot {index_2 + 1}.')
                    continue

                if item_1.name != item_2.name:
                    red('Cannot split to a slot with different item.')
                    continue

                item_type = get_item(item_1.name)
                if item_2.count == item_type.count:
                    red('Targeted slot is already full as a stack.')
                    continue

                delta = min(amount, item_type.count - item_2.count)
                if amount > delta:
                    yellow(f'Splitting {delta} istead of {amount} item.')

                self.inventory[index_1].count -= delta
                self.inventory[index_2].count += delta
                gray(f'Splitted {delta} item from '
                     f'slot {index_1 + 1} to slot {index_2 + 1}.')

            elif words[0] == 'pickupstash':
                if len(words) != 1:
                    red(f'Invalid usage of command {words[0]!r}.')
                    continue

                self.pickupstash()

            elif words[0] == 'talkto':
                if len(words) != 2:
                    red(f'Invalid usage of command {words[0]!r}.')
                    continue

                name = words[1]
                if not includes(region.npcs, name):
                    red(f'Npc not found: {name!r}')
                    continue

                result = self.talkto_npc(get(region.npcs, name))
                if result is not None:
                    last_shop = result

            elif words[0] == 'cheat':
                # item = get_item('aspect_of_the_dragons')
                # item.stars = 5
                # item.hot_potato = 20
                # self.recieve(item)
                # item = get_item('hyperion')
                # item.stars = 10
                # item.hot_potato = 30
                # self.recieve(item)
                # item = get_item('diamond_pickaxe')
                # self.recieve(item)
                item = get_item('golden_axe')
                self.recieve(item)
                # item = get_item('enderman_pet')
                # self.recieve(item)
                # item = get_item('ender_helmet')
                # self.recieve(item)

            else:
                red(f'Unknown command: {words[0]!r}')
