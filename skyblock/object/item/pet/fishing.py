from ...object import *


__all__ = ['FISHING_PETS']

FISHING_PETS = [
    Pet('baby_yeti_pet', rarity='epic', category='fishing',
        intelligence=75, strength=40),
    Pet('baby_yeti_pet', rarity='legendary', category='fishing',
        intelligence=75, strength=40),

    Pet('blue_whale_pet', rarity='common', category='fishing',
        health=200),
    Pet('blue_whale_pet', rarity='uncommon', category='fishing',
        health=200),
    Pet('blue_whale_pet', rarity='rare', category='fishing',
        health=200),
    Pet('blue_whale_pet', rarity='epic', category='fishing',
        health=200),
    Pet('blue_whale_pet', rarity='legendary', category='fishing',
        health=200,
        abilities=['archimedes']),

    Pet('dolphin_pet', rarity='common', category='fishing',
        intelligence=100, sea_creature_chance=5),
    Pet('dolphin_pet', rarity='uncommon', category='fishing',
        intelligence=100, sea_creature_chance=5),
    Pet('dolphin_pet', rarity='rare', category='fishing',
        intelligence=100, sea_creature_chance=5,
        abilities=['rare_echolocation']),
    Pet('dolphin_pet', rarity='epic', category='fishing',
        intelligence=100, sea_creature_chance=5,
        abilities=['epic_echolocation']),
    Pet('dolphin_pet', rarity='legendary', category='fishing',
        intelligence=100, sea_creature_chance=5,
        abilities=['epic_echolocation']),

    Pet('flying_fish_pet', rarity='rare', category='fishing',
        health=40, defense=40),
    Pet('flying_fish_pet', rarity='epic', category='fishing',
        health=40, defense=40),
    Pet('flying_fish_pet', rarity='legendary', category='fishing',
        health=40, defense=40),

    Pet('megalodon_pet', rarity='epic', category='fishing',
        strength=50, magic_find=10, ferocity=5),
    Pet('megalodon_pet', rarity='legendary', category='fishing',
        strength=50, magic_find=10, ferocity=5),

    Pet('squid_pet', rarity='common', category='fishing',
        health=50, intelligence=50),
    Pet('squid_pet', rarity='uncommon', category='fishing',
        health=50, intelligence=50),
    Pet('squid_pet', rarity='rare', category='fishing',
        health=50, intelligence=50),
    Pet('squid_pet', rarity='epic', category='fishing',
        health=50, intelligence=50),
    Pet('squid_pet', rarity='legendary', category='fishing',
        health=50, intelligence=50),
]
