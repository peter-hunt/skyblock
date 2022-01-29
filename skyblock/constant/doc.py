__all__ = ['menu_doc', 'profile_doc']

menu_doc = """
> clear
Clear the screen.

> delete <profile>
> remove <profile>
Delete a profile.

> exit
> quit
Exit the menu.

> help [command]
Show this message or get command description.

> load <profile>
> open <profile>
Load a profile and run it.

> ls
List all the profile avaliable.

> new
> touch
Create a new profile.
""".strip()

profile_doc = """
> armor [armor-part]
Display equipped armor.

> be [mob]
> bestiary [mob]
Display bestiary of the mob.

> buy <index> [amount]
Buy item from the shop.

> cheat
Cheat to debug.

> clear
Clear the screen.

> clearstash
Removes all items currently in the Stash.

> collection [collection]
> collections [collection]
Display collections.

> combine <index> <index>
Combine items with anvil.

> consume <index> [amount]
> use <index> [amount]
Consume item.

> craft <recipe-name> [amount]
Craft items.

> deathcount
Displays how many times you have died.

> del <index>
> delete <index>
> rm <index>
> remove <index>
Delete items from your inventory.

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

> fish <rod-index> [iteration]
Fish for worthy.

> gather <resource> [tool-index] [iteration]
> get <resource> [tool-index] [iteration]
> mine <resource> [tool-index] [iteration]
Gather resources.

> goto <region>
Go to a region.

> help [command]
Show this message or get command description.

> hotm
Open the Heart of the Mountain menu.

> hub
Teleport you to the hub.

> info <index>
Display detailed informatioon about the item.

> item <id>
Display information of any item.

> kill <mob> [index] [iteration]
> slay <mob> [index] [iteration]
Slay mobs.

> ls
List all the items in the inventory.

> look
Get information about the region.

> merge <index> <index>
Merge stackable items in the inventory.

> minion
> minion ls
List all placed minion.

> minion claim <slot>
Claim a minion's inventory.

> minion info <slot>
Display minion inventory.

> minion place <index> <slot>
Place a minion.

> minion remove <slot>
Convert a minion to item.

> money
Display information about your money.

> move <index> <index>
> mv <index> <index>
> switch <index> <index>
Switch items slot in the inventory.

> organize
Organize your inventory.

> pet
> pet ls
List all the pets in the pet menu.

> pet add <index>
Add a pet to the pet menu.

> pet despawn
Despawn the active pet from the pet menu.

> pet info [index]
Display info about a pet.

> pet remove <index>
Remove a pet from the pet menu to your inventory.

> pet summon <index>
Summon a pet from the inventory.

> pickupstash
Takes all items currently in the Stash.

> playtime
> pt
Shows your current playtime.

> recipe [recipe-name] [--all]
> recipes [recipe-name] [--all]
Shows all recipes or recipes avaliable.

> save
Save the profile.

> sell <index-or-name>
Sell the item.

> shop [index]
Show trades in recently opened shop.

> skill [skill]
> skills [skill]
Get information about your skills.

> split <index> <index> <amount>
Split items to another slot.

> stat [stat-name] [index]
> stats [stat-name] [index]
Get information about your stats.

> talkto <npc>
Talk to an npc.

> unequip <armor-part>
Unequip armor.

> warp [island]
Warp to an island using portal or consumed travel scroll.

> warpforge
Warps you to the The Forge area in the Dwarven Mines.

> withdraw [all|half|<coins>]
Withdraw coins from the bank to the purse.
""".strip()
