from random import choice
from re import fullmatch
from typing import Dict, List, Optional

from ..constant.color import GOLD, GRAY, BLUE, GREEN, YELLOW
from ..constant.doc import profile_doc
from ..constant.main import ARMOR_PARTS
from ..constant.util import Number
from ..function.math import calc_exp, calc_lvl
from ..function.io import gray, red, green, yellow, blue, aqua
from ..function.util import (
    backupable, display_int, display_number, generate_help,
    get, includes, parse_int, shorten_number,
)
from ..item.mob import get_mob
from ..item.object import (
    Item, Empty, Bow, Sword, Armor, Axe, Hoe, Pickaxe,
)
from ..item.resource import get_resource
from ..map.island import ISLANDS
from ..map.object import Npc

from .action_wrapper import profile_action
from .display_wrapper import profile_display
from .item_wrapper import profile_item
from .math_wrapper import profile_math
from .wrapper import profile_type

__all__ = ['Profile']


profile_help = generate_help(profile_doc)


@profile_action
@profile_display
@profile_item
@profile_math
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
    play_time: int = 0

    armor: List[Armor] = [Empty() for _ in range(4)]
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

    @backupable
    def talkto_npc(self, npc: Npc, /) -> Optional[str]:
        if npc.name not in self.npc_talked:
            if npc.init_dialog is not None:
                self.npc_talk(npc.name, npc.init_dialog)
            elif npc.dialog is not None:
                if isinstance(npc.dialog, list):
                    self.npc_talk(npc.name, npc.dialog)
                elif isinstance(npc.dialog, tuple):
                    self.npc_talk(npc.name, choice(npc.dialog))
            else:
                self.npc_silent(npc)
            if npc.claim_item is not None:
                self.recieve_item(npc.claim_item)
            self.npc_talked.append(npc.name)
            return
        if npc.trades is not None:
            self.display_shop(npc, None)
            return npc.name
        elif npc.dialog is not None:
            if isinstance(npc.dialog, list):
                self.npc_talk(npc.name, npc.dialog)
            elif isinstance(npc.dialog, tuple):
                self.npc_talk(npc.name, choice(npc.dialog))
        else:
            self.npc_silent(npc)

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
                if len(words) != 1:
                    red(f'Invalid usage of command {words[0]!r}.')
                    continue

                yellow(f'Death Count: {BLUE}{display_int(self.death_count)}')

            elif words[0] in {'playtime', 'pt'}:
                if len(words) != 1:
                    red(f'Invalid usage of command {words[0]!r}.')
                    continue

                self.display_playtime()

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
                    tool_index = self.parse_index(words[2])
                    if tool_index is None:
                        continue

                    tool_item = self.inventory[tool_index]
                    if not isinstance(tool_item, (Empty, Axe, Hoe, Pickaxe)):
                        yellow(f'{tool_item.name} item is not tool.\n'
                               f'Using barehand by default.')
                        tool_index = None

                amount = None

                if len(words) == 4:
                    amount = parse_int(words[3])
                    if amount is None:
                        continue
                    if amount == 0:
                        red(f'Amount must be a positive integer.')
                        continue

                self.get_item(name, tool_index, amount)

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
                    weapon_index = self.parse_index(words[2])
                    if weapon_index is None:
                        continue

                    weapon_item = self.inventory[weapon_index]
                    if not isinstance(weapon_item, (Empty, Bow, Sword)):
                        yellow(f'{weapon_item.name} item is not weapon.\n'
                               f'Using barehand by default.')
                        weapon_index = None

                amount = 1

                if len(words) == 4:
                    amount = parse_int(words[3])
                    if amount is None:
                        continue
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

            elif words[0] in {'inv', 'ls'}:
                if len(words) != 1:
                    red(f'Invalid usage of command {words[0]!r}.')
                    continue

                self.display_inv()

            elif words[0] in {'info', 'information', 'item'}:
                if len(words) != 2:
                    red(f'Invalid usage of command {words[0]!r}.')
                    continue

                index = self.parse_index(words[1])
                if index is None:
                    continue

                self.display_item(self.inventory[index])

            elif words[0] == 'stats':
                if len(words) != 1:
                    red(f'Invalid usage of command {words[0]!r}.')
                    continue

                self.display_stats()

            elif words[0] == 'look':
                if len(words) != 1:
                    red(f'Invalid usage of command {words[0]!r}.')
                    continue

                self.look()

            elif words[0] == 'armor':
                if len(words) > 2:
                    red(f'Invalid usage of command {words[0]!r}.')
                    continue

                if len(words) == 1:
                    self.display_armor()
                    continue

                part = words[1]
                if part not in ARMOR_PARTS:
                    red('Please input a valid armor part!')
                    continue
                self.display_armor(part)

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

            elif words[0] == 'exp':
                if len(words) != 1:
                    red(f'Invalid usage of command {words[0]!r}.')
                    continue

                lvl = calc_exp(self.experience)
                left = self.experience - calc_lvl(lvl)
                if lvl <= 15:
                    gap = 2 * lvl + 7
                elif lvl <= 30:
                    gap = 5 * lvl - 3
                else:
                    gap = 9 * lvl - 158

                yellow(f'Experience: {BLUE}{display_int(lvl)} Levels')
                blue(f'{shorten_number(left)}/{shorten_number(gap)}'
                     f' {YELLOW}to the next level.')

            elif words[0] == 'money':
                if len(words) != 1:
                    red(f'Invalid usage of command {words[0]!r}.')
                    continue

                self.display_money()

            elif words[0] == 'save':
                if len(words) != 1:
                    red(f'Invalid usage of command {words[0]!r}.')
                    continue

                self.dump()
                green('Saved!')

            elif words[0] == 'enchant':
                if len(words) != 2:
                    red(f'Invalid usage of command {words[0]!r}.')
                    continue

                if self.region != 'library':
                    red('You can only enchant items at the library!')
                    continue

                index = self.parse_index(words[1])
                if index is None:
                    pass

                self.enchant(index)

            elif words[0] == 'merge':
                if len(words) != 3:
                    red(f'Invalid usage of command {words[0]!r}.')
                    continue

                index_1 = self.parse_index(words[1])
                if index_1 is None:
                    continue

                index_2 = self.parse_index(words[2])
                if index_2 is None:
                    continue

                self.merge(index_1, index_2)

            elif words[0] in {'move', 'switch'}:
                if len(words) != 3:
                    red(f'Invalid usage of command {words[0]!r}.')
                    continue

                index_1 = self.parse_index(words[1])
                if index_1 is None:
                    continue

                index_2 = self.parse_index(words[2])
                if index_2 is None:
                    continue

                self.inventory[index_1], self.inventory[index_2] = (
                    self.inventory[index_2], self.inventory[index_1])
                gray(f'Switched {self.inventory[index_2].display()}{GRAY}'
                     f' and {self.inventory[index_1].display()}')

            elif words[0] == 'shop':
                if len(words) > 2:
                    red(f'Invalid usage of command {words[0]!r}.')
                    continue

                if last_shop is None:
                    red("You haven't talked to an NPC "
                        "with trades in this region yet!")
                    continue

                npc = get(region.npcs, last_shop)

                if len(words) == 2:
                    trade_index = self.parse_index(words[1], len(npc.trades))
                    if trade_index is None:
                        continue
                else:
                    trade_index = None

                self.display_shop(npc, trade_index)

            elif words[0] == 'buy':
                if len(words) not in {2, 3}:
                    red(f'Invalid usage of command {words[0]!r}.')
                    continue

                if last_shop is None:
                    red("You haven't talked to an NPC "
                        "with trades in this region yet!")
                    continue

                trades = get(region.npcs, last_shop).trades

                trade_index = self.parse_index(words[1], len(trades))
                if trade_index is None:
                    continue
                chosen_trade = trades[trade_index]

                if len(words) == 3:
                    amount = parse_int(words[2])
                    if amount is None:
                        continue
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

                item_index = self.parse_index(words[1])
                if item_index is None:
                    continue

                self.sell(item_index)

            elif words[0] == 'split':
                if len(words) != 4:
                    red(f'Invalid usage of command {words[0]!r}.')
                    continue

                index_1 = self.parse_index(words[1])
                if index_1 is None:
                    continue

                index_2 = self.parse_index(words[2])
                if index_2 is None:
                    continue

                amount = parse_int(words[3])
                if amount is None:
                    continue

                self.split(index_1, index_2, amount)

            elif words[0] == 'equip':
                if len(words) != 2:
                    red(f'Invalid usage of command {words[0]!r}.')
                    continue

                index = self.parse_index(words[1])
                if index is None:
                    continue

                armor_piece = self.inventory[index]
                if not isinstance(armor_piece, Armor):
                    red('Cannot equip non-armor item.')
                    continue

                slot_index = ARMOR_PARTS.index(armor_piece.part)
                self.inventory[index] = self.armor[slot_index]
                self.armor[slot_index] = armor_piece

                green(f'Equipped {armor_piece.display()}{GREEN}!')

            elif words[0] == 'unequip':
                if len(words) != 2:
                    red(f'Invalid usage of command {words[0]!r}.')
                    continue

                part = words[1]
                if part not in ARMOR_PARTS:
                    red('Please input a valid armor part!')
                    continue

                slot_index = ARMOR_PARTS.index(part)
                armor_piece = self.armor[slot_index]

                if isinstance(armor_piece, Empty):
                    red(f'You are not wearing a {part}!')
                    continue

                self.recieve_item(armor_piece)
                self.armor[slot_index] = Empty()

                green(f'Unequipped {armor_piece.display()}{GREEN}!')

            elif words[0] == 'clearstash':
                if len(words) != 1:
                    red(f'Invalid usage of command {words[0]!r}.')
                    continue

                self.clearstash()

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
                # item = get_item('hyperion')
                # item.stars = 10
                # item.hot_potato = 30
                # self.recieve_item(item)
                # item = get_item('diamond_pickaxe')
                # self.recieve_item(item)
                # item = get_item('golden_axe')
                # self.recieve_item(item)
                # item = get_item('enderman_pet')
                # self.recieve_item(item)
                # self.add_exp(2000)
                ...

            else:
                red(f'Unknown command: {words[0]!r}')
                yellow("Use 'help' for help.")
