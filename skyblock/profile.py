from dataclasses import dataclass, field
from decimal import Decimal
from json import dump, load
from math import ceil, radians, tan
from os import get_terminal_size
from os.path import join
from pathlib import Path
from random import choice, choices
from re import fullmatch
from time import sleep, time
from typing import Dict, List, Optional, Union

from .const import SKILL_EXP, INTEREST_TABLE, profile_doc
from .func import (
    Number, calc_skill_exp, calc_exp, exist_dir, exist_file,
    get, backupable, gen_help, random_int, display_money, shorten_money,
    red, green, blue, yellow, cyan, GREEN, YELLOW, CYAN,
)
from .item import (
    ALL_ITEM, COLLECTIONS, RESOURCES, SELL_PRICE, from_obj, ItemType,
    Item, Empty, Pickaxe, Pickaxe, Axe, Mineral, TreeType,
)
from .map import Island, Region, ISLANDS, calc_dist, path_find, includes

__all__ = ['Profile']


profile_help = gen_help(profile_doc)


@dataclass
class Profile:
    name: str
    last_update: Optional[int] = None

    # starter | gold | deluxe | super_deluxe | premier
    bank_level: str = 'starter'
    balance: Number = 0.0
    purse: Number = 0.0

    experience: Number = 0

    island: Island = get(ISLANDS, 'hub')
    region: Region = get(get(ISLANDS, 'hub').regions, 'village')

    base_health: int = 100
    base_defense: int = 0
    base_strength: int = 0
    base_speed: int = 100
    base_crit_chance: int = 0
    base_crit_damage: int = 0
    base_attack_speed: int = 0
    base_intelligence: int = 0
    base_sea_creature_chance: int = 0
    base_magic_find: int = 0
    base_pet_luck: int = 0
    base_ferocity: int = 0
    base_ability_damage: int = 0

    skill_xp_alchemy: float = 0.0
    skill_xp_carpentry: float = 0.0
    skill_xp_combat: float = 0.0
    skill_xp_enchanting: float = 0.0
    skill_xp_farming: float = 0.0
    skill_xp_fishing: float = 0.0
    skill_xp_foraging: float = 0.0
    skill_xp_mining: float = 0.0
    skill_xp_taming: float = 0.0
    collection: Dict[str, int] = field(default_factory=dict)

    crafted_minions: List[str] = field(default_factory=list)

    armor: List[Item] = field(
        default_factory=lambda: [{} for _ in range(4)]
    )
    pets: List[Item] = field(default_factory=list)
    ender_chest: List[Item] = field(default_factory=list)
    inventory: List[Item] = field(
        default_factory=lambda: [{} for _ in range(36)]
    )
    potion_bag: List[Item] = field(default_factory=list)
    quiver: List[Item] = field(default_factory=list)
    stash: List[Item] = field(default_factory=list)
    talisman_bag: List[Item] = field(default_factory=list)
    wardrobe: List[Item] = field(default_factory=list)
    wardrobe_slot: Optional[int] = None

    npc_talked: List[str] = field(default_factory=list)

    @staticmethod
    def is_valid(name, warn=False):
        return (exist_dir(warn=warn) and exist_dir('saves', warn=warn)
                and exist_file('saves', f'{name}.json', warn=warn))

    @classmethod
    def load(cls, name):
        if not cls.is_valid(name, warn=True):
            red('Error: Profile not found.')
            return

        with open(join(Path.home(), 'skyblock',
                       'saves', f'{name}.json')) as file:
            data = load(file)

        return cls(
            name=name, last_update=data.get('last_update'),
            bank_level=data.get('bank_level', 'starter'),
            balance=data.get('balance', 0),
            purse=data.get('purse', 0),

            experience=data.get('experience', 0),

            island=data.get('island', 'hub'),
            region=data.get('region', 'village'),

            base_health=data.get('base_health', 100),
            base_defense=data.get('base_defense', 0),
            base_strength=data.get('base_strength', 0),
            base_speed=data.get('base_speed', 100),
            base_crit_chance=data.get('base_crit_chance', 0),
            base_crit_damage=data.get('base_crit_damage', 0),
            base_attack_speed=data.get('base_attack_speed', 0),
            base_intelligence=data.get('base_intelligence', 0),
            base_sea_creature_chance=data.get('base_sea_creature_chance', 0),
            base_magic_find=data.get('base_magic_find', 0),
            base_pet_luck=data.get('base_pet_luck', 0),
            base_ferocity=data.get('base_ferocity', 0),
            base_ability_damage=data.get('base_ability_damage', 0),

            collection=data.get('collection', {}),
            skill_xp_alchemy=data.get('skill_xp_alchemy', 0.0),
            skill_xp_carpentry=data.get('skill_xp_carpentry', 0.0),
            skill_xp_combat=data.get('skill_xp_combat', 0.0),
            skill_xp_enchanting=data.get('skill_xp_enchanting', 0.0),
            skill_xp_farming=data.get('skill_xp_farming', 0.0),
            skill_xp_fishing=data.get('skill_xp_fishing', 0.0),
            skill_xp_foraging=data.get('skill_xp_foraging', 0.0),
            skill_xp_mining=data.get('skill_xp_mining', 0.0),
            skill_xp_taming=data.get('skill_xp_taming', 0.0),

            crafted_minions=data.get('crafted_minions', []),

            armor=[from_obj(item) for item in data.get(
                'armor', [{'type': 'empty'} for _ in range(4)],
            )],
            pets=[from_obj(item) for item in data.get('pets', [])],
            ender_chest=[from_obj(item)
                         for item in data.get('ender_chest', [])],
            inventory=[from_obj(item) for item in data.get(
                'inventory', [{'type': 'empty'} for _ in range(36)],
            )],
            potion_bag=[from_obj(item) for item in data.get('potion_bag', [])],
            quiver=[from_obj(item) for item in data.get('quiver', [])],
            stash=[from_obj(item) for item in data.get('stash', [])],
            talisman_bag=[from_obj(item)
                          for item in data.get('talisman_bag', [])],
            wardrobe=[from_obj(item) for item in data.get('wardrobe', [])],
            wardrobe_slot=data.get('wardrobe_slot', 0),

            npc_talked=data.get('npc_talked', []),
        )

    def dump(self):
        with open(join(Path.home(), 'skyblock',
                       'saves', f'{self.name}.json'), 'w') as file:
            dump({
                'last_update': self.last_update,
                'bank_level': self.bank_level,
                'balance': self.balance,
                'purse': self.purse,

                'experience': self.experience,

                'island': self.island,
                'region': self.region,

                'base_health': self.base_health,
                'base_defense': self.base_defense,
                'base_strength': self.base_strength,
                'base_speed': self.base_speed,
                'base_crit_chance': self.base_crit_chance,
                'base_crit_damage': self.base_crit_damage,
                'base_attack_speed': self.base_attack_speed,
                'base_intelligence': self.base_intelligence,
                'base_sea_creature_chance': self.base_sea_creature_chance,
                'base_magic_find': self.base_magic_find,
                'base_pet_luck': self.base_pet_luck,
                'base_ferocity': self.base_ferocity,
                'base_ability_damage': self.base_ability_damage,

                'collection': self.collection,
                'skill_xp_alchemy': self.skill_xp_alchemy,
                'skill_xp_carpentry': self.skill_xp_carpentry,
                'skill_xp_combat': self.skill_xp_combat,
                'skill_xp_enchanting': self.skill_xp_enchanting,
                'skill_xp_farming': self.skill_xp_farming,
                'skill_xp_fishing': self.skill_xp_fishing,
                'skill_xp_foraging': self.skill_xp_foraging,
                'skill_xp_mining': self.skill_xp_mining,
                'skill_xp_taming': self.skill_xp_taming,

                'crafted_minions': self.crafted_minions,

                'armor': [item.to_obj() for item in self.armor],
                'pets': [item.to_obj() for item in self.pets],
                'ender_chest': [item.to_obj() for item in self.ender_chest],
                'inventory': [item.to_obj() for item in self.inventory],
                'potion_bag': [item.to_obj() for item in self.potion_bag],
                'quiver': [item.to_obj() for item in self.quiver],
                'stash': [item.to_obj() for item in self.stash],
                'talisman_bag': [item.to_obj() for item in self.talisman_bag],
                'wardrobe': [item.to_obj() for item in self.wardrobe],
                'wardrobe': [item.to_obj() for item in self.wardrobe],
                'wardrobe_slot': self.wardrobe_slot,

                'npc_talked': self.npc_talked,
            }, file, indent=2, sort_keys=True)

    def put_stash(self, item: ItemType):
        if isinstance(item, Item):
            for index, slot in enumerate(self.stash):
                if not isinstance(slot, Item):
                    continue
                if slot.name != item.name or slot.rarity != item.rarity:
                    continue
                self.stash[index].count += item.count
                return
        self.stash.append(item)

    def recieve(self, item: ItemType):
        cyan(f'+{item.display()}')
        if isinstance(item, Item):
            item_type = get(ALL_ITEM, item.name)
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
        else:
            for index, slot in enumerate(self.inventory):
                if isinstance(slot, Empty):
                    self.inventory[index] = item
                    break
            else:
                self.put_stash(item)

    def add_exp(self, amount):
        original_lvl = calc_exp(self.experience)
        self.experience += amount
        current_lvl = calc_exp(self.experience)
        if current_lvl > original_lvl:
            green(f'Reached XP level {current_lvl}.')

    def add_skill_exp(self, name, amount):
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
                if name != 'dungeoneering':
                    green(f'Reward: {SKILL_EXP[lvl][3]} coins')
                    self.purse += SKILL_EXP[lvl][3]

    def look(self):
        island = get(ISLANDS, self.island)
        region = get(island.regions, self.region)

        cyan('Location:')
        cyan(f"  You're at {region} of {island}.")
        cyan('Nearby places:')
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
            cyan(f'  {other.name} on the {direc}')

        if len(region.resources) > 0:
            cyan('Resources:')
            for resource in region.resources:
                cyan(f'  {resource.name} ({resource.type()})')

        if len(region.npcs) > 0:
            cyan('NPCs:')
            for npc in region.npcs:
                cyan(f'  {npc} ({npc.name})')

    def money(self):
        cyan(f'Purse: {YELLOW}{display_money(self.purse)} coins'
             f' {CYAN}({YELLOW}{shorten_money(self.purse)}{CYAN})')
        cyan(f'Balance: {YELLOW}{display_money(self.balance)} coins'
             f' {CYAN}({YELLOW}{shorten_money(self.balance)}{CYAN})')
        bank_level = ' '.join(word.capitalize()
                              for word in self.bank_level.split('_'))
        cyan(f'Bank Level: {bank_level}')

    @backupable
    def talkto_npc(self, npc):
        if npc.name not in self.npc_talked:
            if npc.init_dialog is not None:
                self.npc_talk(npc.init_dialog)
            elif npc.dialog is not None:
                self.npc_talk(choice(npc.dialog))
            else:
                cyan(choices((
                    f"{npc} doesn't seem to want to talk to you.",
                    f"{npc} has got nothing to say to you.",
                    f"{npc} is in his peace.",
                    f"{npc} seems tired and sleepy.",
                    f"{npc} stared at you and didn't talk.",
                    f"{npc} smiled mysteriously.",
                    f"{npc} made a strange noise.",
                    f"{npc} spoke a strange language you've never heard before.",
                ), (20, 25, 20, 18, 10, 4, 2, 1))[0])
            self.npc_talked.append(npc.name)
            return
        if npc.trades is not None:
            cyan(f"{npc}'s shop:")
            digits = len(f'{len(npc.trades)}')
            for index, (price, item) in enumerate(npc.trades):
                cyan(f'  {index:>{digits}} {item.display()}{CYAN} for '
                     f'{YELLOW}{display_money(price)} coins{CYAN}.')
        elif npc.dialog is not None:
            self.npc_talk(choice(npc.dialog))
        else:
            cyan(choices((
                f"{npc} doesn't seem to want to talk to you.",
                f"{npc} has got nothing to say to you.",
                f"{npc} is in his peace.",
                f"{npc} seems tired and sleepy.",
                f"{npc} stared at you and didn't talk.",
                f"{npc} smiled mysteriously.",
                f"{npc} made a strange noise.",
                f"{npc} spoke a language you've never heard before",
            ), (20, 25, 20, 18, 10, 4, 2, 1))[0])

    @backupable
    def goto(self, dest):
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
        cyan(f'Route: {route} ({float(accum_dist):.2f}m)')
        for target in path[1:]:
            dist = calc_dist(region, target)
            time_cost = float(dist) / (5 * (self.base_speed / 100))
            cyan(f'Going from {region} to {target}...')
            cyan(f'(time cost: {time_cost:.2f}s)')
            sleep(time_cost)
            self.region = target.name

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
            cyan(f'{(index + 1):>{digits * 2 + 1}} {item.display()}')
            index += 1

    def info(self, index: int):
        item = self.inventory[index]
        if isinstance(item, Empty):
            cyan('Empty')
            return
        width, _ = get_terminal_size()
        width = ceil(width * 0.85)
        print(f"\x1b[1;38;2;255;255;85m{'':-^{width}}\x1b[0m")
        print(item.info())
        print(f"\x1b[1;38;2;255;255;85m{'':-^{width}}\x1b[0m")

    def collect(self, name: str, amount: int):
        if name not in self.collection:
            self.collection[name] = 0
        self.collection[name] += amount

    def sell(self, index: int):
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
        red(f"Sold {item.display()} for "
            f"{YELLOW}{shorten_money(delta)} coins{CYAN}.")
        self.inventory[index] = Empty()

    def get(self, name: str, tool_index: Optional[int], amount: int):
        resource = get(RESOURCES, name)
        if tool_index is None:
            tool = Empty()
        else:
            tool = self.inventory[tool_index]

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
            is_collection = get(COLLECTIONS, drop_item) is not None
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

        if isinstance(resource, TreeType):
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
            is_collection = get(COLLECTIONS, drop_item) is not None
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

    @staticmethod
    def npc_talk(dialog):
        iterator = iter(dialog)
        blue(next(iterator))
        for sentence in iterator:
            sleep(1.5)
            blue(sentence)

    def update(self):
        now = int(time())
        last = now if self.last_update is None else self.last_update
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
                  f"{YELLOW}{display_money(interest)} coins{GREEN} "
                  f"as interest in your personal bank account!")

        self.last_update = now

    def mainloop(self):
        while True:
            island = get(ISLANDS, self.island)
            region = get(island.regions, self.region)

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

                coins_str = words[1]
                if not fullmatch(r'\d+(\.\d{1,2})?[TtBbMmKk]', coins_str):
                    red('Invalid amount of coins.')
                    continue
                if coins_str[-1].lower() in 'kmbt':
                    mult = 1000 ** ('kmbt'.index(coins_str[-1].lower()) + 1)
                    coins_str = coins_str[:-1]
                else:
                    mult = 1
                coins = eval(coins_str) * mult

                if words[0] == 'deposit':
                    if self.purse < coins:
                        red('Not enough coins to deposit.')
                        continue

                    self.purse -= coins
                    self.balance += coins

                    cyan(f'Desposited {YELLOW}'
                         f'{shorten_money(coins)}'f'{CYAN} coins. '
                         f'You have {YELLOW}'
                         f'{shorten_money(self.purse)}{CYAN} coins in purse.')
                else:
                    if self.balance < coins:
                        red('Not enough coins to withdraw.')
                        continue

                    self.balance -= coins
                    self.purse += coins

                    cyan(f'Withdrew {YELLOW}'
                         f'{shorten_money(coins)}'f'{CYAN} coins. '
                         f'You have {YELLOW}'
                         f'{shorten_money(self.purse)}{CYAN} coins in purse.')

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
                if get(RESOURCES, name) is None:
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

                item_type = get(ALL_ITEM, item_from.name)
                if item_to.count == item_type.count:
                    yellow('Target item is already full as a stack.')
                    continue

                delta = max(item_from.count, item_to.count - item_type.count)
                self.inventory[index_1].count -= delta
                if self.inventory[index_1].count == 0:
                    self.inventory[index_1] = Empty()
                self.inventory[index_2].count += delta

                cyan(f'Merged {item_type.display()}')

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
                cyan(f'Switched {self.inventory[index_2].display()}{CYAN}'
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
                    cyan(f'Splitted {amount} item from '
                         f'slot {index_1 + 1} to slot {index_2 + 1}.')
                    continue

                if item_1.name != item_2.name:
                    red('Cannot split to a slot with different item.')
                    continue

                item_type = get(ALL_ITEM, item_1.name)
                if item_2.count == item_type.count:
                    yellow('Targeted slot is already full as a stack.')
                    continue

                delta = min(amount, item_type.count - item_2.count)
                if amount > delta:
                    yellow(f'Splitting {delta} istead of {amount} item.')

                self.inventory[index_1].count -= delta
                self.inventory[index_2].count += delta
                cyan(f'Splitted {delta} item from '
                     f'slot {index_1 + 1} to slot {index_2 + 1}.')

            elif words[0] == 'talkto':
                if len(words) != 2:
                    red(f'Invalid usage of command {words[0]!r}.')
                    continue

                name = words[1]
                if not includes(region.npcs, name):
                    red(f'Npc not found: {name!r}')
                    continue
                self.talkto_npc(get(region.npcs, name))

            # elif words[0] == 'test':
            #     self.recieve(get(ALL_ITEM, 'golden_axe'))

            else:
                red(f'Unknown command: {words[0]!r}')
