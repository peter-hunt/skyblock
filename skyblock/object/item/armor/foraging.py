from ...object import *


__all__ = ['FORAGING_ARMOR']

FORAGING_ARMOR = [
    Armor('leaflet_helmet', rarity='common', part='helmet',
          health=20),
    Armor('leaflet_chestplate', rarity='common', part='chestplate',
          health=35),
    Armor('leaflet_leggings', rarity='common', part='leggings',
          health=30),
    Armor('leaflet_boots', rarity='common', part='boots',
          health=15),

    Armor('growth_helmet', rarity='rare', part='helmet',
          health=50, defense=30),
    Armor('growth_chestplate', rarity='rare', part='chestplate',
          health=100, defense=50),
    Armor('growth_leggings', rarity='rare', part='leggings',
          health=80, defense=40),
    Armor('growth_boots', rarity='rare', part='boots',
          health=50, defense=25),
]
