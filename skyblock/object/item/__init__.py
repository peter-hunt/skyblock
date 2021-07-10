from ...function.io import *
from ...function.util import get, includes

from ..object import *

from .armor import ARMOR
from .pet import PETS
from .scroll import TRAVEL_SCROLLS, get_scroll
from .stone import REFORGE_STONES, get_stone
from .tool import TOOLS
from .weapon import WEAPONS


__all__ = [
    'COLLECTION_ITEMS',  'OTHER_ITEMS',
    'ARMOR', 'PETS', 'TRAVEL_SCROLLS', 'REFORGE_STONES', 'TOOLS', 'WEAPONS',
    'get_scroll', 'get_stone',
    'ITEMS', 'get_item', 'validify_item', 'get_stack_size',
]

COLLECTION_ITEMS = [
    Item('hay_bale', 64, 'common'),
    Item('enchanted_bread', 64, 'common'),
    Item('golden_carrot', 64, 'common'),
    Item('glistering_melon', 64, 'common'),
    Item('mushroom_block', 64, 'common'),
    Item('wool', 64, 'common'),

    Item('wheat', 64, 'common'),
    Item('carrot', 64, 'common'),
    Item('potato', 64, 'common'),
    Item('pumpkin', 64, 'common'),
    Item('melon', 64, 'common'),
    Item('seeds', 64, 'common'),
    Item('mushroom', 64, 'common'),
    Item('cocoa', 64, 'common'),
    Item('cactus', 64, 'common'),
    Item('sugar_cane', 64, 'common'),
    Item('feather', 64, 'common'),
    Item('beef', 64, 'common'),
    Item('leather', 64, 'common'),
    Item('pork', 64, 'common'),
    Item('chicken', 64, 'common'),
    Item('mutton', 64, 'common'),
    Item('rabbit', 64, 'common'),
    Item('rabbit_foot', 64, 'common'),
    Item('rabbit_hide', 64, 'common'),
    Item('nether_wart', 64, 'common'),

    Item('enchanted_hay_bale', 64, 'uncommon'),
    Item('tightly_tied_hay_bale', 64, 'rare'),
    Item('enchanted_carrot', 64, 'uncommon'),
    Item('enchanted_golden_carrot', 64, 'uncommon'),
    Item('enchanted_potato', 64, 'uncommon'),
    Item('enchanted_baked_potato', 64, 'rare'),
    Item('enchanted_pumpkin', 64, 'uncommon'),
    Item('polished_pumpkin', 64, 'rare'),
    Item('enchanted_melon', 64, 'uncommon'),
    Item('enchanted_glistering_melon', 64, 'rare'),
    Item('enchanted_melon_block', 64, 'rare'),
    Item('enchanted_mushroom', 64, 'common'),
    Item('enchanted_mushroom_block', 64, 'common'),
    Item('enchanted_cocoa', 64, 'uncommon'),
    Item('enchanted_cookie', 64, 'rare'),
    Item('enchanted_sugar', 64, 'uncommon'),
    Item('enchanted_paper', 64, 'uncommon'),
    Item('enchanted_bookshelf', 64, 'uncommon'),
    Item('enchanted_sugar_cane', 64, 'rare'),
    Item('enchanted_feather', 64, 'uncommon'),
    Item('enchanted_beef', 64, 'uncommon'),
    Item('enchanted_leather', 64, 'uncommon'),
    Item('enchanted_pork', 64, 'uncommon'),
    Item('enchanted_grilled_pork', 64, 'rare'),
    Item('enchanted_chicken', 64, 'uncommon'),
    Item('enchanted_egg', 16, 'rare'),
    Item('enchanted_cake', 16, 'uncommon'),
    Item('super_enchanted_egg', 64, 'rare'),
    Item('enchanted_mutton', 64, 'uncommon'),
    Item('enchanted_cooked_mutton', 64, 'rare'),
    Item('enchanted_rabbit', 64, 'uncommon'),
    Item('enchanted_rabbit_foot', 64, 'uncommon'),
    Item('enchanted_rabbit_hide', 64, 'uncommon'),
    Item('enchanted_nether_wart', 64, 'uncommon'),
    Item('mutant_nether_wart', 64, 'rare'),

    Item('cobblestone', 64, 'common'),
    Item('coal', 64, 'common'),
    Item('iron', 64, 'common'),
    Item('gold', 64, 'common'),
    Item('diamond', 64, 'common'),
    Item('lapis', 64, 'common'),
    Item('emerald', 64, 'common'),
    Item('redstone', 64, 'common'),
    Item('quartz', 64, 'common'),
    Item('obsidian', 64, 'common'),
    Item('glowstone', 64, 'common'),
    Item('gravel', 64, 'common'),
    Item('ice', 64, 'common'),
    Item('netherrack', 64, 'common'),
    Item('sand', 64, 'common'),
    Item('end_stone', 64, 'common'),
    Item('mithril', 64, 'common'),
    Item('starfall', 64, 'rare'),
    Item('titanium', 64, 'rare'),
    Item('sorrow', 64, 'rare'),
    Item('plasma', 64, 'rare'),

    Item('coal_block', 64, 'common'),
    Item('iron_block', 64, 'common'),
    Item('gold_block', 64, 'common'),
    Item('diamond_block', 64, 'common'),
    Item('lapis_block', 64, 'common'),
    Item('emerald_block', 64, 'common'),
    Item('redstone_block', 64, 'common'),
    Item('packed_ice', 64, 'common'),

    Item('enchanted_cobblestone', 64, 'uncommon'),
    Item('enchanted_coal', 64, 'uncommon'),
    Item('enchanted_iron', 64, 'uncommon'),
    Item('enchanted_gold', 64, 'uncommon'),
    Item('enchanted_diamond', 64, 'uncommon'),
    Item('enchanted_lapis', 64, 'uncommon'),
    Item('enchanted_emerald', 64, 'uncommon'),
    Item('enchanted_redstone', 64, 'uncommon'),
    Item('enchanted_quartz', 64, 'uncommon'),
    Item('enchanted_obsidian', 64, 'uncommon'),
    Item('enchanted_glowstone', 64, 'uncommon'),
    Item('enchanted_flint', 64, 'uncommon'),
    Item('enchanted_ice', 64, 'uncommon'),
    Item('enchanted_netherrack', 64, 'uncommon'),
    Item('enchanted_sand', 64, 'uncommon'),
    Item('enchanted_end_stone', 64, 'uncommon'),
    Item('enchanted_mithril', 64, 'uncommon'),
    Item('enchanted_titanium', 64, 'epic'),

    Item('enchanted_coal_block', 64, 'rare'),
    Item('enchanted_iron_block', 64, 'rare'),
    Item('enchanted_gold_block', 64, 'rare'),
    Item('enchanted_diamond_block', 64, 'rare'),
    Item('enchanted_lapis_block', 64, 'rare'),
    Item('enchanted_emerald_block', 64, 'rare'),
    Item('enchanted_redstone_block', 64, 'rare'),
    Item('enchanted_quartz_block', 64, 'rare'),
    Item('enchanted_glowstone_block', 64, 'uncommon'),
    Item('enchanted_redstone_lamp', 64, 'rare'),
    Item('enchanted_packed_ice', 64, 'rare'),

    Item('refined_diamond', 64, 'epic'),
    Item('refined_mithril', 64, 'epic'),
    Item('refined_titanium', 64, 'legendary'),
    Item('fuel_tank', 1, 'rare'),
    Item('mithril_plate', 1, 'rare'),
    Item('bejeweled_handle', 64, 'rare'),
    Item('golden_plate', 1, 'rare'),
    Item('drill_engine', 1, 'rare'),

    Item('rotten_flesh', 64, 'common'),
    Item('bone', 64, 'common'),
    Item('string', 64, 'common'),
    Item('spider_eye', 64, 'common'),
    Item('gunpowder', 64, 'common'),
    Item('ender_pearl', 16, 'common'),
    Item('ghast_tear', 64, 'common'),
    Item('slime_ball', 64, 'common'),
    Item('blaze_rod', 64, 'common'),
    Item('magma_cream', 64, 'common'),

    Item('slime_block', 64, 'common'),

    Item('enchanted_rotten_flesh', 64, 'uncommon'),
    Item('enchanted_bone', 64, 'uncommon'),
    Item('enchanted_string', 64, 'uncommon'),
    Item('enchanted_spider_eye', 64, 'uncommon'),
    Item('enchanted_gunpowder', 64, 'uncommon'),
    Item('enchanted_ender_pearl', 16, 'uncommon'),
    Item('enchanted_eye_of_ender', 64, 'uncommon'),
    Item('enchanted_ghast_tear', 64, 'uncommon'),
    Item('enchanted_slime_ball', 64, 'uncommon'),
    Item('enchanted_blaze_powder', 64, 'uncommon'),
    Item('enchanted_magma_cream', 64, 'uncommon'),

    Item('enchanted_bone_block', 64, 'rare'),
    Item('enchanted_fermented_spider_eye', 64, 'rare'),
    Item('enchanted_firework_rocket', 64, 'rare'),
    Item('enchanted_eye_of_ender', 64, 'rare'),
    Item('absolute_ender_pearl', 64, 'rare'),
    Item('tesselated_ender_pearl', 64, 'legendary'),
    Item('enchanted_slime_block', 64, 'rare'),
    Item('enchanted_blaze_rod', 64, 'uncommon'),

    Item('oak_wood', 64, 'common'),
    Item('birch_wood', 64, 'common'),
    Item('spruce_wood', 64, 'common'),
    Item('dark_oak_wood', 64, 'common'),
    Item('acacia_wood', 64, 'common'),
    Item('jungle_wood', 64, 'common'),

    Item('enchanted_oak', 64, 'uncommon'),
    Item('enchanted_birch', 64, 'uncommon'),
    Item('enchanted_spruce', 64, 'uncommon'),
    Item('enchanted_dark_oak', 64, 'uncommon'),
    Item('enchanted_acacia', 64, 'uncommon'),
    Item('enchanted_jungle', 64, 'uncommon'),

    Item('oak_sapling', 64, 'common'),
    Item('birch_sapling', 64, 'common'),
    Item('spruce_sapling', 64, 'common'),
    Item('dark_oak_sapling', 64, 'common'),
    Item('acacia_sapling', 64, 'common'),
    Item('jungle_sapling', 64, 'common'),

    Item('oak_leaves', 64, 'common'),
    Item('birch_leaves', 64, 'common'),
    Item('spruce_leaves', 64, 'common'),
    Item('dark_oak_leaves', 64, 'common'),
    Item('acacia_leaves', 64, 'common'),
    Item('jungle_leaves', 64, 'common'),

    Item('dandelion', 64, 'common'),
    Item('poppy', 64, 'common'),

    Item('enchanted_dandelion', 64, 'uncommon'),
    Item('enchanted_poppy', 64, 'uncommon'),

    Item('fish', 64, 'common'),
    Item('salmon', 64, 'common'),
    Item('clownfish', 64, 'common'),
    Item('pufferfish', 64, 'common'),
    Item('prismarine_shard', 64, 'common'),
    Item('prismarine_crystals', 64, 'common'),
    Item('clay', 64, 'common'),
    Item('lily_pad', 64, 'common'),
    Item('ink_sack', 64, 'common'),
    Item('sponge', 64, 'common'),

    Item('enchanted_fish', 64, 'uncommon'),
    Item('enchanted_salmon', 64, 'uncommon'),
    Item('enchanted_pufferfish', 64, 'uncommon'),
    Item('enchanted_prismarine_shard', 64, 'uncommon'),
    Item('enchanted_prismarine_crystals', 64, 'uncommon'),
    Item('enchanted_clay', 64, 'uncommon'),
    Item('enchanted_lily_pad', 64, 'uncommon'),
    Item('enchanted_ink_sack', 64, 'uncommon'),
    Item('enchanted_sponge', 64, 'uncommon'),

    Item('enchanted_cooked_fish', 64, 'rare'),
    Item('enchanted_cooked_salmon', 64, 'rare'),
    Item('enchanted_wet_sponge', 64, 'rare'),
]

OTHER_ITEMS = [
    Item('arrow', 64, 'common'),
    Item('blaze_powder', 64, 'common'),
    Item('enchanted_golden_apple', 64, 'uncommon'),
    Item('exp_share_core', 1, 'epic'),
    Item('flint', 64, 'common'),
    Item('glowstone_block', 64, 'common'),
    Item('gold_nugget', 64, 'common'),
    Item('golden_powder', 64, 'epic'),
    Item('iron_nugget', 64, 'common'),
    Item('lapis_crystal', 1, 'rare'),
    Item('planks', 64, 'common'),
    Item('poisonous_potato', 64, 'common'),
    Item('saving_grace', 64, 'rare'),
    Item('stick', 64, 'common'),

    Item('apple', 64, 'common'),
    Item('book', 64, 'common'),
    Item('bread', 64, 'common'),
    Item('egg', 16, 'common'),
    Item('golden_apple', 64, 'common'),
    Item('paper', 64, 'common'),
    Item('sugar', 64, 'common'),

    Item('hot_potato_book', 1, 'epic'),
    Item('fuming_potato_book', 1, 'epic'),

    Item('glass', 64, 'common'),
    Item('bottle', 64, 'common'),
    Item('experience_bottle', 64, 'common',
         abilities=['exp_bottle']),
    Item('grand_experience_bottle', 64, 'uncommon',
         abilities=['exp_bottle']),
    Item('titanic_experience_bottle', 64, 'rare',
         abilities=['exp_bottle']),

    Item('glacite_jewel', 64, 'rare'),
    Item('treasurite', 64, 'epic'),

    Item('summoning_eye', 1, 'epic'),
    Item('bag_of_cash', 1, 'rare'),

    Item('minnow_bait', 64, 'common'),
    Item('fish_bait', 64, 'common'),
    Item('light_bait', 64, 'common'),
    Item('dark_bait', 64, 'common'),
    Item('spiked_bait', 64, 'common'),
    Item('spooky_bait', 64, 'common'),
    Item('carrot_bait', 64, 'common'),
    Item('blessed_bait', 64, 'uncommon'),
    Item('whale_bait', 64, 'rare'),
    Item('ice_bait', 64, 'uncommon'),
    Item('shark_bait', 64, 'uncommon'),

    Item('shark_fin', 64, 'rare'),
    Item('emperors_skull', 64, 'rare'),

    EnchantedBook(),
]

ITEMS = (COLLECTION_ITEMS + OTHER_ITEMS + WEAPONS
         + ARMOR + TOOLS + TRAVEL_SCROLLS + REFORGE_STONES + PETS)


def get_item(name: str, **kwargs) -> ItemType:
    if not includes(ITEMS, name):
        red(f'Item not found: {name!r}')
        exit()
    return get(ITEMS, name, **kwargs)


def get_stack_size(name: str, /) -> int:
    return getattr(get_item(name), 'count', 1)


def validify_item(item: ItemType, /) -> ItemType:
    attrs = {}
    kwargs = {}
    if getattr(item, 'enchantments', {}) != {}:
        attrs['enchantments'] = item.enchantments.copy()
    if getattr(item, 'hot_potato', 0) != 0:
        attrs['hot_potato'] = item.hot_potato
    if getattr(item, 'modifier', None) is not None:
        attrs['modifier'] = item.modifier
    if getattr(item, 'stars', 0) != 0:
        attrs['stars'] = item.stars

    if getattr(item, 'rarity', None) != None:
        if isinstance(item, (Sword, Bow, Armor, Pet)):
            kwargs['rarity'] = item.rarity
        else:
            attrs['rarity'] = item.rarity

    item_copy = get_item(item.name, **kwargs)
    for key, value in attrs.items():
        setattr(item_copy, key, value)

    return item_copy
