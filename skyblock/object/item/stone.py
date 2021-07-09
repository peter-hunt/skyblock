from ...function.io import *

from ..object import *


__all__ = ['REFORGE_STONES', 'get_stone']

REFORGE_STONES = [
    ReforgeStone('dirt_bottle', 'dirty', 'melee', 'rare',
                 (1000, 5000, 10000, 15000, 50000, 75000),
                 mining_skill_req=10),
    ReforgeStone('dragon_claw', 'fabled', 'melee', 'rare',
                 (60000, 125000, 250000, 500000, 1000000, 2000000),
                 mining_skill_req=22),
    ReforgeStone('suspicious_vial', 'suspicious', 'melee', 'rare',
                 (60000, 125000, 250000, 500000, 1000000, 2000000),
                 mining_skill_req=23),
    ReforgeStone('wither_blood', 'withered', 'melee', 'epic',
                 (10000, 20000, 30000, 40000, 50000, 60000),
                 mining_skill_req=30),

    ReforgeStone('optical_lens', 'precise', 'bow', 'rare',
                 (30000, 75000, 150000, 300000, 600000, 1200000),
                 mining_skill_req=22),
    ReforgeStone('spirit_stone', 'spiritual', 'bow', 'rare',
                 (60000, 125000, 250000, 500000, 1000000, 2000000),
                 mining_skill_req=24),
    ReforgeStone('salmon_opal', 'headstrong', 'bow', 'rare',
                 (15000, 30000, 60000, 125000, 250000, 500000),
                 mining_skill_req=15),

    ReforgeStone('diamond_atom', 'perfect', 'armor', 'rare',
                 (25000, 50000, 150000, 300000, 600000, 800000),
                 mining_skill_req=22),
    ReforgeStone('necromancers_brooch', 'necrotic', 'armor', 'rare',
                 (20000, 40000, 80000, 150000, 300000, 600000),
                 mining_skill_req=19),
    ReforgeStone('precursor_gear', 'ancient', 'armor', 'epic',
                 (10000, 20000, 30000, 40000, 50000, 60000),
                 mining_skill_req=30),
    ReforgeStone('dragon_scale', 'spiked', 'armor', 'rare',
                 (30000, 75000, 150000, 300000, 600000, 1200000),
                 mining_skill_req=20),
    ReforgeStone('dragon_horn', 'renowned', 'armor', 'epic',
                 (60000, 125000, 250000, 500000, 1000000, 2000000),
                 mining_skill_req=25),
    ReforgeStone('molten_cube', 'cubic', 'armor', 'rare',
                 (4000, 7500, 15000, 40000, 75000, 150000),
                 mining_skill_req=10),
    ReforgeStone('end_stone_geode', 'warped', 'armor', 'rare',
                 (5000, 10000, 20000, 50000, 100000, 200000),
                 mining_skill_req=24),
    ReforgeStone('rare_diamond', 'reinforced', 'armor', 'rare',
                 (2500, 5000, 10000, 25000, 50000, 100000),
                 mining_skill_req=8),
    ReforgeStone('giant_tooth', 'giant', 'armor', 'epic',
                 (60000, 125000, 250000, 500000, 1000000, 2000000),
                 mining_skill_req=25),
    ReforgeStone('deep_sea_orb', 'submerged', 'armor', 'epic',
                 (50000, 150000, 300000, 600000, 750000, 800000),
                 mining_skill_req=25),
]


def get_stone(name: str) -> ReforgeStone:
    for stone in REFORGE_STONES:
        if name == stone.name:
            return stone
    red(f'Reforge Stone not found: {name!r}')
