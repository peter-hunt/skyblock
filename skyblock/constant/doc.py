__all__ = ['menu_doc', 'profile_doc']

menu_doc = """
> new
> touch
Create a new profile.

> del <name>
> delete <name>
Delete a profile.

> exit
> quit
Exit the menu.

> help [command]
Show this message or get command description.

> list
> ls
List all the profile avaliable.

> load <name>
> open <name>
Load a profile and run it.
""".strip()

profile_doc = """
> buy <index> [amount=1]
Buy item from the shop.

> clearstash
Removes all items currently in the Stash.

> consume
> use
Consume items.

> deathcount
Displays how many times you have died.

> deposit <coins>
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
> information <index>
Display detailed informatioon about the item.

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

> pickupstash
Takes all items currently in the Stash.

> playtime
> pt
Shows your current playtime.

> sell <index>
Sell item.

> shop [index=all]
Show goods in recently opened shop.

> skills [skill=all]
Get information about your skills.

> slay <mob> [amount=1] [weapon=hand]
Slay mobs.

> split <from-index> <to-index> <amount>
Split items to another slot.

> stats
Get information about your stats.

> talkto <npc>
Talk to an npc.

> unequip <part>
Unequip armor.

> warp <island>
Warp to an island using portal or consumed travel scroll.

> withdraw <coins>
Withdraw coins from the bank to the purse.
""".strip()
