from ...object import Armor


__all__ = ['ADMIN_ARMOR']

ADMIN_ARMOR = [
    Armor('anubis', rarity='legendary', part='helmet',
          health=3000),

    Armor('titans_helmet', rarity='legendary', part='helmet',
          strength=10, health=150, defense=100, intelligence=50),
    Armor('titans_chestplate', rarity='legendary', part='chestplate',
          strength=20, health=300, defense=200, intelligence=75),
    Armor('titans_leggings', rarity='legendary', part='leggings',
          strength=15, health=200, defense=175, intelligence=50),
    Armor('titans_boots', rarity='legendary', part='boots',
          strength=10, health=150, defense=100, intelligence=50),

    Armor('boss', rarity='legendary', part='helmet',
          health=1000, defense=1000, speed=60),

    Armor('kindred', rarity='legendary', part='helmet',
          speed=70),

    Armor('the_fast', rarity='legendary', part='helmet',
          speed=300),

    Armor('helmet_of_the_stars', rarity='legendary', part='helmet',
          health=10000, defense=3000, intelligence=1000),
    Armor('chestplate_of_the_stars', rarity='legendary', part='chestplate',
          health=20000, defense=5000, intelligence=2000),
    Armor('leggings_of_the_stars', rarity='legendary', part='leggings',
          health=15000, defense=4000, intelligence=1500),
    Armor('boots_of_the_stars', rarity='legendary', part='boots',
          health=7500, defense=2500, intelligence=1000),

    Armor('arenjey_god', rarity='special', part='helmet',
          magic_find=1000),
]
