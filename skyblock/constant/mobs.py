__all__ = [
    'CUBISM_EFT',
    'BLAST_PROT_EFT', 'PROJ_PROT_EFT', 'IMPALING_EFT',
    'SEA_CREATURES',
    'ZOMBIES', 'SPIDERS', 'WOLVES', 'SKELETONS', 'END_MOBS', 'ENDERMEN',
    'WITHERS', 'BLAZES', 'NETHER_MOBS', 'UNDEADS',
    'BESTIARY_ALTER',
]

CUBISM_EFT = [
    'sneaky_creeper',
    'small_emerald_slime', 'medium_emerald_slime', 'large_emerald_slime',
    'small_magma_cube', 'medium_magma_cube', 'large_magma_cube',
    'rain_slime', 'ghost',
]

BLAST_PROT_EFT = [
    'sneaky_creeper', 'large_magma_cube', 'ghast',
]

PROJ_PROT_EFT = [
    'skeleton', 'gravel_skeleton', 'watcher',
    'diamond_skeleton', 'sea_archer',
]


# # DRAGON_HUNTER
# DH_EFT

IMPALING_EFT = [
    'squid', 'night_squid',
    'sea_guardian', 'guardian_defender', 'sea_emperor',
]

SEA_CREATURES = [
    'squid', 'sea_walker', 'night_squid', 'sea_guardian', 'sea_witch',
    'sea_archer', 'monster_of_the_deep', 'catfish', 'sea_leech',
    'guardian_defender', 'deep_sea_protector', 'water_hydra', 'sea_emperor',
]

ZOMBIES = [
    'zombie', 'zombie_villager',
    'crypt_ghoul', 'golden_ghoul',
    'lapis_zombie', 'diamond_zombie',
    'redstone_pigman', 'zombie_pigman',
]

SPIDERS = [
    'splitter_spider',
    'weaver_spider',
    'voracious_spider',
    'dasher_spider',
    'spider_jockey',
]

WOLVES = [
    'wolf', 'old_wolf',
    'pack_spirit', 'howling_spirit', 'soul_of_the_alpha',
]

SKELETONS = [
    'skeleton', 'gravel_skeleton',
    'diamond_skeleton',
]

END_MOBS = [
    'enderman',
    'endermite',
    'zealot',
    'watcher',
    'obsidian_defender',
    'voidling_fanatic',
    'voidling_extremist',
]

ENDERMEN = [
    'enderman',
    'zealot',
    'voidling_fanatic',
    'voidling_extremist',
]

WITHERS = [
    'wither_skeleton',
]

BLAZES = [
    'ashfang', 'bezal', 'blaze', 'flare', 'millenia_aged_blaze',
    'mutated_blaze', 'smoldering_blaze',
]

NETHER_MOBS = [
    'ashfang', 'barbarian', 'barbarian_duke_x', 'bezal', 'bladesoul', 'blaze', 'dive_ghast',
    'fire_mage', 'flaming_spider', 'flare', 'ghast', 'goliath_barbarian', 'kada_knight',
    'krondor_necromancer', 'mage_outlaw', 'magma_cube_boss', 'magma_cube_rider', 'magma_cube',
    'millenia_aged_blaze', 'mushroom_bull', 'mutated_blaze', 'smoldering_blaze', 'vanquisher',
    'wither_skeleton', 'wither_spectre',
]

UNDEADS = ZOMBIES + SKELETONS + WITHERS

BESTIARY_ALTER = {
    'crypt_ghoul': ('crypt_ghoul', 'golden_ghoul'),
    'blaze': ('blaze', 'mini_blaze'),
    'magma_cube': ('small_magma_cube',
                   'medium_magma_cube',
                   'large_magma_cube'),
    'emerald_slime': ('small_emerald_slime',
                      'medium_emerald_slime',
                      'large_emerald_slime'),
    'miner_zombie': ('diamond_zombie',),
    'miner_skeleton': ('diamond_skeleton',),
}
