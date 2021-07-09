from ...object import *


__all__ = ['FISHING_RODS']

FISHING_RODS = [
    FishingRod('fishing_rod', rarity='common'),
    FishingRod('prismarine_rod', rarity='common',
               damage=15, strength=10, fishing_speed=10,
               fishing_skill_req=3),
    FishingRod('sponge_rod', rarity='common',
               damage=20, strength=15,
               fishing_speed=20,
               fishing_skill_req=5),
    FishingRod('speedster_rod', rarity='uncommon',
               damage=30, strength=15, fishing_speed=30,
               fishing_skill_req=6),

    FishingRod('farmers_rod', rarity='uncommon',
               damage=50, strength=20, fishing_speed=40,
               fishing_skill_req=8),
    FishingRod('challenging_rod', rarity='rare',
               damage=60, strength=60,
               fishing_speed=50, sea_creature_chance=2,
               fishing_skill_req=10),
    FishingRod('rod_of_champions', rarity='rare',
               damage=90, strength=80,
               fishing_speed=60, sea_creature_chance=4,
               fishing_skill_req=15),
    FishingRod('rod_of_legends', rarity='rare',
               damage=130, strength=120,
               fishing_speed=70, sea_creature_chance=6,
               fishing_skill_req=20),

    FishingRod('shredder', rarity='legendary',
               damage=120, ferocity=50, fishing_speed=75,
               fishing_skill_req=20),
]
