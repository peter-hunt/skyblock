from ...object import Armor


__all__ = ['FISHING_ARMOR']

FISHING_ARMOR = [
    Armor('fairys_fedora', rarity='uncommon', part='helmet',
          health=1, defense=1, intelligence=-1, speed=10,
          abilities=['fairys_outfit']),
    Armor('fairys_polo', rarity='uncommon', part='chestplate',
          health=1, defense=1, intelligence=-1, speed=10,
          abilities=['fairys_outfit']),
    Armor('fairys_trousers', rarity='uncommon', part='leggings',
          health=1, defense=1, intelligence=-1, speed=10,
          abilities=['fairys_outfit']),
    Armor('fairys_galoshes', rarity='uncommon', part='boots',
          health=1, defense=1, intelligence=-1, speed=10,
          abilities=['fairys_outfit']),

    Armor('squid_boots', rarity='uncommon', part='boots',
          health=100, sea_creature_chance=1.5),

    Armor('water_hydra_head', rarity='epic', part='helmet',
          health=100, defense=100, sea_creature_chance=1.8),

    Armor('divers_mask', rarity='legendary', part='helmet',
          health=120, defense=65, sea_creature_chance=2),
    Armor('divers_shirt', rarity='legendary', part='chestplate',
          health=100, defense=200, sea_creature_chance=2),
    Armor('divers_trunks', rarity='legendary', part='leggings',
          health=75, defense=170, sea_creature_chance=2),
    Armor('divers_boots', rarity='legendary', part='boots',
          health=60, defense=110, sea_creature_chance=2),

    Armor('fish_hat', rarity='common', part='helmet',
          health=5),

    Armor('angler_helmet', rarity='common', part='helmet',
          defense=15, sea_creature_chance=1),
    Armor('angler_chestplate', rarity='common', part='chestplate',
          defense=40, sea_creature_chance=1),
    Armor('angler_leggings', rarity='common', part='leggings',
          defense=30, sea_creature_chance=1),
    Armor('angler_boots', rarity='common', part='boots',
          defense=15, sea_creature_chance=1),

    Armor('salmon_helmet', rarity='common', part='helmet',
          health=35, defense=80, sea_creature_chance=1.5),
    Armor('salmon_chestplate', rarity='common', part='chestplate',
          health=130, defense=55, sea_creature_chance=1.5),
    Armor('salmon_leggings', rarity='common', part='leggings',
          health=105, defense=30, sea_creature_chance=1.5),
    Armor('salmon_boots', rarity='common', part='boots',
          health=60, defense=25, sea_creature_chance=1.5),

    Armor('clownfish_hat', rarity='uncommon', part='helmet',
          intelligence=50),

    Armor('pufferfish_hat', rarity='common', part='helmet',
          health=20, strength=10),

    Armor('guardian_chestplate', rarity='rare', part='chestplate',
          health=20, defense=50),

    Armor('blobfish_hat', rarity='common', part='helmet',
          strength=25, intelligence=-10),

    Armor('squid_hat', rarity='common', part='helmet',
          speed=1),

    Armor('stereo_pants', rarity='epic', part='leggings',
          defense=35),

    Armor('sponge_helmet', rarity='epic', part='helmet',
          defense=80, sea_creature_chance=1.8),
    Armor('sponge_chestplate', rarity='epic', part='chestplate',
          defense=145, sea_creature_chance=1.8),
    Armor('sponge_leggings', rarity='epic', part='leggings',
          defense=100, sea_creature_chance=1.8),
    Armor('sponge_boots', rarity='epic', part='boots',
          defense=60, sea_creature_chance=1.8),
]
