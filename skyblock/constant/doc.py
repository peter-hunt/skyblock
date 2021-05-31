__all__ = ['menu_doc', 'profile_doc']

menu_doc = """
> help [command]
Show this message or get command description.

> exit
> quit
Exit the menu.

> create
> new
> touch
Create a new profile.

> list
> ls
List all the profile avaliable.

> del <name>
> delete <name>
Delete a profile.

> load <name>
> open <name>
> start <name>
Load a profile and run it.
""".strip()

profile_doc = """
> exit
> quit
Exit to the menu.

> help [command]
Show this message or get command description.

> inv
> inventory
> list
> ls
List all the items in the inventory.

> info <index>
> information <index>
Display detailed informatioon about the item.

> look
Get information about the region.

> money
Display information about your money.

> deposit <coins>
Deposit coins from the purse to the bank.

> withdraw <coins>
Withdraw coins from the bank to the purse.

> goto <location>
Go to a region.

> get <resource> [amount=1] [tool=hand]
Get resources for an amount with chosen tool or hand by default.

> sell <index>
Sell the item.

> merge <from-index> <to-index>
Merge stackable items in the inventory.

> move <index-1> <index-2>
> switch <index-1> <index-2>
Switch items slot in the inventory.

> split <from-index> <to-index> <amount>
Split items to another slot.

> pickupstash
Pick up items from stash.

> talkto <npc>
Talk to an npc.
""".strip()
