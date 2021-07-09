from ...object import *


__all__ = ['MISC_ARMOR']

MISC_ARMOR = [
    Armor('leather_helmet', rarity='common', part='helmet',
          defense=5),
    Armor('leather_chestplate', rarity='common', part='chestplate',
          defense=15),
    Armor('leather_leggings', rarity='common', part='leggings',
          defense=10),
    Armor('leather_boots', rarity='common', part='boots',
          defense=5),

    Armor('golden_helmet', rarity='common', part='helmet',
          defense=10),
    Armor('golden_chestplate', rarity='common', part='chestplate',
          defense=25),
    Armor('golden_leggings', rarity='common', part='leggings',
          defense=15),
    Armor('golden_boots', rarity='common', part='boots',
          defense=5),

    Armor('chainmail_helmet', rarity='uncommon', part='helmet',
          defense=12),
    Armor('chainmail_chestplate', rarity='uncommon', part='chestplate',
          defense=30),
    Armor('chainmail_leggings', rarity='uncommon', part='leggings',
          defense=20),
    Armor('chainmail_boots', rarity='uncommon', part='boots',
          defense=7),

    Armor('iron_helmet', rarity='common', part='helmet',
          defense=10),
    Armor('iron_chestplate', rarity='common', part='chestplate',
          defense=30),
    Armor('iron_leggings', rarity='common', part='leggings',
          defense=25),
    Armor('iron_boots', rarity='common', part='boots',
          defense=10),

    Armor('diamond_helmet', rarity='uncommon', part='helmet',
          defense=15),
    Armor('diamond_chestplate', rarity='uncommon', part='chestplate',
          defense=40),
    Armor('diamond_leggings', rarity='uncommon', part='leggings',
          defense=30),
    Armor('diamond_boots', rarity='uncommon', part='boots',
          defense=15),

    Armor('cheap_tuxedo_jacket', rarity='epic', part='chestplate',
          crit_damage=50, intelligence=50),
    Armor('cheap_tuxedo_pants', rarity='epic', part='leggings',
          crit_damage=25, intelligence=25),
    Armor('cheap_tuxedo_oxfords', rarity='epic', part='boots',
          crit_damage=25, intelligence=25),

    Armor('fancy_tuxedo_jacket', rarity='legendary', part='chestplate',
          crit_damage=80, intelligence=150),
    Armor('fancy_tuxedo_pants', rarity='legendary', part='leggings',
          crit_damage=35, intelligence=75),
    Armor('fancy_tuxedo_oxfords', rarity='legendary', part='boots',
          crit_damage=35, intelligence=75),

    Armor('elegant_tuxedo_jacket', rarity='legendary', part='chestplate',
          crit_damage=100, intelligence=300),
    Armor('elegant_tuxedo_pants', rarity='legendary', part='leggings',
          crit_damage=50, intelligence=100),
    Armor('elegant_tuxedo_oxfords', rarity='legendary', part='boots',
          crit_damage=50, intelligence=100, speed=10),
]
