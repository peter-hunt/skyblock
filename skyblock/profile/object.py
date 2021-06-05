from decimal import Decimal
from math import ceil, radians, tan
from os import get_terminal_size
from random import choice, choices
from re import fullmatch
from time import sleep, time
from typing import Dict, Iterable, List, Optional

from ..constant.colors import BOLD, GOLD, GRAY, GREEN, AQUA, YELLOW, WHITE
from ..constant.doc import profile_doc
from ..constant.main import INTEREST_TABLE, SELL_PRICE, SKILL_EXP
from ..constant.util import Number
from ..function.io import gray, red, green, yellow, aqua, white
from ..function.math import calc_exp, calc_skill_exp, random_int
from ..function.util import (
    backupable, display_money, display_number, display_name, generate_help,
    get, includes, shorten_money,
)
from ..item.items import COLLECTIONS, get_item
from ..item.mobs import get_mob
from ..item.object import (
    ItemType, Item, Empty, Pickaxe, Axe, Mineral, Tree, Mob,
)
from ..item.resources import get_resource
from ..map import Npc, ISLANDS, calc_dist, path_find

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
    base_crit_chance: int = 0
    base_crit_damage: int = 50
    base_attack_speed: int = 0
    base_intelligence: int = 100
    base_sea_creature_chance: int = 0
    base_magic_find: int = 0
    base_pet_luck: int = 0
    base_ferocity: int = 0
    base_ability_damage: int = 0

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

    def put_stash(self, item: ItemType, /):
        if isinstance(item, Item):
            for index, slot in enumerate(self.stash):
                if not isinstance(slot, Item):
                    continue
                if slot.name != item.name or slot.rarity != item.rarity:
                    continue
                self.stash[index].count += item.count
                return
        self.stash.append(item)
        materials = sum(getattr(item, 'count', 1) for item in self.stash)
        items = 0
        for item in self.stash:
            stack_count = getattr(get_item(item.name), 'count', 1)
            items += ceil(getattr(item, 'count', 1) / stack_count)
        yellow(f'You have {GREEN}{display_number(materials)} materials{YELLOW}'
               f' totalling {AQUA}{display_number(items)} items{YELLOW}'
               f' stashed away!!')
        yellow(f'Use {GOLD}`pickupstash`{YELLOW} to pick it all up!')

    def recieve(self, item: ItemType, /, *, log: bool = True):
        if isinstance(item, Item):
            item_type = get_item(item.name)
            count = item.count
            for index, slot in enumerate(self.inventory):
                if isinstance(slot, Empty):
                    delta = min(count, item_type.count)
                    self.inventory[index] = Item(item.name, delta, item.rarity)
                    count -= delta
                elif not isinstance(slot, Item):
                    continue
                elif slot.name != item.name or slot.rarity != item.rarity:
                    continue
                else:
                    delta = min(count, item_type.count - slot.count)
                    count -= delta
                    self.inventory[index].count += delta
                if count == 0:
                    break
            else:
                self.put_stash(Item(item.name, count, item.rarity))
                return
        else:
            for index, slot in enumerate(self.inventory):
                if isinstance(slot, Empty):
                    self.inventory[index] = item
                    break
            else:
                self.put_stash(item)
                return
        if log:
            gray(f'+ {item.display()}')

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
        current_lvl = calc_skill_exp(name, original_lvl)
        if current_lvl > original_lvl:
            for lvl in range(original_lvl + 1, current_lvl + 1):
                green(f'Reached {name.capitalize()} XP level {lvl} level!')
                if name != 'catacombs':
                    green(f'Reward: {SKILL_EXP[lvl][3]} coins')
                    self.purse += SKILL_EXP[lvl][3]

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
        gray(f"  You're at {region} of {island}.")
        gray('Nearby places:')
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
            gray(f'  {other.name} on the {AQUA}{direc}')

        if len(region.resources) > 0:
            gray('Resources:')
            for resource in region.resources:
                gray(f'  {GREEN}{resource.name}{GRAY} ({resource.type()})')

        if len(region.npcs) > 0:
            gray('NPCs:')
            for npc in region.npcs:
                gray(f'  {GREEN}{npc}{GRAY} ({npc.name})')

    def money(self):
        if self.region != 'bank':
            if self.purse < 1000:
                shortened_purse = ''
            else:
                shortened_purse = f' {GRAY}({shorten_money(self.purse)})'

            white(f'Purse: {GOLD}{display_money(self.purse)}'
                  f'{shortened_purse}')
            return

        if self.balance < 1000:
            shortened_balance = ''
        else:
            shortened_balance = f' {GRAY}({shorten_money(self.balance)})'

        if self.purse < 1000:
            shortened_purse = ''
        else:
            shortened_purse = f' {GRAY}({shorten_money(self.purse)})'

        green('Bank Account')
        gray(f'Balance: {GOLD}{display_money(self.balance)}'
             f'{shortened_balance}')
        white(f'Purse: {GOLD}{display_money(self.purse)}'
              f'{shortened_purse}')
        gray(f'Bank Level: {GREEN}{display_name(self.bank_level)}')

    @backupable
    def talkto_npc(self, npc: Npc, /):
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
                gray(f'  {index:>{digits}} {item.display()}{GRAY} for '
                     f'{GOLD}{display_money(price)} coins{GRAY}.')
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
            dist = calc_dist(region, target)
            time_cost = float(dist) / (5 * (self.base_speed / 100))
            green(f'Going from {region} to {target}...')
            gray(f'(time cost: {time_cost:.2f}s)')
            sleep(time_cost)
            self.region = target.name
            region = get(island.regions, target.name)

    def ls(self):
        length = len(self.inventory)
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
              f"{GOLD}{shorten_money(delta)} Coins{GREEN}!")
        self.inventory[index] = Empty()

    def get(self, name: str, tool_index: Optional[int], amount: int, /):
        resource = get_resource(name)
        tool = Empty() if tool_index is None else self.inventory[tool_index]

        if not isinstance(tool, (Empty, Axe, Pickaxe)):
            tool = Empty()

        if isinstance(resource, Mineral):
            if isinstance(tool, Pickaxe):
                breaking_power = tool.breaking_power
                mining_speed = tool.mining_speed
                if 'efficiency' in tool.enchantments:
                    mining_speed += 10 + 20 * tool.enchantments['efficiency']
            else:
                breaking_power = 0
                mining_speed = 50

            if resource.breaking_power > breaking_power:
                red(f'Insufficient breaking power for {resource.name}.')
                return

            time_cost = 30 * resource.hardness / mining_speed

            mining_lvl = calc_skill_exp('mining', self.skill_xp_mining,)
            drop_mult = (1 + 0.1 * tool.enchantments.get('fortune', 0)
                         + 0.04 * mining_lvl)
            exp_mult = 1 + 0.125 * tool.enchantments.get('experience', 0)
            drop_item = resource.drop
            default_amount = resource.amount

            last_cp = Decimal()
            cp_step = Decimal('0.1')
            is_collection = includes(COLLECTIONS, drop_item)
            for count in range(1, amount + 1):
                sleep(time_cost)
                drop_pool = random_int(drop_mult)
                self.recieve(Item(drop_item, default_amount * drop_pool))
                if is_collection:
                    self.collect(drop_item, default_amount * drop_pool)

                self.add_exp(resource.exp * random_int(exp_mult))
                self.add_skill_exp('mining', resource.mining_exp)
                if count >= (last_cp + cp_step) * amount:
                    while count >= (last_cp + cp_step) * amount:
                        last_cp += cp_step
                    print(f'{count} / {amount} ({(last_cp * 100):.0f}%) done')

        elif isinstance(resource, Tree):
            if isinstance(tool, Axe):
                tool_speed = tool.tool_speed
                if 'efficiency' in tool.enchantments:
                    tool_speed += tool.enchantments['efficiency'] ** 2 + 1
                time_cost = ceil(1.5 * resource.hardness / tool_speed)
            else:
                tool_speed = 1
                time_cost = ceil(5 * resource.hardness / tool_speed)

            foraging_lvl = calc_skill_exp('foraging', self.skill_xp_foraging)
            drop_mult = (1 + 0.01 * foraging_lvl
                         + 0.01 * max(0, foraging_lvl - 14))

            drop_item = resource.drop

            last_cp = Decimal()
            cp_step = Decimal('0.1')
            is_collection = includes(COLLECTIONS, drop_item)
            for count in range(1, amount + 1):
                sleep(time_cost)
                drop_pool = random_int(drop_mult)
                self.recieve(Item(drop_item, drop_pool))
                if is_collection:
                    self.collect(drop_item, drop_pool)

                self.add_skill_exp('foraging', resource.foraging_exp)
                if count >= (last_cp + cp_step) * amount:
                    while count >= (last_cp + cp_step) * amount:
                        last_cp += cp_step
                    print(f'{count} / {amount} ({(last_cp * 100):.0f}%) done')

        else:
            red('Unknown resource type.')

    def slay(self, name: str, weapon_index: Optional[int], amount: int, /):
        mob = get_mob(name)
        tool = Empty(
        ) if weapon_index is None else self.inventory[weapon_index]

        if not isinstance(tool, (Empty, Bow, Sword)):
            tool = Empty()

        if isinstance(mob, Mob):
            red('Unknown mob type.')
            return

        health = self.base_health
        defense = self.base_defense
        strength = self.base_strength
        crit_chance = self.base_crit_chance
        crit_damage = self.base_crit_damage
        attack_speed = self.base_attack_speed
        intelligence = self.base_intelligence
        magic_find = self.magic_find
        ferocity = self.ferocity

        # if isinstance(tool, Pickaxe):
        #     breaking_power = tool.breaking_power
        #     mining_speed = tool.mining_speed
        #     if 'efficiency' in tool.enchantments:
        #         mining_speed += 10 + 20 * tool.enchantments['efficiency']
        # else:
        #     breaking_power = 0
        #     mining_speed = 50

        # time_cost = 30 * resource.hardness / mining_speed

        # mining_lvl = calc_skill_exp('mining', self.skill_xp_mining,)
        # drop_mult = (1 + 0.1 * tool.enchantments.get('fortune', 0)
        #              + 0.04 * mining_lvl)
        # exp_mult = 1 + 0.125 * tool.enchantments.get('experience', 0)
        # drop_item = resource.drop
        # default_amount = resource.amount

        # last_cp = Decimal()
        # cp_step = Decimal('0.1')
        # is_collection = includes(COLLECTIONS, drop_item)
        # for count in range(1, amount + 1):
        #     sleep(time_cost)
        #     drop_pool = random_int(drop_mult)
        #     self.recieve(Item(drop_item, default_amount * drop_pool))
        #     if is_collection:
        #         self.collect(drop_item, default_amount * drop_pool)

        #     self.add_exp(resource.exp * random_int(exp_mult))
        #     self.add_skill_exp('mining', resource.mining_exp)
        #     if count >= (last_cp + cp_step) * amount:
        #         while count >= (last_cp + cp_step) * amount:
        #             last_cp += cp_step
        #         print(f'{count} / {amount} ({(last_cp * 100):.0f}%) done')

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
                  f"{GOLD}{display_money(interest)} coins{GREEN} "
                  f"as interest in your personal bank account!")

        self.last_update = now

    def mainloop(self):
        while True:
            island = get(ISLANDS, self.island)
            if island is None:
                yellow('Invalid island. Using hub as default.')
                island = get(ISLANDS, 'hub')
            region = get(island.regions, self.region)
            if region is None:
                yellow('Invalid region. Using island spawn as default.')
                region = get(island.regions, island.spawn)

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
                          f'{display_money(coins)} Coins{GREEN}! '
                          f'You now have {GOLD}'
                          f'{display_money(self.balance)} Coins{GREEN} '
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
                          f'{display_money(coins)} Coins{GREEN}! '
                          f'You now have {GOLD}'
                          f'{display_money(self.balance)} Coins{GREEN} '
                          'in your account!')

            elif words[0] == 'help':
                if len(words) == 1:
                    print(profile_doc)
                else:
                    phrase = ' '.join(words[1:])
                    if phrase in profile_help:
                        print(f'> {phrase}')
                        print(profile_help[phrase])
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

            elif words[0] == 'goto':
                if len(words) != 2:
                    red(f'Invalid usage of command {words[0]!r}.')
                    continue

                self.goto(words[1])

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

                if not hasattr(item_1, 'count'):
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

                self.talkto_npc(get(region.npcs, name))

            elif words[0] == 'test':
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
                item = get_item('enderman_pet')
                self.recieve(item)
                item = get_item('ender_helmet')
                self.recieve(item)

            else:
                red(f'Unknown command: {words[0]!r}')
