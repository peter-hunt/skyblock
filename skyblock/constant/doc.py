"""
Docstring for user cli.
"""

__all__ = ['menu_doc', 'profile_doc']

# documentation for commands at menu and profiles
menu_doc = """
> clear
Clear the screen.

> delete <name>
> remove <name>
Delete a profile.

> exit
> quit
Exit the menu.

> help [command]
Show this message or get command description.

> load <name>
> open <name>
Load a profile and run it.

> ls
List all the profile avaliable.

> new
> touch
Create a new profile.
""".strip()

profile_doc = """
> armor [part=all]
Display equipped armor.

> buy <index> [amount=1]
Buy item from the shop.

> cheat
Cheat to debug.

> clear
Clear the screen.

> clearstash
Removes all items currently in the Stash.

> collection [category|name]
> collections [category|name]
Display collections.

> consume <index> [amount=1]
> use <index> [amount=1]
Consume item.

> craft <recipe-index> [amount=1]
Craft items.

> deathcount
Displays how many times you have died.

> deposit [all|half|<coins>]
Deposit coins from the purse to the bank.

> enchant <index>
Enchant an item.

> equip <index>
Equip armor.

> exit
> quit
Exit to the menu.

> exp
Display your vanilla experience.

> get <resource> [amount=1] [tool=hand]
Get resources.

> goto <region>
Go to a region.

> info <index>
Display detailed informatioon about the item.

> item <id>
Display information of any item.

> ls
List all the items in the inventory.

> help [command]
Show this message or get command description.

> look
Get information about the region.

> merge <from-index> <to-index>
Merge stackable items in the inventory.

> money
Display information about your money.

> move <index-1> <index-2>
> switch <index-1> <index-2>
Switch items slot in the inventory.

> organize
Organize your inventory. (replace empty slots and make stacks)

> pet
> pet ls
List all the pets in the pet menu.

> pet add <index>
Add a pet to the pet menu.

> pet despawn <index>
Despawn a pet from the pet menu.

> pet info <index>
Display info about pet in the pet menu.

> pet remove <index>
Remove a pet from the pet menu to your inventory.

> pet summon <index>
Summon a pet from the inventory.

> pickupstash
Takes all items currently in the Stash.

> playtime
> pt
Shows your current playtime.

> recipe [category] [--all]
> recipes [category] [--all]
Shows all recipes or recipes avaliable.

> sell <index>
Sell the item.

> shop [index=all]
Show trades in recently opened shop.

> skill [skill=all]
> skills [skill=all]
Get information about your skills.

> slay <mob> [amount=1] [weapon=hand]
Slay mobs.

> split <from-index> <to-index> <amount>
Split items to another slot.

> stats [item_index=none]
Get information about your stats.

> talkto <npc>
Talk to an npc.

> unequip <part>
Unequip armor.

> warp [island]
Warp to an island using portal or consumed travel scroll.

> withdraw [all|half|<coins>]
Withdraw coins from the bank to the purse.
""".strip()
