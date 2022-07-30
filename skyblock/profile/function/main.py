from re import fullmatch
from time import time

from ..._lib import add_history
from ...constant.colors import *
from ...constant.doc import profile_doc, debug_doc
from ...constant.main import ARMOR_PARTS
from ...constant.stat import ALL_STATS
from ...function.io import *
from ...function.math import calc_exp_level, calc_exp, calc_pet_exp
from ...function.util import (
    checkpoint, clear, format_name, format_number, format_roman, format_short,
    generate_help, get, includes, is_valid_usage, parse_int,
)
from ...map.islands import get_island
from ...object.collection import is_collection
from ...object.items import ITEMS, get_item
from ...object.mobs import get_mob
from ...object.object import *
from ...object.options import OPTIONS
from ...object.placed_minion import *
from ...object.recipes import get_recipe
from ...object.resources import get_resource


__all__ = ['mainloop']


if OPTIONS['debug']:
    profile_help = generate_help(f'{profile_doc}\n\n{debug_doc}')
else:
    profile_help = generate_help(profile_doc)


@checkpoint
def mainloop(self):
    last_shop: str | None = None

    green(f'You are playing on profile: {YELLOW}{self.name}')

    self.update(save=False)

    while True:
        island = get_island(self.island)
        if island is None:
            yellow('Invalid island. Using hub as default.')
            island = get_island('hub')

        zone = get(island.zones, self.zone)
        if zone is None:
            yellow('Invalid zone. Using island spawn as default.')
            zone = get(island.zones, island.spawn)

        if last_shop is not None:
            if not includes(zone.npcs, last_shop):
                last_shop = None

        if self.zone not in self.visited_zones:
            dark_green(f'{BOLD}{zone}')
            green(f'New Zone Discovered!')
            self.visited_zones.append(self.zone)

        self.update()

        original_input = input(':> ')
        words = original_input.split()

        if len(words) == 0:
            continue

        add_history(original_input)

        phrase = words[0]
        cmd_found = False
        for i in range(len(words), 0, -1):
            phrase = ' '.join(words[:i])
            for key in profile_help:
                if key == phrase:
                    cmd_found = True
                    break
            if cmd_found:
                break

        if not cmd_found:
            red(f'Command not found: {phrase!r}.')
            continue
        if not is_valid_usage(profile_help[phrase][0], words):
            red(f'Invalid usage of command: {words[0]}.')
            continue

        if words[0] == 'armor':
            if len(words) == 1:
                self.display_armor()
                continue

            part = words[1]
            if part not in ARMOR_PARTS:
                red('Please input a valid armor part!')
                continue
            self.display_armor(part)

        elif words[0] == 'bag':
            if len(words) == 1:
                white(f'Accessory bag {GRAY}(bag accessory)')
                white(f'Minion bag {GRAY}(bag minion)')
            elif len(words) == 2:
                if words[1] in {'accessory', 'minion'}:
                    storage = getattr(self, f'{words[1]}_bag')
                    self.display_storage(storage)

            elif len(words) == 3:
                if words[1] == 'put':
                    index = self.parse_index(words[2])
                    if index is None:
                        continue

                    item = self.inventory[index]
                    if isinstance(item, Empty):
                        red("You don't have an item there!")
                    elif isinstance(item, Accessory):
                        self.inventory[index] = Empty()
                        self.accessory_bag.append(item)
                        self.accessory_bag = sorted(
                            self.accessory_bag,
                            key=lambda accessory: (-'curelm'.index(accessory.rarity[0]), accessory.name)
                        )
                    elif isinstance(item, Minion):
                        self.inventory[index] = Empty()
                        self.minion_bag.append(item)
                        self.minion_bag = sorted(
                            self.minion_bag,
                            key=lambda minion: (minion.name, minion.tier)
                        )
                    else:
                        red('Invalid item type to put in a bag.')
                        continue
                    green(f'Added {item.display()}{GREEN} into bag!')
            elif len(words) == 4:
                if words[1] in {'accessory', 'minion'} and words[2] == 'info':
                    storage = getattr(self, f'{words[1]}_bag')
                    index = self.parse_index(words[3], len(storage))
                    if index is None:
                        continue

                    self.display_item(storage[index])
                if words[1] in {'accessory', 'minion'} and words[2] == 'remove':
                    storage = getattr(self, f'{words[1]}_bag')
                    index = self.parse_index(words[3], len(storage))
                    if index is None:
                        continue

                    item = storage.pop(index)
                    self.recieve_item(item.to_obj())
                    setattr(self, f'{words[1]}_bag', storage)
                    green(f'Removed {item.display()}{GREEN} from bag!')

        elif words[0] in {'be', 'bestiary'}:
            if len(words) == 1:
                self.display_bestiaries()
                continue

            mob_name = words[1]
            if get_mob(mob_name) is None:
                continue

            self.display_bestiary(mob_name)

        elif words[0] == 'buy':
            if last_shop is None:
                red("You haven't talked to an NPC "
                    "with trades in this zone yet!")
                continue

            trades = get(zone.npcs, last_shop).trades

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

        elif words[0] == 'cheat':
            ...

        elif words[0] == 'clear':
            clear()

        elif words[0] == 'clearstash':
            self.clearstash()

        elif words[0] == 'combine':
            index_1 = self.parse_index(words[1])
            if index_1 is None:
                continue

            index_2 = self.parse_index(words[2])
            if index_2 is None:
                continue

            self.combine(index_1, index_2)

        elif words[0] in {'consume', 'use'}:
            index = self.parse_index(words[1])
            if index is None:
                continue

            amount = 1
            if len(words) == 3:
                amount = parse_int(words[2])
                if amount is None:
                    continue
                if amount == 0:
                    yellow('Can only use positive amount of items.')
                    continue

            self.consume(index, amount)

        elif words[0] in {'collection', 'collections'}:
            if len(words) == 1:
                self.display_collections()
                continue

            category = words[1]
            if category in ('farming', 'mining', 'combat',
                            'foraging', 'fishing'):
                self.display_collection(category)
            elif is_collection(category):
                if self.collection[category] == 0:
                    red("You haven't unlocked this collection yet!")
                    continue
                self.display_collection_info(category)
            else:
                red(f'Unknown collection: {category!r}')

        elif words[0] == 'craft':
            recipe = get_recipe(words[1])
            if recipe is None:
                continue

            amount = 1

            if len(words) == 3:
                if words[2] == '--max':
                    if isinstance(recipe, RecipeGroup):
                        for subrecipe in recipe.recipes:
                            self.craft(get_recipe(subrecipe), -1)
                        continue
                    amount = -1
                else:
                    amount = parse_int(words[2])
                    if amount is None:
                        continue
                    if amount == 0:
                        red(f'Amount must be a positive integer.')
                        continue

            if isinstance(recipe, Recipe):
                recipes = [recipe]
            elif isinstance(recipe, RecipeGroup):
                recipes = [get_recipe(name) for name in recipe.recipes]
            self.craft(recipes, amount)

        elif words[0] == 'deathcount':
            death_count = self.stats.get('deaths', 0)
            yellow(f'Death Count: {BLUE}{format_number(death_count)}')

        elif words[0] in {'del', 'delete', 'rm', 'remove'}:
            index = self.parse_index(words[1])
            if index is None:
                continue

            item = self.inventory[index]
            if isinstance(item, Empty):
                red("You don't have an item there!")
                continue
            self.inventory[index] = Empty()
            green(f'Deleted {item.display()}{GREEN}!')

        elif words[0] in {'deposit', 'withdraw'}:
            if self.zone not in {'bank', 'dwarven_village'}:
                red('You can only do that while you are '
                    'at the Bank or Dwarvin Village!')
                continue

            coins_str = words[1].lower() if len(words) == 2 else 'all'
            if coins_str in {'all', 'half'}:
                if words[0] == 'deposit':
                    coins = self.purse
                else:
                    coins = self.balance

                if coins_str == 'half':
                    coins /= 2
            else:
                if not fullmatch(r'\d+(\.\d+)?[tbmk]?', coins_str):
                    red('Invalid amount of coins.')
                    continue

                if coins_str[-1] in 'kmbt':
                    mult = 1000 ** ('kmbt'.index(
                        coins_str[-1].lower()) + 1)
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
                      f'{format_number(coins)} Coins{GREEN}! '
                      f'You now have {GOLD}'
                      f'{format_number(self.balance)} Coins{GREEN} '
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
                      f'{format_number(coins)} Coins{GREEN}! '
                      f'You now have {GOLD}'
                      f'{format_number(self.balance)} Coins{GREEN} '
                      'in your account!')

        elif words[0] == 'enchant':
            if self.zone != 'library':
                red('You can only enchant items at the library!')
                continue

            index = self.parse_index(words[1])
            if index is None:
                continue

            self.enchant(index)

        elif words[0] == 'equip':
            index = self.parse_index(words[1])
            if index is None:
                continue

            armor_piece = self.inventory[index]
            if not isinstance(armor_piece, Armor):
                red('Cannot equip non-armor item.')
                continue

            if armor_piece.collection_req is not None:
                coll_name, lvl = armor_piece.collection_req
                if self.get_collection_level(coll_name) < lvl:
                    red("You haven't reached the required collection yet!")
                    continue

            combat_req = armor_piece.combat_skill_req
            combat_level = self.get_skill_level('combat')

            if armor_piece.combat_skill_req is None:
                pass
            elif combat_req > combat_level:
                red(f'Requires Combat level {format_roman(combat_req)}')
                continue

            slot_index = ARMOR_PARTS.index(armor_piece.part)
            self.inventory[index] = self.armor[slot_index]
            self.armor[slot_index] = armor_piece

            green(f'Equipped {armor_piece.display()}{GREEN}!')

        elif words[0] in {'exit', 'quit'}:
            self.dump()
            green('Saved!')
            break

        elif words[0] == 'exp':
            lvl = calc_exp_level(self.experience)
            left = self.experience - calc_exp(lvl)
            if lvl <= 15:
                gap = 2 * lvl + 7
            elif lvl <= 30:
                gap = 5 * lvl - 3
            else:
                gap = 9 * lvl - 158

            gray(f'Experience: {BLUE}{format_number(lvl)} Levels')
            yellow(f'{format_short(left)}{GOLD}'
                   f'/{YELLOW}{format_short(gap)}'
                   f' {GRAY}to the next level.')

        elif words[0] == 'fish':
            if not zone.fishable:
                red("There's no water for you to fish at!")
                continue

            rod_index = self.parse_index(words[1])
            if rod_index is None:
                continue

            rod_item = self.inventory[rod_index]
            if not isinstance(rod_item, FishingRod):
                yellow(f'Can only use fishing rod to fish!')
                continue

            iteration = 1

            if len(words) == 3:
                iteration = parse_int(words[2])
                if iteration is None:
                    continue
                if iteration == 0:
                    red(f'Iteration must be a positive integer.')
                    continue

            self.fish(rod_index, iteration)

        elif words[0] in {'gather', 'get', 'mine'}:
            name = words[1]
            if get_resource(name) is None:
                continue
            if get(zone.resources, name) is None:
                red(f'Resource not avaliable at {zone}: {name!r}')
                continue

            tool_index = None

            if len(words) >= 3:
                tool_index = self.parse_index(words[2])
                if tool_index is None:
                    continue

                tool_item = self.inventory[tool_index]
                if not isinstance(tool_item,
                                  (Empty, Axe, Hoe, Pickaxe, Drill)):
                    yellow(f'{tool_item.display()} {YELLOW}is not tool.\n'
                           f'Using barehand.')
                    tool_index = None

            amount = 1

            if len(words) == 4:
                amount = parse_int(words[3])
                if amount is None:
                    continue
                if amount == 0:
                    red(f'Amount must be a positive integer.')
                    continue

            self.gather(name, tool_index, amount)

        elif words[0] == 'give':
            name = words[1]
            item = get_item(name)
            if item is None:
                continue

            if len(words) == 2:
                amount = 1
            elif len(words) == 3:
                amount = parse_int(words[2])

            obj = item.to_obj()
            obj['count'] = amount
            self.recieve_item(obj)

        elif words[0] == 'goto':
            self.goto(words[1])

        elif words[0] == 'help':
            if len(words) == 1:
                gray(f'\n{profile_doc}\n')
                continue

            phrase = ' '.join(words[1:])
            help_found = []
            for key, pair in profile_help.items():
                if key.startswith(phrase):
                    usage, description = pair
                    help_found.append(f'{usage}\n{description}')
            if len(help_found) != 0:
                gray('\n' + '\n\n'.join(help_found) + '\n')
            else:
                red(f'Command not found: {phrase!r}.')

        elif words[0] == 'hotm':
            if self.island != 'mines':
                red('You can only use the HoTM menu in the Dwarven Mines!')
                continue

            self.display_hotm()

        elif words[0] == 'hub':
            self.warp('hub')

        elif words[0] in {'info', 'information'}:
            index = self.parse_index(words[1])
            if index is None:
                continue

            self.display_item(self.inventory[index])

        elif words[0] == 'item':
            name = words[1]

            rarity = None
            tier = None
            if match := fullmatch(r'(\w+_minion)_([1-9]|1[0-2])', name):
                name = match.group(1)
                tier = int(match.group(2))
            elif match := fullmatch(
                (r'(common|uncommon|rare|epic|legendary|mythic'
                 r'|divine|special|very_special)_(\w+)'),
                name,
            ):
                rarity = match.group(1)
                name = match.group(2)

            for item in ITEMS:
                if rarity is None:
                    pass
                elif getattr(item, 'rarity', None) != rarity:
                    continue

                if tier is None:
                    pass
                elif getattr(item, 'tier', None) != tier:
                    continue

                if item.name == name:
                    if isinstance(item, Pet):
                        item.exp = calc_pet_exp(item.rarity, 100)
                    self.display_item(item)
                    break
            else:
                restric = []
                if rarity is not None:
                    restric.append(f'{format_name(rarity)} rarity')
                if tier is not None:
                    restric.append(f'tier {tier}')

                if len(restric) == 0:
                    red(f'Item not found: {name!r}.')
                else:
                    restric_str = ', '.join(restric)
                    red(f'Item not found: {name!r} with {restric_str}.')

        elif words[0] in {'kill', 'slay'}:
            name = words[1]
            mob = get_mob(name)
            if mob is None:
                continue

            mob = get(zone.mobs, name)
            if mob is None:
                red(f'Mob not avaliable at {zone}: {name!r}')
                continue

            weapon_index = None

            if len(words) >= 3:
                weapon_index = self.parse_index(words[2])
                if weapon_index is None:
                    continue

                weapon_item = self.inventory[weapon_index]
                if (isinstance(weapon_item, (FishingRod, Pickaxe, Drill)) and
                        getattr(weapon_item, 'damage', 0) != 0):
                    pass
                elif not isinstance(weapon_item, (Empty, Bow, Sword)):
                    yellow(f'{weapon_item.display()} {YELLOW}is not weapon.\n'
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

            self.slay(mob, weapon_index, amount)

        elif words[0] == 'look':
            self.display_location()

        elif words[0] == 'ls':
            self.display_storage()

        elif words[0] == 'merge':
            index_1 = self.parse_index(words[1])
            index_2 = self.parse_index(words[2])
            if index_1 is None or index_2 is None:
                continue

            self.merge(index_1, index_2)

        elif words[0] == 'minion':
            if len(words) == 1 or words[1] == 'ls':
                self.display_minions()

            elif words[1] == 'claim':
                slot = self.parse_index(words[2], len(self.placed_minions))
                if slot is None:
                    continue

                minion = self.placed_minions[slot]
                if not isinstance(minion, PlacedMinion):
                    red('This slot is empty!')
                    continue
                elif slot is None:
                    for item in minion.inventory:
                        if not isinstance(item, Empty):
                            break
                    else:
                        self.claim_minion(slot)
                        continue
                    red('This Minion does not have any items stored!')
                else:
                    self.claim_minion(slot)

            elif words[1] == 'info':
                slot = self.parse_index(words[2], len(self.placed_minions))
                if slot is None:
                    continue

                minion = self.placed_minions[slot]
                if not isinstance(minion, PlacedMinion):
                    red('This slot is empty!')
                    continue

                self.display_minion_info(slot)

            elif words[1] == 'place':
                index = self.parse_index(words[2])
                if index is None:
                    continue

                minion = self.inventory[index]
                if not isinstance(minion, Minion):
                    red('This is not a Minion!')
                    continue

                slot = self.parse_index(words[3], len(self.placed_minions))
                if slot is None:
                    continue

                self.place_minion(index, slot)

            elif words[1] == 'remove':
                slot = self.parse_index(words[2], len(self.placed_minions))
                if slot is None:
                    continue

                self.remove_minion(slot)

            else:
                red(f'Invalid subcommand of {words[0]}: {words[1]!r}')

        elif words[0] == 'money':
            self.display_money()

        elif words[0] in {'move', 'mv', 'switch'}:
            index_1 = self.parse_index(words[1])
            index_2 = self.parse_index(words[2])
            if index_1 is None or index_2 is None:
                continue

            self.inventory[index_1], self.inventory[index_2] = (
                self.inventory[index_2], self.inventory[index_1])
            gray(f'Switched {self.inventory[index_2].display()}{GRAY}'
                 f' and {self.inventory[index_1].display()}')

        elif words[0] == 'organize':
            inventory = [item.copy() for item in self.inventory
                         if not isinstance(item, Empty)]
            self.inventory = [Empty() for _ in range(36)]
            for item in inventory:
                if isinstance(item, Empty):
                    continue
                self.recieve_item(item.to_obj())

        elif words[0] == 'pickupstash':
            self.pickupstash()

        elif words[0] == 'pet':
            if len(words) == 1 or words[1] == 'ls':
                self.display_pets()

            elif words[1] == 'add':
                index = self.parse_index(words[2])
                if index is None:
                    continue

                item = self.inventory[index]
                if not isinstance(item, Pet):
                    red('You cannot add this item to your pet menu!')
                    continue

                self.add_pet(index)

            elif words[1] == 'despawn':
                self.despawn_pet()

            elif words[1] == 'info':
                if len(words) == 2:
                    for pet in self.pets:
                        if pet.active:
                            self.display_item(pet)
                            break
                    else:
                        red("You don't have an active pet!")
                    continue

                index = self.parse_index(words[2], len(self.pets))
                if index is None:
                    continue

                self.display_item(self.pets[index])

            elif words[1] == 'remove':
                index = self.parse_index(words[2], len(self.pets))
                if index is None:
                    continue

                self.remove_pet(index)

            elif words[1] == 'sort':
                self.pets = sorted(self.pets, key=lambda pet: (-'curelm'.index(pet.rarity[0]), -pet.exp, pet.name))
                green('Sorted pet list!')

            elif words[1] == 'summon':
                index = self.parse_index(words[2], len(self.pets))
                if index is None:
                    continue

                self.summon_pet(index)

            else:
                red(f'Invalid subcommand of {words[0]}: {words[1]!r}')

        elif words[0] in {'pt', 'playtime'}:
            self.display_playtime()

        elif words[0] in {'recipe', 'recipes'}:
            if len(words) == 1:
                self.display_recipes()
                continue

            show_all = False

            if len(words) == 3:
                if words[2] != '--all':
                    red(f'Invalid tag: {words[2]!r}')
                    red("Can only use '--all'.")
                    continue
                show_all = True

            arg = words[1]
            if len(words) == 2 and arg == '--all':
                self.display_recipes(show_all=True)
                continue
            elif arg in {
                    'farming', 'mining', 'forging',
                    'smelting', 'combat', 'fishing',
                    'foraging', 'enchanting', 'alchemy', 'slayer'}:
                self.display_recipe(arg, show_all=show_all)
                continue

            recipe = get_recipe(arg)
            if recipe is None:
                continue

            self.display_recipe_info(recipe)

        elif words[0] == 'save':
            self.dump()
            self.last_update = time()
            green('Saved!')

        elif words[0] == 'sell':
            index = self.parse_index(words[1], warn=False)
            if index is not None:
                if len(zone.npcs) == 0:
                    red('No NPCs around to sell the item.')
                    continue
                self.sell(index)
                continue

            sell_item = get_item(words[1])
            if sell_item is None:
                continue

            if len(zone.npcs) == 0:
                red('No NPCs around to sell the item.')
                continue
            sell_name = words[1]
            sold = False
            for i, item in enumerate(self.inventory):
                if isinstance(item, Empty):
                    continue
                if item.name == sell_name:
                    if not sold:
                        sold = True
                    self.sell(i)

            if not sold:
                red("You don't have this item in your inventory!")

        elif words[0] == 'shop':
            if last_shop is None:
                red("You haven't talked to an NPC "
                    "with trades in this zone yet!")
                continue

            npc = get(zone.npcs, last_shop)

            if len(words) == 2:
                trade_index = self.parse_index(words[1], len(npc.trades))
                if trade_index is None:
                    continue
            else:
                trade_index = None

            self.display_shop(npc, trade_index)

        elif words[0] in {'skill', 'skills'}:
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

        elif words[0] == 'split':
            index_1 = self.parse_index(words[1])
            index_2 = self.parse_index(words[2])
            if index_1 is None or index_2 is None:
                continue

            amount = parse_int(words[3])
            if amount is None:
                continue

            self.split(index_1, index_2, amount)

        elif words[0] in {'stat', 'stats'}:
            stat_name = 'all'
            index = None
            if len(words) == 3:
                stat_name = words[1]
                index = self.parse_index(words[2])
                if index is None:
                    continue
            elif len(words) == 2:
                if words[1] in ALL_STATS:
                    stat_name = words[1]
                else:
                    index = self.parse_index(words[1])
                    if index is None:
                        red('Invalid stat name!')
                        continue
            else:
                index = None

            if stat_name == 'all':
                self.display_stats(index)
            else:
                self.display_stat(stat_name, index)

        elif words[0] == 'talkto':
            name = words[1]
            if not includes(zone.npcs, name):
                red(f'Npc not found: {name!r}.')
                continue

            result = self.talkto_npc(get(zone.npcs, name))
            if result is not None:
                last_shop = result

        elif words[0] == 'unequip':
            part = words[1]
            if part not in ARMOR_PARTS:
                red('Please input a valid armor part!')
                continue

            slot_index = ARMOR_PARTS.index(part)
            armor_piece = self.armor[slot_index]

            if isinstance(armor_piece, Empty):
                red(f'You are not wearing a {part}!')
                continue

            self.recieve_item(armor_piece.to_obj())
            self.armor[slot_index] = Empty()

            green(f'Unequipped {armor_piece.display()}{GREEN}!')

        elif words[0] == 'warp':
            if len(words) == 1:
                self.display_warp()
            else:
                self.warp(words[1])

        else:
            red('Unknown command. Type `help` for help.')


main_functions = {
    name: globals()[name] for name in __all__
}
