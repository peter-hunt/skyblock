__all__ = [
    'CUBISM_EFT', 'ENDER_SLAYER_EFT', 'BOA_EFT', 'SMITE_EFT',
    'BLAST_PROT_EFT', 'PROJ_PROT_EFT', 'IMPALING_EFT',
    'SEA_CREATURES', 'ZOMBIES', 'SKELETONS',
    'BESTIARY_ALTER',
]

CUBISM_EFT = [
    'sneaky_creeper',
    'small_emerald_slime', 'medium_emerald_slime', 'large_emerald_slime',
    'small_magma_cube', 'medium_magma_cube', 'large_magma_cube',
    'rain_slime', 'ghost',
]

ENDER_SLAYER_EFT = [
    'enderman',
    'zealot',
    'voidling_fanatic',
    'voidling_extremist',
]

# BANE_OF_ARTHROPODS
BOA_EFT = [
    'splitter_spider',
    'weaver_spider',
    'voracious_spider',
    'dasher_spider',
    'spider_jockey',
]

BLAST_PROT_EFT = [
    'sneaky_creeper', 'large_magma_cube', 'ghast',
]

PROJ_PROT_EFT = [
    'skeleton', 'gravel_skeleton', 'watcher',
    'diamond_skeleton', 'sea_archer',
]

SMITE_EFT = [
    'zombie', 'zombie_villager', 'skeleton',
    'gravel_skeleton',
    'crypt_ghoul', 'golden_ghoul',
    'lapis_zombie',
    'redstone_pigman',
    'diamond_zombie', 'diamond_skeleton',
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
]

SKELETONS = [
    'skeleton', 'gravel_skeleton',
    'diamond_skeleton',
]


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
