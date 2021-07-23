# Skyblock Beta
![](https://img.shields.io/github/repo-size/peter-hunt/skyblock)
![](https://img.shields.io/github/license/peter-hunt/skyblock)
![](https://img.shields.io/github/issues/peter-hunt/skyblock)
![](https://img.shields.io/github/stars/peter-hunt/skyblock)


Hypixel Skyblock Remake in Python.
(only support Ironman mode for now)

Requires Skyblock-Data repo, [Skyblock Data](https://github.com/peter-hunt/skyblock-data), which will install automatically.

The data required will be auto-cached, and it will auto-update every 12 hours.

The project is in Beta cause there is no Alpha!

# Warning!
This project is still in heavy development, so the data structures used for caching and saving data will change. If you'd like to play this game in Beta, and your saved files get out of data or just from strange bugs, your files will corrupt.

If your data folder corrupts, delete the whole `~/skyblock/data` folder to let the program fix it.
If your saved files go corrupt, then it's probably not going to be resolved. Maybe I'll implement better usage, but the profile isn't like going to work again.

# Installation
Use pip or git to install Skyblock.

Use pip to install the project straight as an executable library.

```bash
pip install git+https://github.com/peter-hunt/skyblock.git
```

Or, if you want to install from the source, use git to clone the source code.

```bash
git clone https://github.com/peter-hunt/skyblock.git
```

To install the library from the source, go into the directory and:

```bash
python setup.py install
```

This project requires Python 3.8+

## Usage
```bash
python -m skyblock
```

# Content
## Added Features:
* Abilities
* Accessories
* Armor Pieces, Tools, and Weapons
* Bestiaries and Bestiary Milestones
* Crafting
* Collections
* Combining Enchantments, Reforge Stone, and Potato Books
* Farming, Mining, Simple Combat, Foraging, Fishing, and Enchanting
* Fast Traveling
* NPC Buying and Trading items
* Minions
* Modifiers and Reforging
* Pets
* Skills

## Features Planned:
* Bestiary Milestones
* Combat while Mining
* Commissions
* Dungeons
* Fairy Souls
* Forging (Dwarven Mines)
* HoTM Skill Tree (Dwarven Mines)
* Milestone Pets
* Minion Support Items
* NPC Usage (like Kat, Fetchur, etc.)
* Pet Items
* Pet Score

# Furthur information
This project is a clone of [Hypixel Skyblock](https://hypixel-skyblock.fandom.com/wiki/Hypixel_SkyBlock_Wiki)

# License
[MIT](LICENSE.txt)
