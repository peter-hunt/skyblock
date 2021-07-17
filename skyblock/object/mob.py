from typing import Optional

from ..function.io import *
from ..function.util import get, includes

from .item import get_item
from .object import *


__all__ = ['MOBS', 'get_mob']

MOBS = [
    Mob('zombie', level=1, health=100, damage=20,
        coins=1, exp=1, combat_exp=6,
        drops=[
            (Item('rotten_flesh'), 1, 'common', 1),
            (Item('poisonous_potato'), 1, 'uncommon', 0.02),
            (Item('potato'), 1, 'rare', 0.01),
            (Item('carrot'), 1, 'rare', 0.01),
        ]),
    Mob('zombie_villager', level=1, health=120, damage=24,
        coins=1, exp=2, combat_exp=7,
        drops=[
            (Item('rotten_flesh'), 1, 'common', 1),
            (Item('poisonous_potato'), 1, 'uncommon', 0.02),
            (Item('potato'), 1, 'rare', 0.01),
            (Item('carrot'), 1, 'rare', 0.01),
        ]),
    Mob('skeleton', level=6, health=200, damage=47,
        coins=2, exp=4, combat_exp=6,
        drops=[
            (Item('bone'), 2, 'common', 1),
        ]),
    Mob('crypt_ghoul', level=30, health=2000, damage=200,
        coins=13, exp=30, combat_exp=32,
        drops=[
            (Item('rotten_flesh'), (1, 2), 'common', 1),
            (get_item('ghoul_pet', rarity='epic'),
             1, 'pray_rngesus', 0.00003),
            (get_item('ghoul_pet', rarity='legendary'),
             1, 'pray_rngesus', 0.00001),
        ]),
    Mob('golden_ghoul', level=60, health=45000, damage=500,
        coins=100, exp=30, combat_exp=50,
        drops=[
            (Item('rotten_flesh'), 2, 'common', 1),
            (Item('gold'), (1, 10), 'common', 1),
            (Item('golden_powder'), 1, 'legendary', 0.0005),
        ]),
    Mob('wolf', level=15, health=250, damage=80,
        coins=1, exp=4, combat_exp=10,
        drops=[
            (Item('bone'), 1, 'common', 1),
            (get_item('hound_pet', rarity='epic'),
             1, 'pray_rngesus', 0.00001),
            (get_item('hound_pet', rarity='legendary'),
             1, 'pray_rngesus', 0.000003),
        ]),
    Mob('old_wolf', level=50, health=15000, damage=720,
        coins=40, exp=4, combat_exp=40,
        drops=[
            (Item('bone'), 1, 'common', 1),
            (get_item('hound_pet', rarity='epic'),
             1, 'pray_rngesus', 0.00001),
            (get_item('hound_pet', rarity='legendary'),
             1, 'pray_rngesus', 0.000003),
        ]),

    Mob('chicken', level=1, health=4, damage=0,
        coins=0, exp=2, farming_exp=2,
        drops=[
            (Item('chicken'), 1, 'common', 1),
            (Item('feather'), (1, 2), 'common', 2 / 3),
            (Item('egg'), 1, 'common', 1 / 4),
        ]),
    Mob('cow', level=1, health=10, damage=0,
        coins=0, exp=2, farming_exp=2,
        drops=[
            (Item('beef'), (1, 3), 'common', 1),
            (Item('leather'), (1, 2), 'common', 2 / 3),
        ]),
    Mob('mooshroom', level=1, health=10, damage=0,
        coins=0, exp=2, farming_exp=2,
        drops=[
            (Item('beef'), (1, 3), 'common', 1),
            (Item('leather'), (1, 2), 'common', 2 / 3),
            (Item('mushroom'), (1, 3), 'common', 1),
        ]),
    Mob('pig', level=1, health=10, damage=0,
        coins=0, exp=2, farming_exp=2,
        drops=[
            (Item('pork'), (1, 3), 'common', 1),
        ]),
    Mob('sheep', level=1, health=8, damage=0,
        coins=0, exp=2, farming_exp=2,
        drops=[
            (Item('mutton'), (1, 2), 'common', 1),
            (Item('wool'), 1, 'common', 1),
        ]),
    Mob('rabbit', level=10, health=125, damage=0,
        coins=0, exp=2, farming_exp=2,
        drops=[
            (Item('rabbit'), 1, 'common', 0.6),
            (Item('rabbit_hide'), 1, 'common', 0.3),
            (Item('rabbit_foot'), 1, 'uncommon', 0.1),
        ]),

    Mob('dasher_spider', level=4, health=160, damage=55,
        coins=2, exp=8, combat_exp=10,
        drops=[
            (Item('string'), 1, 'common', 1),
            (Item('spider_eye'), 1, 'common', 0.5),
            (get_item('travel_scroll_to_nest'), 1, 'legendary', 0.0002),
            (get_item('tarantula_pet', rarity='epic'),
             1, 'pray_rngesus', 0.0001),
            (get_item('tarantula_pet', rarity='legendary'),
             1, 'pray_rngesus', 0.0001),
        ]),
    Mob('dasher_spider', level=42, health=5000, damage=240,
        coins=10, exp=10, combat_exp=28,
        drops=[
            (Item('string'), 1, 'common', 1),
            (Item('spider_eye'), 1, 'common', 0.5),
            (get_item('travel_scroll_to_nest'), 1, 'legendary', 0.0002),
            (get_item('tarantula_pet', rarity='epic'),
             1, 'pray_rngesus', 0.0001),
            (get_item('tarantula_pet', rarity='legendary'),
             1, 'pray_rngesus', 0.0001),
        ]),
    Mob('dasher_spider', level=45, health=6000, damage=580,
        coins=12, exp=10, combat_exp=30,
        drops=[
            (Item('string'), 1, 'common', 1),
            (Item('spider_eye'), 1, 'common', 0.5),
            (get_item('travel_scroll_to_nest'), 1, 'legendary', 0.0002),
            (get_item('tarantula_pet', rarity='epic'),
             1, 'pray_rngesus', 0.0001),
            (get_item('tarantula_pet', rarity='legendary'),
             1, 'pray_rngesus', 0.0001),
        ]),
    Mob('dasher_spider', level=50, health=7000, damage=720,
        coins=15, exp=10, combat_exp=36,
        drops=[
            (Item('string'), 1, 'common', 1),
            (Item('spider_eye'), 1, 'common', 0.5),
            (get_item('travel_scroll_to_nest'), 1, 'legendary', 0.0002),
            (get_item('tarantula_pet', rarity='epic'),
             1, 'pray_rngesus', 0.0001),
            (get_item('tarantula_pet', rarity='legendary'),
             1, 'pray_rngesus', 0.0001),
        ]),
    Mob('spider_jockey', level=5, health=530, damage=93,
        coins=7, exp=10, combat_exp=14,
        drops=[
            (Item('string'), (1, 2), 'common', 1),
            (Item('bone'), 2, 'common', 1),
            (Item('spider_eye'), 1, 'uncommon', 0.1),
            (get_item('bow'), 1, 'rare', 0.02),
        ]),
    Mob('weaver_spider', level=3, health=160, damage=35,
        coins=2, exp=2, combat_exp=9,
        drops=[
            (Item('string'), 1, 'common', 1),
            (Item('spider_eye'), 1, 'uncommon', 0.1),
        ]),
    Mob('weaver_spider', level=5, health=200, damage=45,
        coins=2, exp=2, combat_exp=8,
        drops=[
            (Item('string'), 1, 'common', 1),
            (Item('spider_eye'), 1, 'uncommon', 0.1),
        ]),
    Mob('voracious_spider', level=10, health=1000, damage=100,
        coins=2, exp=3, combat_exp=10,
        drops=[
            (Item('string'), 1, 'common', 1),
            (Item('spider_eye'), 1, 'uncommon', 0.1),
        ]),
    Mob('voracious_spider', level=42, health=5000, damage=244,
        coins=8, exp=8, combat_exp=28,
        drops=[
            (Item('string'), 1, 'common', 1),
            (Item('spider_eye'), 1, 'uncommon', 0.1),
        ]),
    Mob('voracious_spider', level=45, health=7000, damage=648,
        coins=12, exp=9, combat_exp=30,
        drops=[
            (Item('string'), 1, 'common', 1),
            (Item('spider_eye'), 1, 'uncommon', 0.1),
        ]),
    Mob('voracious_spider', level=50, health=7000, damage=648,
        coins=15, exp=10, combat_exp=36,
        drops=[
            (Item('string'), 1, 'common', 1),
            (Item('spider_eye'), 1, 'uncommon', 0.1),
        ]),
    Mob('splitter_spider', level=2, health=180, damage=25,
        coins=2, exp=2, combat_exp=8,
        drops=[
            (Item('string'), (1, 2), 'common', 1),
            (Item('spider_eye'), 1, 'uncommon', 0.1),
        ]),
    Mob('gravel_skeleton', level=2, health=100, damage=33,
        coins=1, exp=4, combat_exp=6,
        drops=[
            (Item('bone'), (3, 6), 'common', 1),
        ]),
    Mob('rain_slime', level=8, health=200, damage=100,
        coins=5, exp=3, combat_exp=4,
        drops=[
            (Item('slime_ball'), 1, 'common', 1),
        ]),

    Mob('small_magma_cube', level=3, health=200, damage=70,
        coins=3, exp=7, combat_exp=4,
        drops=[
            (Item('magma_cream'), 1, 'common', 1),
        ]),
    Mob('medium_magma_cube', level=6, health=250, damage=120,
        coins=4, exp=9, combat_exp=4,
        drops=[
            (Item('magma_cream'), 1, 'common', 1),
        ]),
    Mob('large_magma_cube', level=9, health=300, damage=150,
        coins=4, exp=20, combat_exp=4,
        drops=[
            (Item('magma_cream'), (1, 3), 'common', 1),
            (get_item('magma_cube_pet', rarity='common'),
             1, 'rare', 0.01),
            (get_item('magma_cube_pet', rarity='uncommon'),
             1, 'legendary', 0.0005),
            (get_item('magma_cube_pet', rarity='rare'),
             1, 'pray_rngesus', 0.0001),
        ]),
    Mob('mini_blaze', level=12, health=500, damage=120,
        coins=5, exp=30, combat_exp=10,
        drops=[
            (Item('blaze_rod'), 1, 'common', 1),
        ]),
    Mob('blaze', level=15, health=600, damage=150,
        coins=10, exp=35, combat_exp=10,
        drops=[
            (Item('blaze_rod'), 2, 'common', 1),
            (get_item('blaze_hat'), 1, 'uncommon', 0.05),
        ]),
    Mob('wither_skeleton', level=10, health=250, damage=152,
        coins=4, exp=15, combat_exp=13,
        drops=[
            (Item('bone'), 3, 'common', 1),
            (Item('coal'), 1, 'common', 0.5),
            (Item('enchanted_coal'), 1, 'rare', 0.01),
        ]),
    Mob('zombie_pigman', level=12, health=240, damage=125,
        coins=4, exp=25, combat_exp=15,
        drops=[
            (Item('gold_nugget'), 2, 'common', 1),
            (get_item('flaming_sword'), 1, 'uncommon', 0.03),
        ]),
    Mob('ghast', level=17, health=330, damage=150,
        coins=30, exp=32, combat_exp=50,
        drops=[
            (Item('ghast_tear'), 1, 'common', 1),
        ]),

    Mob('enderman', level=42, health=4500, damage=500,
        coins=10, exp=8, combat_exp=40.8,
        drops=[
            (Item('ender_pearl'), (1, 3), 'common', 1),
            (Item('enchanted_ender_pearl'), 1, 'rare', 0.01),
            (get_item('enderman_pet', rarity='common'),
             1, 'legendary', 0.0005),
            (get_item('enderman_pet', rarity='uncommon'),
             1, 'legendary', 0.0002),
            (get_item('enderman_pet', rarity='rare'),
             1, 'pray_rngesus', 0.0001),
            (get_item('ender_helmet'), 1, 'legendary', 0.00025),
            (get_item('ender_chestplate'), 1, 'legendary', 0.00025),
            (get_item('ender_leggings'), 1, 'legendary', 0.00025),
            (get_item('ender_helmet'), 1, 'legendary', 0.00025),
        ]),
    Mob('enderman', level=45, health=6000, damage=600,
        coins=12, exp=9, combat_exp=40.8,
        drops=[
            (Item('ender_pearl'), (1, 3), 'common', 1),
            (Item('enchanted_ender_pearl'), 1, 'rare', 0.01),
            (get_item('enderman_pet', rarity='uncommon'),
             1, 'legendary', 0.0005),
            (get_item('enderman_pet', rarity='rare'),
             1, 'legendary', 0.0002),
            (get_item('enderman_pet', rarity='epic'),
             1, 'pray_rngesus', 0.0001),
            (get_item('ender_helmet'), 1, 'legendary', 0.00025 / 3),
            (get_item('ender_chestplate'), 1, 'legendary', 0.00025 / 3),
            (get_item('ender_leggings'), 1, 'legendary', 0.00025 / 3),
            (get_item('ender_helmet'), 1, 'legendary', 0.00025 / 3),
        ]),
    Mob('enderman', level=50, health=9000, damage=700,
        coins=15, exp=10, combat_exp=40.8,
        drops=[
            (Item('ender_pearl'), (1, 2), 'common', 1),
            (Item('enchanted_ender_pearl'), 1, 'rare', 0.01),
            (get_item('enderman_pet', rarity='rare'),
             1, 'legendary', 0.001),
            (get_item('enderman_pet', rarity='epic'),
             1, 'pray_rngesus', 0.0001),
            (get_item('enderman_pet', rarity='legendary'),
             1, 'pray_rngesus', 0.000006),
            (get_item('ender_helmet'), 1, 'legendary', 0.00005),
            (get_item('ender_chestplate'), 1, 'legendary', 0.00005),
            (get_item('ender_leggings'), 1, 'legendary', 0.00005),
            (get_item('ender_helmet'), 1, 'legendary', 0.00005),
        ]),
    Mob('obsidian_defender', level=55, health=10000, damage=200,
        coins=15, exp=10, combat_exp=40,
        drops=[
            (Item('obsidian'), (2, 3), 'common', 1),
            (Item('enchanted_obsidian'), 1, 'rare', 0.01),
            (get_item('obsidian_chestplate'), 1, 'legendary', 0.001),
        ]),
    Mob('watcher', level=55, health=9500, damage=475,
        coins=15, exp=10, combat_exp=40,
        drops=[
            (Item('arrow'), (1, 4), 'common', 1),
            (Item('ender_pearl'), (1, 2), 'common', 1),
            (Item('enchanted_bone'), 1, 'rare', 0.01),
            (get_item('end_stone_bow'), 1, 'legendary', 0.001),
        ]),
    Mob('zealot', level=55, health=13000, damage=1250,
        coins=15, exp=10, combat_exp=40,
        drops=[
            (Item('ender_pearl'), (2, 4), 'common', 1),
            (Item('enchanted_ender_pearl'), 1, 'rare', 0.02),
            (Item('summoning_eye'), 1, 'legendary', 1 / 420),
        ]),
    Mob('endermite', level=37, health=2000, damage=400,
        coins=10, exp=8, combat_exp=25,
        drops=[
            (Item('end_stone'), (1, 2), 'common', 1),
        ]),
    Mob('endermite', level=40, health=2300, damage=475,
        coins=11, exp=8, combat_exp=28,
        drops=[
            (Item('end_stone'), (2, 4), 'common', 1),
        ]),

    Mob('voidling_fanatic', level=85, health=750000, damage=3500,
        coins=20, exp=30, combat_exp=110,
        drops=[
            (Item('ender_pearl'), (4, 5), 'common', 1),
            (Item('enchanted_ender_pearl'), 1, 'rare', 0.01),
        ]),
    Mob('voidling_extremist', level=100, health=8000000, damage=13500,
        coins=100, exp=70, combat_exp=500,
        drops=[
            (Item('ender_pearl'), (32, 64), 'common', 1),
            (Item('enchanted_ender_pearl'), 1, 'rare', 0.02),
        ]),

    Mob('sneaky_creeper', level=3, health=120, damage=80,
        coins=3, exp=3, combat_exp=8,
        drops=[
            (Item('gunpowder'), 1, 'common', 1),
            (Item('exp_share_core'), 1, 'pray_rngesus', 0.0001),
        ]),
    Mob('lapis_zombie', level=7, health=200, damage=50,
        coins=5, exp=10, combat_exp=12,
        drops=[
            (Item('rotten_flesh'), (1, 2), 'common', 1),
            (get_item('lapis_helmet'), 1, 'rare', 0.0025),
            (get_item('lapis_chestplate'), 1, 'rare', 0.0025),
            (get_item('lapis_leggings'), 1, 'rare', 0.0025),
            (get_item('lapis_boots'), 1, 'rare', 0.0025),
            (Item('lapis_crystal'), 1, 'rare', 0.0025),
            (Item('exp_share_core'), 1, 'pray_rngesus', 0.0001),
        ]),
    Mob('redstone_pigman', level=12, health=240, damage=125,
        coins=4, exp=25, combat_exp=20,
        drops=[
            (Item('gold_nugget'), 2, 'common', 1),
            (Item('exp_share_core'), 1, 'pray_rngesus', 0.0001),
        ]),
    Mob('small_emerald_slime', level=5, health=80, damage=70,
        coins=5, exp=20, combat_exp=12,
        drops=[
            (Item('slime_ball'), 1, 'common', 1),
            (Item('exp_share_core'), 1, 'pray_rngesus', 0.0001),
        ]),
    Mob('medium_emerald_slime', level=10, health=150, damage=100,
        coins=8, exp=30, combat_exp=15,
        drops=[
            (Item('slime_ball'), (1, 2), 'common', 1),
            (Item('exp_share_core'), 1, 'pray_rngesus', 0.0001),
        ]),
    Mob('large_emerald_slime', level=15, health=250, damage=150,
        coins=12, exp=50, combat_exp=20,
        drops=[
            (Item('slime_ball'), 2, 'common', 1),
            (Item('exp_share_core'), 1, 'pray_rngesus', 0.0001),
        ]),
    Mob('diamond_zombie', level=15, health=250, damage=150,
        coins=12, exp=30, combat_exp=20,
        drops=[
            (Item('rotten_flesh'), 4, 'common', 1),
            (get_item('miner_helmet'), 1, 'pray_rngesus', 0.00125),
            (get_item('miner_chestplate'), 1, 'pray_rngesus', 0.00125),
            (get_item('miner_leggings'), 1, 'pray_rngesus', 0.00125),
            (get_item('miner_boots'), 1, 'pray_rngesus', 0.00125),
            (Item('exp_share_core'), 1, 'pray_rngesus', 0.0001),
        ]),
    Mob('diamond_skeleton', level=15, health=250, damage=150,
        coins=12, exp=30, combat_exp=20,
        drops=[
            (Item('bone'), 4, 'common', 1),
            (get_item('miner_helmet'), 1, 'pray_rngesus', 0.00125),
            (get_item('miner_chestplate'), 1, 'pray_rngesus', 0.00125),
            (get_item('miner_leggings'), 1, 'pray_rngesus', 0.00125),
            (get_item('miner_boots'), 1, 'pray_rngesus', 0.00125),
            (Item('exp_share_core'), 1, 'pray_rngesus', 0.0001),
        ]),
    Mob('diamond_zombie', level=20, health=300, damage=190,
        coins=15, exp=40, combat_exp=24,
        drops=[
            (Item('rotten_flesh'), 4, 'common', 1),
            (get_item('miner_helmet', enchantments={'protection': 5}),
             1, 'pray_rngesus', 0.00125),
            (get_item('miner_chestplate', enchantments={'protection': 5}),
             1, 'pray_rngesus', 0.00125),
            (get_item('miner_leggings', enchantments={'protection': 5}),
             1, 'pray_rngesus', 0.00125),
            (get_item('miner_boots', enchantments={'protection': 5}),
             1, 'pray_rngesus', 0.00125),
            (Item('exp_share_core'), 1, 'pray_rngesus', 0.0001),
        ]),
    Mob('diamond_skeleton', level=20, health=300, damage=190,
        coins=15, exp=40, combat_exp=24,
        drops=[
            (Item('bone'), 4, 'common', 1),
            (get_item('miner_helmet', enchantments={'protection': 5}),
             1, 'pray_rngesus', 0.00125),
            (get_item('miner_chestplate', enchantments={'protection': 5}),
             1, 'pray_rngesus', 0.00125),
            (get_item('miner_leggings', enchantments={'protection': 5}),
             1, 'pray_rngesus', 0.00125),
            (get_item('miner_boots', enchantments={'protection': 5}),
             1, 'pray_rngesus', 0.00125),
            (Item('exp_share_core'), 1, 'pray_rngesus', 0.0001),
        ]),

    Mob('ghost', level=250, health=1000000, damage=1000, true_damage=100,
        coins=100, exp=30, combat_exp=100,
        drops=[
            (Item('sorrow'), 1, 'rare', 0.0012),
            (Item('plasma'), 1, 'legendary', 0.001),
            (Item('bag_of_cash'), 1, 'pray_rngesus', 0.0001),
        ]),
    Mob('goblin', level=25, health=800, damage=300,
        coins=10, exp=20, combat_exp=50,
        drops=[
            (get_item('goblin_helmet'),
             1, 'pray_rngesus', 0.00075),
            (get_item('goblin_chestplate'),
             1, 'pray_rngesus', 0.00075),
            (get_item('goblin_leggings'),
             1, 'pray_rngesus', 0.00075),
            (get_item('goblin_boots'),
             1, 'pray_rngesus', 0.00075),
        ]),
    Mob('treasure_hoarder', level=70, health=22000, damage=750,
        coins=50, exp=60, combat_exp=70,
        drops=[
            (Item('starfall'), (1, 2), 'common', 1),
            (get_item('salmon_opal'), 1, 'rare', 0.01),
            (Item('treasurite'), 1, 'rare', 0.005),
        ]),
    Mob('ice_walker', level=45, health=888, defense=800, damage=500,
        coins=40, exp=35, combat_exp=40,
        drops=[
            (get_item('glacite_helmet'),
             1, 'pray_rngesus', 0.0025),
            (get_item('glacite_chestplate'),
             1, 'pray_rngesus', 0.0025),
            (get_item('glacite_leggings'),
             1, 'pray_rngesus', 0.0025),
            (get_item('glacite_boots'),
             1, 'pray_rngesus', 0.0025),
        ]),

    Mob('pack_spirit', level=35, health=7000, damage=450,
        coins=11, exp=10, combat_exp=15,
        drops=[
            (Item('spruce'), 1, 'uncommon', 0.15),
            (Item('dark'), 1, 'uncommon', 0.15),
            (Item('acacia'), 1, 'uncommon', 0.15),
            (get_item('travel_scroll_to_howl'), 1, 'legendary', 0.0002),
            (get_item('hound_pet', rarity='epic'),
             1, 'pray_rngesus', 0.0002 / 3),
            (get_item('hound_pet', rarity='legendary'),
             1, 'pray_rngesus', 0.0001 / 6),
        ]),
    Mob('howling_spirit', level=35, health=7000, damage=450,
        coins=11, exp=10, combat_exp=15,
        drops=[
            (Item('spruce'), 1, 'uncommon', 0.15),
            (Item('dark'), 1, 'uncommon', 0.15),
            (Item('acacia'), 1, 'uncommon', 0.15),
            (get_item('travel_scroll_to_howl'), 1, 'legendary', 0.0002),
            (get_item('hound_pet', rarity='epic'),
             1, 'pray_rngesus', 0.0002 / 3),
            (get_item('hound_pet', rarity='legendary'),
             1, 'pray_rngesus', 0.0001 / 6),
        ]),
    Mob('soul_of_the_alpha', level=55, health=31150, damage=1150,
        coins=50, exp=15, combat_exp=50,
        drops=[
            (Item('jungle'), 1, 'common', 1),
            (get_item('travel_scroll_to_howl'), 1, 'legendary', 0.00035),
            (get_item('hound_pet', rarity='epic'),
             1, 'pray_rngesus', 0.0002 / 3),
            (get_item('hound_pet', rarity='legendary'),
             1, 'pray_rngesus', 0.0001 / 6),
        ]),

    # sea creatures
    Mob('squid', level=1, health=2000,
        coins=0, exp=15, fishing_exp=41,
        drops=[
            (Item('lily_pad'), (1, 2), 'common', 1),
            (Item('ink_sack'), (2, 5), 'common', 1),
        ]),
    Mob('sea_walker', level=4, health=1500, damage=60,
        coins=0, exp=30, fishing_exp=68,
        drops=[
            (Item('rotten_flesh'), (1, 4), 'common', 1),
            (Item('lily_pad'), (1, 6), 'common', 1),
            (Item('fish'), (1, 4), 'common', 1),
        ]),
    Mob('night_squid', level=6, health=4000,
        coins=0, exp=28, fishing_exp=270,
        drops=[
            (Item('ink_sack'), (12, 27), 'common', 1),
            (Item('lily_pad'), (1, 4), 'common', 1),
            (get_item('squid_boots'), 1, 'rare', 0.05),
        ]),
    Mob('sea_guardian', level=10, health=5000, damage=150,
        coins=0, exp=32, fishing_exp=75,
        drops=[
            (Item('lily_pad'), (1, 2), 'common', 1),
            (Item('prismarine_shard'), (1, 3), 'common', 1),
            (Item('prismarine_crystals'), (1, 3), 'common', 1),
        ]),
    Mob('sea_witch', level=15, health=6000, damage=160,
        coins=0, exp=35, fishing_exp=338,
        drops=[
            (Item('fish'), (1, 5), 'common', 1),
            (Item('salmon'), (2, 4), 'common', 1),
            (Item('clownfish'), 1, 'common', 0.5),
            (Item('lily_pad'), (2, 3), 'common', 1),
            (get_item('fairys_fedora'), 1, 'rare', 0.01),
            (get_item('fairys_polo'), 1, 'rare', 0.01),
            (get_item('fairys_trousers'), 1, 'rare', 0.01),
            (get_item('fairys_galoshes'), 1, 'rare', 0.01),
        ]),
    Mob('sea_archer', level=15, health=7000, damage=130,
        coins=0, exp=41, fishing_exp=169,
        drops=[
            (Item('bone'), (1, 6), 'common', 1 / 7),
            (Item('enchanted_bone'), 1, 'common', 6 / 7),
            (Item('fish'), (2, 3), 'common', 1),
            (Item('lily_pad'), (2, 4), 'common', 1),
        ]),
    Mob('monster_of_the_deep', level=20, health=20000, damage=200,
        coins=0, exp=41, fishing_exp=270,
        drops=[
            (Item('lily_pad'), (2, 4), 'common', 1),
            (Item('sponge'), 1, 'common', 1),
            (Item('rotten_flesh'), (1, 6), 'common', 1 / 7),
            (Item('enchanted_rotten_flesh'), 1, 'common', 6 / 7),
            (Item('enchanted_feather'), 1, 'common', 6 / 7),
            (EnchantedBook(enchantments={'magnet': 6}), 1, 'rare', 0.02),
        ]),
    Mob('catfish', level=23, health=26000, damage=220,
        coins=0, exp=50, fishing_exp=405,
        drops=[
            (Item('clownfish'), (1, 2), 'common', 1),
            (Item('lily_pad'), (2, 5), 'common', 1),
            (Item('pufferfish'), 1, 'common', 1),
            (Item('fish'), (1, 3), 'common', 1),
            (Item('salmon'), (1, 3), 'common', 1),
            (Item('sponge'), 1, 'common', 1),
            (EnchantedBook(enchantments={'frail': 6}), 1, 'rare', 0.02),
        ]),
    Mob('sea_leech', level=30, health=60000, damage=300,
        coins=0, exp=65, fishing_exp=675,
        drops=[
            (Item('fish'), (10, 20), 'common', 1),
            (Item('clownfish'), 2, 'common', 1),
            (Item('lily_pad'), 3, 'common', 1),
            (Item('sponge'), 1, 'common', 1),
            (EnchantedBook(enchantments={'spiked_hook': 6}), 1, 'rare', 0.02),
        ]),
    Mob('guardian_defender', level=45, health=70000, damage=212,
        coins=0, exp=72, fishing_exp=1150,
        drops=[
            (Item('fish'), (15, 30), 'common', 1),
            (Item('enchanted_prismarine_shard'), 1, 'common', 1),
            (Item('enchanted_prismarine_crystals'), 1, 'common', 3 / 4),
            (Item('sponge'), (1, 2), 'common', 1),
            (Item('lily_pad'), (5, 11), 'common', 1),
            (EnchantedBook(enchantments={'lure': 6}), 1, 'rare', 0.02),
        ]),
    Mob('deep_sea_protector', level=60, health=150000, damage=400,
        coins=0, exp=100, fishing_exp=1350,
        drops=[
            (Item('clownfish'), (10, 25), 'common', 1),
            (Item('lily_pad'), (30, 40), 'common', 1),
            (Item('enchanted_iron'), (2, 4), 'common', 1),
            (Item('sponge'), (1, 3), 'common', 1),
            (EnchantedBook(enchantments={'angler': 4}), 1, 'rare', 0.02),
        ]),
    Mob('water_hydra', level=100, health=500000, damage=500,
        coins=0, exp=175, fishing_exp=3000,
        drops=[
            (get_item('water_hydra_head'), (1, 2), 'rare', 0.05),
            (EnchantedBook(enchantments={'luck_of_the_sea': 6}),
             1, 'rare', 0.02),
        ]),
    Mob('sea_emperor', level=150, health=750000, damage=600,
        coins=0, exp=250, fishing_exp=3375,
        drops=[
            (Item('enchanted_lily_pad'), (1, 3), 'common', 1),
            (Item('emperors_skull'), 1, 'common', 1),
            (get_item('shredder'), 1, 'rare', 0.2),
            (get_item('flying_fish_pet', rarity='rare'), 1, 'rare', 0.1),
            (get_item('flying_fish_pet', rarity='epic'), 1, 'rare', 0.04),
            (get_item('flying_fish_pet', rarity='legendary'), 1, 'rare', 0.01),
        ]),
]


def get_mob(name: str, warn=True, **kwargs) -> Optional[ItemType]:
    if not includes(MOBS, name):
        red(f'Mob not found: {name!r}')
        return
    return get(MOBS, name, **kwargs)
