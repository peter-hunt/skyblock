from ...object import *


__all__ = ['FARMING_ARMOR']

FARMING_ARMOR = [
    Armor('farm_suit_helmet', rarity='common', part='helmet',
          defense=15,
          abilities=['farm_suit_speed']),
    Armor('farm_suit_chestplate', rarity='common', part='chestplate',
          defense=40,
          abilities=['farm_suit_speed']),
    Armor('farm_suit_leggings', rarity='common', part='leggings',
          defense=30,
          abilities=['farm_suit_speed']),
    Armor('farm_suit_boots', rarity='common', part='boots',
          defense=15,
          abilities=['farm_suit_speed']),

    Armor('farm_helmet', rarity='rare', part='helmet',
          health=20, defense=40,
          abilities=['farm_armor_speed']),
    Armor('farm_chestplate', rarity='rare', part='chestplate',
          health=20, defense=75,
          abilities=['farm_armor_speed']),
    Armor('farm_leggings', rarity='rare', part='leggings',
          health=20, defense=50,
          abilities=['farm_armor_speed']),
    Armor('farm_boots', rarity='rare', part='boots',
          health=20, defense=35,
          abilities=['farm_armor_speed']),

    Armor('pumpkin_helmet', rarity='common', part='helmet',
          health=8, defense=8,
          abilities=['pumpkin_buff']),
    Armor('pumpkin_chestplate', rarity='common', part='chestplate',
          health=14, defense=14,
          abilities=['pumpkin_buff']),
    Armor('pumpkin_leggings', rarity='common', part='leggings',
          health=10, defense=10,
          abilities=['pumpkin_buff']),
    Armor('pumpkin_boots', rarity='common', part='boots',
          health=8, defense=8,
          abilities=['pumpkin_buff']),

    Armor('farmer_boots', rarity='uncommon', part='boots',
          health=40, defense=20, speed=10),
    Armor('ranchers_boots', rarity='rare', part='boots',
          health=100, defense=70, speed=50),

    Armor('mushroom_helmet', rarity='common', part='helmet',
          health=20),
    Armor('mushroom_chestplate', rarity='common', part='chestplate',
          health=10, defense=10),
    Armor('mushroom_leggings', rarity='common', part='leggings',
          health=10, defense=5),
    Armor('mushroom_boots', rarity='common', part='boots',
          health=15),

    Armor('cactus_helmet', rarity='common', part='helmet',
          health=5, defense=10,
          abilities=['deflect']),
    Armor('cactus_chestplate', rarity='common', part='chestplate',
          health=15, defense=25,
          abilities=['deflect']),
    Armor('cactus_leggings', rarity='common', part='leggings',
          health=10, defense=20,
          abilities=['deflect']),
    Armor('cactus_boots', rarity='common', part='boots',
          health=5, defense=10,
          abilities=['deflect']),

    Armor('speedster_helmet', rarity='epic', part='helmet',
          defense=70, speed=15,
          abilities=['speester_bonus']),
    Armor('speedster_chestplate', rarity='epic', part='chestplate',
          defense=120, speed=15,
          abilities=['speester_bonus']),
    Armor('speedster_leggings', rarity='epic', part='leggings',
          defense=95, speed=15,
          abilities=['speester_bonus']),
    Armor('speedster_boots', rarity='epic', part='boots',
          defense=65, speed=15,
          abilities=['speester_bonus']),

    Armor('cow_head', rarity='common', part='helmet',
          health=15, defense=5),
]
