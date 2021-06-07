from typing import Any

from ..function.io import red
from ..function.util import get, includes

from .item import get_item
from .object import ItemType, Mob

__all__ = ['MOBS', 'get_mob']


MOBS = [
    Mob('zombie', level=1, health=100, damage=20,
        coins=1, combat_xp=6, exp=1,
        drops=[
            (get_item('rotten_flesh'), 1, 'common', 1),
            (get_item('poisonous_potato'), 1, 'uncommon', 0.02),
            (get_item('potato'), 1, 'rare', 0.01),
            (get_item('carrot'), 1, 'rare', 0.01),
        ]),

    Mob('sneaky_creeper', level=3, health=120, damage=80,
        coins=3, combat_xp=8, exp=3,
        drops=[
            (get_item('gunpowder'), 1, 'common', 1),
            (get_item('exp_share_core'), 1, 'pray_rngesus', 0.0001),
        ]),
    Mob('lapis_zombie', level=7, health=200, damage=50,
        coins=5, combat_xp=12, exp=10,
        drops=[
            (get_item('rotten_flesh'), (1, 2), 'common', 1),
            (get_item('lapis_helmet'), 1, 'rare', 0.0025),
            (get_item('lapis_chestplate'), 1, 'rare', 0.0025),
            (get_item('lapis_leggings'), 1, 'rare', 0.0025),
            (get_item('lapis_boots'), 1, 'rare', 0.0025),
            (get_item('lapis_crystal'), 1, 'rare', 0.0025),
            (get_item('exp_share_core'), 1, 'pray_rngesus', 0.0001),
        ]),
    Mob('redstone_pigman', level=12, health=240, damage=125,
        coins=4, combat_xp=15, exp=25,
        drops=[
            (get_item('gold_nugget'), 2, 'common', 1),
            (get_item('flaming_sword'), 1, 'uncommon', 0.03),
            (get_item('exp_share_core'), 1, 'pray_rngesus', 0.0001),
        ]),
    Mob('small_emerald_slime', level=5, health=80, damage=70,
        coins=5, combat_xp=12, exp=20,
        drops=[
            (get_item('slime_ball'), 1, 'common', 1),
            (get_item('exp_share_core'), 1, 'pray_rngesus', 0.0001),
        ]),
    Mob('medium_emerald_slime', level=10, health=150, damage=100,
        coins=8, combat_xp=15, exp=30,
        drops=[
            (get_item('slime_ball'), (1, 2), 'common', 1),
            (get_item('exp_share_core'), 1, 'pray_rngesus', 0.0001),
        ]),
    Mob('large_emerald_slime', level=15, health=250, damage=150,
        coins=12, combat_xp=20, exp=50,
        drops=[
            (get_item('slime_ball'), 2, 'common', 1),
            (get_item('exp_share_core'), 1, 'pray_rngesus', 0.0001),
        ]),
    Mob('diamond_zombie', level=15, health=250, damage=150,
        coins=12, combat_xp=20, exp=30,
        drops=[
            (get_item('rotten_flesh'), 4, 'common', 1),
            (get_item('miner_helmet'), 1, 'pray_rngesus', 0.00125),
            (get_item('miner_chestplate'), 1, 'pray_rngesus', 0.00125),
            (get_item('miner_leggings'), 1, 'pray_rngesus', 0.00125),
            (get_item('miner_boots'), 1, 'pray_rngesus', 0.00125),
            (get_item('exp_share_core'), 1, 'pray_rngesus', 0.0001),
        ]),
    Mob('diamond_skeleton', level=15, health=250, damage=150,
        coins=12, combat_xp=20, exp=30,
        drops=[
            (get_item('bone'), 4, 'common', 1),
            (get_item('miner_helmet'), 1, 'pray_rngesus', 0.00125),
            (get_item('miner_chestplate'), 1, 'pray_rngesus', 0.00125),
            (get_item('miner_leggings'), 1, 'pray_rngesus', 0.00125),
            (get_item('miner_boots'), 1, 'pray_rngesus', 0.00125),
            (get_item('exp_share_core'), 1, 'pray_rngesus', 0.0001),
        ]),
    Mob('enchanted_diamond_zombie', level=20, health=300, damage=190,
        coins=15, combat_xp=24, exp=40,
        drops=[
            (get_item('rotten_flesh'), 4, 'common', 1),
            (get_item('miner_helmet', enchantments={'protection': 5}),
             1, 'pray_rngesus', 0.00125),
            (get_item('miner_chestplate', enchantments={'protection': 5}),
             1, 'pray_rngesus', 0.00125),
            (get_item('miner_leggings', enchantments={'protection': 5}),
             1, 'pray_rngesus', 0.00125),
            (get_item('miner_boots', enchantments={'protection': 5}),
             1, 'pray_rngesus', 0.00125),
            (get_item('exp_share_core'), 1, 'pray_rngesus', 0.0001),
        ]),
    Mob('enchanted_diamond_skeleton', level=20, health=300, damage=190,
        coins=15, combat_xp=24, exp=40,
        drops=[
            (get_item('bone'), 4, 'common', 1),
            (get_item('miner_helmet', enchantments={'protection': 5}),
             1, 'pray_rngesus', 0.00125),
            (get_item('miner_chestplate', enchantments={'protection': 5}),
             1, 'pray_rngesus', 0.00125),
            (get_item('miner_leggings', enchantments={'protection': 5}),
             1, 'pray_rngesus', 0.00125),
            (get_item('miner_boots', enchantments={'protection': 5}),
             1, 'pray_rngesus', 0.00125),
            (get_item('exp_share_core'), 1, 'pray_rngesus', 0.0001),
        ]),

    Mob('enderman', level=42, health=4_500, damage=500,
        coins=10, combat_xp=40.8, exp=8,
        drops=[
            (get_item('ender_pearl'), (1, 3), 'common', 1),
            (get_item('enchanted_ender_pearl'), 1, 'rare', 0.01),
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
    Mob('enderman', level=45, health=6_000, damage=600,
        coins=12, combat_xp=40.8, exp=9,
        drops=[
            (get_item('ender_pearl'), (1, 3), 'common', 1),
            (get_item('enchanted_ender_pearl'), 1, 'rare', 0.01),
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
    Mob('enderman', level=50, health=9_000, damage=700,
        coins=15, combat_xp=40.8, exp=10,
        drops=[
            (get_item('ender_pearl'), (1, 2), 'common', 1),
            (get_item('enchanted_ender_pearl'), 1, 'rare', 0.01),
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
    Mob('zealot', level=55, health=13_000, damage=1250,
        coins=15, combat_xp=40, exp=10,
        drops=[
            (get_item('ender_pearl'), (2, 4), 'common', 1),
            (get_item('enchanted_ender_pearl'), 1, 'rare', 0.02),
        ]),
]


def get_mob(name: str, default: Any = None, **kwargs) -> ItemType:
    if not includes(MOBS, name):
        red(f'Invalid mob: {name!r}')
        exit()
    return get(MOBS, name, default, **kwargs)
