from ..item import get_item, get_scroll
from ..object import Item, Recipe


__all__ = ['COMBAT_RECIPES']

COMBAT_RECIPES = [
    Recipe('leather_helmet', 'combat',
           [(Item('leather'), 5)],
           (get_item('leather_helmet'), 1)),
    Recipe('leather_chestplate', 'combat',
           [(Item('leather'), 8)],
           (get_item('leather_chestplate'), 1)),
    Recipe('leather_leggings', 'combat',
           [(Item('leather'), 7)],
           (get_item('leather_leggings'), 1)),
    Recipe('leather_boots', 'combat',
           [(Item('leather'), 4)],
           (get_item('leather_boots'), 1)),

    Recipe('golden_helmet', 'combat',
           [(Item('gold'), 5)],
           (get_item('golden_helmet'), 1)),
    Recipe('golden_chestplate', 'combat',
           [(Item('gold'), 8)],
           (get_item('golden_chestplate'), 1)),
    Recipe('golden_leggings', 'combat',
           [(Item('gold'), 7)],
           (get_item('golden_leggings'), 1)),
    Recipe('golden_boots', 'combat',
           [(Item('gold'), 4)],
           (get_item('golden_boots'), 1)),

    Recipe('iron_helmet', 'combat',
           [(Item('iron'), 5)],
           (get_item('iron_helmet'), 1)),
    Recipe('iron_chestplate', 'combat',
           [(Item('iron'), 8)],
           (get_item('iron_chestplate'), 1)),
    Recipe('iron_leggings', 'combat',
           [(Item('iron'), 7)],
           (get_item('iron_leggings'), 1)),
    Recipe('iron_boots', 'combat',
           [(Item('iron'), 4)],
           (get_item('iron_boots'), 1)),

    Recipe('diamond_helmet', 'combat',
           [(Item('diamond'), 5)],
           (get_item('diamond_helmet'), 1)),
    Recipe('diamond_chestplate', 'combat',
           [(Item('diamond'), 8)],
           (get_item('diamond_chestplate'), 1)),
    Recipe('diamond_leggings', 'combat',
           [(Item('diamond'), 7)],
           (get_item('diamond_leggings'), 1)),
    Recipe('diamond_boots', 'combat',
           [(Item('diamond'), 4)],
           (get_item('diamond_boots'), 1)),

    Recipe('arrow', 'combat',
           [(Item('flint'), 1),
            (Item('stick'), 1),
            (Item('feather'), 1)],
           (Item('arrow'), 4)),

    Recipe('wooden_sword', 'combat',
           [(Item('planks'), 2),
            (Item('stick'), 1)],
           (get_item('wooden_sword'), 1)),
    Recipe('gold_sword', 'combat',
           [(Item('gold'), 2),
            (Item('stick'), 1)],
           (get_item('golden_sword'), 1)),
    Recipe('stone_sword', 'combat',
           [(Item('cobblestone'), 2),
            (Item('stick'), 1)],
           (get_item('stone_sword'), 1)),
    Recipe('iron_sword', 'combat',
           [(Item('iron'), 2),
            (Item('stick'), 1)],
           (get_item('iron_sword'), 1)),
    Recipe('diamond_sword', 'combat',
           [(Item('diamond'), 2),
            (Item('stick'), 1)],
           (get_item('diamond_sword'), 1)),
    Recipe('bow', 'combat',
           [(Item('stick'), 3),
            (Item('string'), 3)],
           (get_item('bow'), 1)),

    Recipe('slime_ball_to_block', 'combat',
           [(Item('slime_ball'), 9)],
           (Item('slime_block'), 1)),
    Recipe('slime_block_to_ball', 'combat',
           [(Item('slime_block'), 1)],
           (Item('slime_ball'), 9)),
    Recipe('blaze_rod_to_powder', 'combat',
           [(Item('blaze_rod'), 1)],
           (Item('blaze_powder'), 2)),

    Recipe('zombie_pickaxe', 'combat',
           [(Item('rotten_flesh'), 3),
            (Item('stick', 2))],
           (get_item('zombie_pickaxe'), 1),
           collection_req=('rotten_flesh', 2)),
    Recipe('rotten_flesh_to_enchanted', 'combat',
           [(Item('rotten_flesh'), 160)],
           (Item('enchanted_rotten_flesh'), 1),
           collection_req=('rotten_flesh', 4)),
    Recipe('zombie_hat', 'combat',
           [(Item('rotten_flesh'), 5)],
           (get_item('zombie_hat'), 1),
           collection_req=('rotten_flesh', 5)),
    Recipe('zombies_heart', 'combat',
           [(Item('enchanted_rotten_flesh'), 256)],
           (get_item('zombies_heart'), 1),
           collection_req=('rotten_flesh', 6)),
    Recipe('zombie_sword', 'combat',
           [(Item('zombies_heart'), 2),
            (Item('stick', 1))],
           (get_item('zombie_sword'), 1),
           collection_req=('rotten_flesh', 7)),
    Recipe('zombie_chestplate', 'combat',
           [(Item('zombies_heart'), 4),
            (Item('enchanted_rotten_flesh'), 4)],
           (get_item('zombie_chestplate'), 1),
           collection_req=('rotten_flesh', 8)),
    Recipe('zombie_leggings', 'combat',
           [(Item('zombies_heart'), 3),
            (Item('enchanted_rotten_flesh'), 4)],
           (get_item('zombie_leggings'), 1),
           collection_req=('rotten_flesh', 8)),
    Recipe('zombie_boots', 'combat',
           [(Item('zombies_heart'), 2),
            (Item('enchanted_rotten_flesh'), 2)],
           (get_item('zombie_boots'), 1),
           collection_req=('rotten_flesh', 8)),
    Recipe('uncommon_zombie_pet', 'combat',
           [(Item('zombies_heart'), 8),
            (Item('enchanted_egg'), 1)],
           (get_item('zombie_pet', rarity='uncommon'), 1),
           collection_req=('rotten_flesh', 9)),
    Recipe('epic_zombie_pet', 'combat',
           [(Item('zombies_heart'), 8),
            (Item('super_enchanted_egg'), 1)],
           (get_item('zombie_pet', rarity='epic'), 1),
           collection_req=('rotten_flesh', 9)),

    Recipe('skeleton_hat', 'combat',
           [(Item('bone'), 8)],
           (get_item('skeleton_hat'), 1),
           collection_req=('bone', 4)),
    Recipe('bone_to_enchanted', 'combat',
           [(Item('bone'), 160)],
           (Item('enchanted_bone'), 1),
           collection_req=('bone', 5)),
    Recipe('uncommon_skeleton_pet', 'combat',
           [(Item('enchanted_bone'), 128),
            (Item('enchanted_egg'), 1)],
           (get_item('skeleton_pet', rarity='uncommon'), 1),
           collection_req=('bone', 6)),
    Recipe('epic_skeleton_pet', 'combat',
           [(Item('enchanted_bone'), 128),
            (Item('super_enchanted_egg'), 1)],
           (get_item('skeleton_pet', rarity='epic'), 1),
           collection_req=('bone', 6)),
    Recipe('hurricane_bow', 'combat',
           [(Item('enchanted_bone'), 96),
            (Item('string'), 96)],
           (get_item('hurricane_bow'), 1),
           collection_req=('bone', 7)),
    Recipe('skeletons_helmet', 'combat',
           [(Item('enchanted_bone'), 320)],
           (get_item('skeletons_helmet'), 1),
           collection_req=('bone', 8)),
    Recipe('runaans_bow', 'combat',
           [(Item('enchanted_bone'), 192),
            (Item('enchanted_string'), 192)],
           (get_item('runaans_bow'), 1),
           collection_req=('bone', 9)),
    Recipe('bone_to_enchanted_block', 'combat',
           [(Item('enchanted_bone'), 160)],
           (Item('enchanted_bone_block'), 1),
           collection_req=('bone', 10)),

    Recipe('string_to_enchanted', 'combat',
           [(Item('string'), 192)],
           (Item('enchanted_string'), 1),
           collection_req=('string', 4)),
    Recipe('spiders_boots', 'combat',
           [(Item('enchanted_string'), 256)],
           (get_item('spiders_boots'), 1),
           collection_req=('string', 8)),
    Recipe('uncommon_spider_pet', 'combat',
           [(Item('enchanted_string'), 512),
            (Item('enchanted_egg'), 1)],
           (get_item('spider_pet', rarity='uncommon'), 1),
           collection_req=('string', 9)),
    Recipe('epic_spider_pet', 'combat',
           [(Item('enchanted_string'), 512),
            (Item('super_enchanted_egg'), 1)],
           (get_item('spider_pet', rarity='epic'), 1),
           collection_req=('string', 9)),

    Recipe('spider_sword', 'combat',
           [(Item('spider_eye'), 2),
            (Item('stick'), 1)],
           (get_item('spider_sword'), 1),
           collection_req=('spider_eye', 2)),
    Recipe('spider_hat', 'combat',
           [(Item('spider_eye'), 8)],
           (get_item('spider_hat'), 1),
           collection_req=('spider_eye', 3)),
    Recipe('spider_eye_to_enchanted', 'combat',
           [(Item('spider_eye'), 160)],
           (Item('enchanted_spider_eye'), 1),
           collection_req=('spider_eye', 4)),
    Recipe('spider_eye_to_enchanted_fermented', 'combat',
           [(Item('enchanted_spider_eye'), 64),
            (Item('mushroom'), 64),
            (Item('sugar'), 64)],
           (Item('enchanted_fermented_spider_eye'), 1),
           collection_req=('spider_eye', 7)),
    Recipe('leaping_sword', 'combat',
           [(Item('enchanted_fermented_spider_eye'), 24),
            (Item('stick'), 1)],
           (get_item('leaping_sword'), 1),
           collection_req=('spider_eye', 9)),

    Recipe('creeper_hat', 'combat',
           [(Item('gunpowder'), 8)],
           (get_item('creeper_hat'), 1),
           collection_req=('gunpowder', 2)),
    Recipe('gunpowder_to_enchanted', 'combat',
           [(Item('gunpowder'), 160)],
           (Item('enchanted_gunpowder'), 1),
           collection_req=('gunpowder', 4)),
    Recipe('gunpowder_to_enchanted_firework', 'combat',
           [(Item('enchanted_gunpowder'), 64),
            (Item('paper'), 4)],
           (Item('enchanted_firework_rocket'), 1),
           collection_req=('gunpowder', 6)),
    Recipe('creeper_pants', 'combat',
           [(Item('enchanted_gunpowder'), 224)],
           (get_item('creeper_pants'), 1),
           collection_req=('gunpowder', 8)),
    Recipe('explosive_bow', 'combat',
           [(Item('enchanted_firework_rocket'), 3),
            (Item('string'), 3)],
           (get_item('explosive_bow'), 1),
           collection_req=('gunpowder', 9)),

    Recipe('ender_pearl_to_enchanted', 'combat',
           [(Item('ender_pearl'), 20)],
           (Item('enchanted_ender_pearl'), 1),
           collection_req=('ender_pearl', 2)),
    Recipe('ender_bow', 'combat',
           [(Item('enchanted_ender_pearl'), 12),
            (Item('string'), 3)],
           (get_item('ender_bow'), 1),
           collection_req=('ender_pearl', 5)),
    Recipe('ender_pearl_to_enchanted_eye', 'combat',
           [(Item('enchanted_ender_pearl'), 16),
            (Item('blaze_powder'), 64)],
           (Item('enchanted_eye_of_ender'), 1),
           collection_req=('ender_pearl', 6)),
    Recipe('aspect_of_the_end', 'combat',
           [(Item('enchanted_eye_of_ender'), 32),
            (Item('enchanted_diamond'), 1)],
           (get_item('aspect_of_the_end'), 1),
           collection_req=('ender_pearl', 7)),
    Recipe('ender_pearl_to_absolute', 'combat',
           [(Item('enchanted_ender_pearl'), 80)],
           (Item('absolute_ender_pearl'), 1),
           collection_req=('ender_pearl', 7)),
    Recipe('ender_pearl_to_tesselated', 'combat',
           [(Item('absolute_ender_pearl'), 80),
            (Item('enchanted_lapis_block'), 32)],
           (Item('tesselated_ender_pearl'), 1)),
    Recipe('saving_grace', 'combat',
           [(Item('enchanted_ender_pearl'), 128),
            (Item('enchanted_golden_apple'), 16)],
           (Item('saving_grace'), 1),
           collection_req=('ender_pearl', 9)),

    Recipe('ghast_head', 'combat',
           [(Item('ghast_tear'), 8)],
           (get_item('ghast_head'), 1),
           collection_req=('ghast_tear', 2)),
    Recipe('ghast_tear_to_enchanted', 'combat',
           [(Item('ghast_tear'), 5)],
           (Item('enchanted_ghast_tear'), 1),
           collection_req=('ghast_tear', 4)),
    Recipe('silver_fang', 'combat',
           [(Item('enchanted_ghast_tear'), 25)],
           (get_item('silver_fang'), 1),
           collection_req=('ghast_tear', 6)),

    Recipe('slime_hat', 'combat',
           [(Item('slime_ball'), 8)],
           (get_item('slime_hat'), 1),
           collection_req=('slime_ball', 2)),
    Recipe('slime_ball_to_enchanted', 'combat',
           [(Item('slime_ball'), 160)],
           (Item('enchanted_slime_ball'), 1),
           collection_req=('slime_ball', 5)),
    Recipe('slime_ball_to_enchanted_block', 'combat',
           [(Item('enchanted_slime_ball'), 160)],
           (Item('enchanted_slime_block'), 1),
           collection_req=('slime_ball', 8)),
    Recipe('slime_bow', 'combat',
           [(Item('enchanted_slime_block'), 15),
            (Item('enchanted_string'), 3)],
           (get_item('slime_bow'), 1),
           collection_req=('slime_ball', 9)),

    Recipe('blaze_hat', 'combat',
           [(Item('blaze_rod'), 8)],
           (get_item('blaze_hat'), 1),
           collection_req=('blaze_rod', 2)),
    Recipe('blaze_rod_to_enchanted_powder', 'combat',
           [(Item('blaze_rod'), 160)],
           (Item('enchanted_blaze_powder'), 1),
           collection_req=('blaze_rod', 4)),
    Recipe('blaze_rod_to_enchanted', 'combat',
           [(Item('enchanted_blaze_powder'), 160)],
           (Item('enchanted_blaze_rod'), 1),
           collection_req=('blaze_rod', 7)),

    Recipe('blaze_helmet', 'combat',
           [(Item('enchanted_blaze_rod'), 5)],
           (get_item('blaze_helmet'), 1),
           collection_req=('blaze_rod', 8)),
    Recipe('blaze_chestplate', 'combat',
           [(Item('enchanted_blaze_rod'), 8)],
           (get_item('blaze_chestplate'), 1),
           collection_req=('blaze_rod', 8)),
    Recipe('blaze_leggings', 'combat',
           [(Item('enchanted_blaze_rod'), 7)],
           (get_item('blaze_leggings'), 1),
           collection_req=('blaze_rod', 8)),
    Recipe('blaze_boots', 'combat',
           [(Item('enchanted_blaze_rod'), 4)],
           (get_item('blaze_boots'), 1),
           collection_req=('blaze_rod', 8)),
    Recipe('epic_blaze_pet', 'combat',
           [(Item('enchanted_blaze_rod'), 64),
            (Item('super_enchanted_egg'), 1)],
           (get_item('blaze_pet', rarity='epic'), 1),
           collection_req=('blaze_rod', 9)),

    Recipe('magma_cube_head', 'combat',
           [(Item('magma_cream'), 8)],
           (get_item('magma_cube_head'), 1),
           collection_req=('magma_cream', 2)),
    Recipe('magma_cream_to_enchanted', 'combat',
           [(Item('magma_cream'), 160)],
           (Item('enchanted_magma_cream'), 1),
           collection_req=('magma_cream', 5)),

    Recipe('armor_of_magma_helmet', 'combat',
           [(Item('enchanted_magma_cream'), 60)],
           (get_item('armor_of_magma_helmet'), 1),
           collection_req=('magma_cream', 8)),
    Recipe('armor_of_magma_chestplate', 'combat',
           [(Item('enchanted_magma_cream'), 96)],
           (get_item('armor_of_magma_chestplate'), 1),
           collection_req=('magma_cream', 8)),
    Recipe('armor_of_magma_leggings', 'combat',
           [(Item('enchanted_magma_cream'), 84)],
           (get_item('armor_of_magma_leggings'), 1),
           collection_req=('magma_cream', 8)),
    Recipe('armor_of_magma_boots', 'combat',
           [(Item('enchanted_magma_cream'), 48)],
           (get_item('armor_of_magma_boots'), 1),
           collection_req=('magma_cream', 8)),

    Recipe('magma_bow', 'combat',
           [(Item('enchanted_magma_cream'), 96),
            (Item('enchanted_string'), 3)],
           (get_item('magma_bow'), 1),
           collection_req=('magma_cream', 9)),
]