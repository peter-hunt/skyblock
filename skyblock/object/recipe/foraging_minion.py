from ..item import get_item
from ..object import *


FORAGING_MINION_RECIPES = [
    Recipe('oak_minion_1', 'foraging',
           [(get_item('wooden_axe'), 1),
            (Item('oak_wood'), 80)],
           (get_item('oak_minion', tier=1), 1),
           collection_req=('oak_wood', 1)),
    Recipe('oak_minion_2', 'foraging',
           [(get_item('oak_minion', tier=1), 1),
            (Item('oak_wood'), 160)],
           (get_item('oak_minion', tier=2), 1),
           collection_req=('oak_wood', 1)),
    Recipe('oak_minion_3', 'foraging',
           [(get_item('oak_minion', tier=2), 1),
            (Item('oak_wood'), 320)],
           (get_item('oak_minion', tier=3), 1),
           collection_req=('oak_wood', 1)),
    Recipe('oak_minion_4', 'foraging',
           [(get_item('oak_minion', tier=3), 1),
            (Item('oak_wood'), 512)],
           (get_item('oak_minion', tier=4), 1),
           collection_req=('oak_wood', 1)),
    Recipe('oak_minion_5', 'foraging',
           [(get_item('oak_minion', tier=4), 1),
            (Item('enchanted_oak'), 8)],
           (get_item('oak_minion', tier=5), 1),
           collection_req=('oak_wood', 1)),
    Recipe('oak_minion_6', 'foraging',
           [(get_item('oak_minion', tier=5), 1),
            (Item('enchanted_oak'), 16)],
           (get_item('oak_minion', tier=6), 1),
           collection_req=('oak_wood', 1)),
    Recipe('oak_minion_7', 'foraging',
           [(get_item('oak_minion', tier=6), 1),
            (Item('enchanted_oak'), 32)],
           (get_item('oak_minion', tier=7), 1),
           collection_req=('oak_wood', 1)),
    Recipe('oak_minion_8', 'foraging',
           [(get_item('oak_minion', tier=7), 1),
            (Item('enchanted_oak'), 64)],
           (get_item('oak_minion', tier=8), 1),
           collection_req=('oak_wood', 1)),
    Recipe('oak_minion_9', 'foraging',
           [(get_item('oak_minion', tier=8), 1),
            (Item('enchanted_oak'), 128)],
           (get_item('oak_minion', tier=9), 1),
           collection_req=('oak_wood', 1)),
    Recipe('oak_minion_10', 'foraging',
           [(get_item('oak_minion', tier=9), 1),
            (Item('enchanted_oak'), 256)],
           (get_item('oak_minion', tier=10), 1),
           collection_req=('oak_wood', 1)),
    Recipe('oak_minion_11', 'foraging',
           [(get_item('oak_minion', tier=10), 1),
            (Item('enchanted_oak'), 512)],
           (get_item('oak_minion', tier=11), 1),
           collection_req=('oak_wood', 1)),
    RecipeGroup('oak_minion', 'foraging',
                ['oak_minion_1', 'oak_minion_2', 'oak_minion_3',
                 'oak_minion_4', 'oak_minion_5', 'oak_minion_6',
                 'oak_minion_7', 'oak_minion_8', 'oak_minion_9',
                 'oak_minion_10', 'oak_minion_11'],
                collection_req=('oak_wood', 1)),

    Recipe('birch_minion_1', 'foraging',
           [(get_item('wooden_axe'), 1),
            (Item('birch_wood'), 80)],
           (get_item('birch_minion', tier=1), 1),
           collection_req=('birch_wood', 1)),
    Recipe('birch_minion_2', 'foraging',
           [(get_item('birch_minion', tier=1), 1),
            (Item('birch_wood'), 160)],
           (get_item('birch_minion', tier=2), 1),
           collection_req=('birch_wood', 1)),
    Recipe('birch_minion_3', 'foraging',
           [(get_item('birch_minion', tier=2), 1),
            (Item('birch_wood'), 320)],
           (get_item('birch_minion', tier=3), 1),
           collection_req=('birch_wood', 1)),
    Recipe('birch_minion_4', 'foraging',
           [(get_item('birch_minion', tier=3), 1),
            (Item('birch_wood'), 512)],
           (get_item('birch_minion', tier=4), 1),
           collection_req=('birch_wood', 1)),
    Recipe('birch_minion_5', 'foraging',
           [(get_item('birch_minion', tier=4), 1),
            (Item('enchanted_birch'), 8)],
           (get_item('birch_minion', tier=5), 1),
           collection_req=('birch_wood', 1)),
    Recipe('birch_minion_6', 'foraging',
           [(get_item('birch_minion', tier=5), 1),
            (Item('enchanted_birch'), 16)],
           (get_item('birch_minion', tier=6), 1),
           collection_req=('birch_wood', 1)),
    Recipe('birch_minion_7', 'foraging',
           [(get_item('birch_minion', tier=6), 1),
            (Item('enchanted_birch'), 32)],
           (get_item('birch_minion', tier=7), 1),
           collection_req=('birch_wood', 1)),
    Recipe('birch_minion_8', 'foraging',
           [(get_item('birch_minion', tier=7), 1),
            (Item('enchanted_birch'), 64)],
           (get_item('birch_minion', tier=8), 1),
           collection_req=('birch_wood', 1)),
    Recipe('birch_minion_9', 'foraging',
           [(get_item('birch_minion', tier=8), 1),
            (Item('enchanted_birch'), 128)],
           (get_item('birch_minion', tier=9), 1),
           collection_req=('birch_wood', 1)),
    Recipe('birch_minion_10', 'foraging',
           [(get_item('birch_minion', tier=9), 1),
            (Item('enchanted_birch'), 256)],
           (get_item('birch_minion', tier=10), 1),
           collection_req=('birch_wood', 1)),
    Recipe('birch_minion_11', 'foraging',
           [(get_item('birch_minion', tier=10), 1),
            (Item('enchanted_birch'), 512)],
           (get_item('birch_minion', tier=11), 1),
           collection_req=('birch_wood', 1)),
    RecipeGroup('birch_minion', 'foraging',
                ['birch_minion_1', 'birch_minion_2', 'birch_minion_3',
                 'birch_minion_4', 'birch_minion_5', 'birch_minion_6',
                 'birch_minion_7', 'birch_minion_8', 'birch_minion_9',
                 'birch_minion_10', 'birch_minion_11'],
                collection_req=('birch_wood', 1)),

    Recipe('spruce_minion_1', 'foraging',
           [(get_item('wooden_axe'), 1),
            (Item('spruce_wood'), 80)],
           (get_item('spruce_minion', tier=1), 1),
           collection_req=('spruce_wood', 1)),
    Recipe('spruce_minion_2', 'foraging',
           [(get_item('spruce_minion', tier=1), 1),
            (Item('spruce_wood'), 160)],
           (get_item('spruce_minion', tier=2), 1),
           collection_req=('spruce_wood', 1)),
    Recipe('spruce_minion_3', 'foraging',
           [(get_item('spruce_minion', tier=2), 1),
            (Item('spruce_wood'), 320)],
           (get_item('spruce_minion', tier=3), 1),
           collection_req=('spruce_wood', 1)),
    Recipe('spruce_minion_4', 'foraging',
           [(get_item('spruce_minion', tier=3), 1),
            (Item('spruce_wood'), 512)],
           (get_item('spruce_minion', tier=4), 1),
           collection_req=('spruce_wood', 1)),
    Recipe('spruce_minion_5', 'foraging',
           [(get_item('spruce_minion', tier=4), 1),
            (Item('enchanted_spruce'), 8)],
           (get_item('spruce_minion', tier=5), 1),
           collection_req=('spruce_wood', 1)),
    Recipe('spruce_minion_6', 'foraging',
           [(get_item('spruce_minion', tier=5), 1),
            (Item('enchanted_spruce'), 16)],
           (get_item('spruce_minion', tier=6), 1),
           collection_req=('spruce_wood', 1)),
    Recipe('spruce_minion_7', 'foraging',
           [(get_item('spruce_minion', tier=6), 1),
            (Item('enchanted_spruce'), 32)],
           (get_item('spruce_minion', tier=7), 1),
           collection_req=('spruce_wood', 1)),
    Recipe('spruce_minion_8', 'foraging',
           [(get_item('spruce_minion', tier=7), 1),
            (Item('enchanted_spruce'), 64)],
           (get_item('spruce_minion', tier=8), 1),
           collection_req=('spruce_wood', 1)),
    Recipe('spruce_minion_9', 'foraging',
           [(get_item('spruce_minion', tier=8), 1),
            (Item('enchanted_spruce'), 128)],
           (get_item('spruce_minion', tier=9), 1),
           collection_req=('spruce_wood', 1)),
    Recipe('spruce_minion_10', 'foraging',
           [(get_item('spruce_minion', tier=9), 1),
            (Item('enchanted_spruce'), 256)],
           (get_item('spruce_minion', tier=10), 1),
           collection_req=('spruce_wood', 1)),
    Recipe('spruce_minion_11', 'foraging',
           [(get_item('spruce_minion', tier=10), 1),
            (Item('enchanted_spruce'), 512)],
           (get_item('spruce_minion', tier=11), 1),
           collection_req=('spruce_wood', 1)),
    RecipeGroup('spruce_minion', 'foraging',
                ['spruce_minion_1', 'spruce_minion_2', 'spruce_minion_3',
                 'spruce_minion_4', 'spruce_minion_5', 'spruce_minion_6',
                 'spruce_minion_7', 'spruce_minion_8', 'spruce_minion_9',
                 'spruce_minion_10', 'spruce_minion_11'],
                collection_req=('spruce_wood', 1)),

    Recipe('dark_oak_minion_1', 'foraging',
           [(get_item('wooden_axe'), 1),
            (Item('dark_oak_wood'), 80)],
           (get_item('dark_oak_minion', tier=1), 1),
           collection_req=('dark_oak_wood', 1)),
    Recipe('dark_oak_minion_2', 'foraging',
           [(get_item('dark_oak_minion', tier=1), 1),
            (Item('dark_oak_wood'), 160)],
           (get_item('dark_oak_minion', tier=2), 1),
           collection_req=('dark_oak_wood', 1)),
    Recipe('dark_oak_minion_3', 'foraging',
           [(get_item('dark_oak_minion', tier=2), 1),
            (Item('dark_oak_wood'), 320)],
           (get_item('dark_oak_minion', tier=3), 1),
           collection_req=('dark_oak_wood', 1)),
    Recipe('dark_oak_minion_4', 'foraging',
           [(get_item('dark_oak_minion', tier=3), 1),
            (Item('dark_oak_wood'), 512)],
           (get_item('dark_oak_minion', tier=4), 1),
           collection_req=('dark_oak_wood', 1)),
    Recipe('dark_oak_minion_5', 'foraging',
           [(get_item('dark_oak_minion', tier=4), 1),
            (Item('enchanted_dark_oak'), 8)],
           (get_item('dark_oak_minion', tier=5), 1),
           collection_req=('dark_oak_wood', 1)),
    Recipe('dark_oak_minion_6', 'foraging',
           [(get_item('dark_oak_minion', tier=5), 1),
            (Item('enchanted_dark_oak'), 16)],
           (get_item('dark_oak_minion', tier=6), 1),
           collection_req=('dark_oak_wood', 1)),
    Recipe('dark_oak_minion_7', 'foraging',
           [(get_item('dark_oak_minion', tier=6), 1),
            (Item('enchanted_dark_oak'), 32)],
           (get_item('dark_oak_minion', tier=7), 1),
           collection_req=('dark_oak_wood', 1)),
    Recipe('dark_oak_minion_8', 'foraging',
           [(get_item('dark_oak_minion', tier=7), 1),
            (Item('enchanted_dark_oak'), 64)],
           (get_item('dark_oak_minion', tier=8), 1),
           collection_req=('dark_oak_wood', 1)),
    Recipe('dark_oak_minion_9', 'foraging',
           [(get_item('dark_oak_minion', tier=8), 1),
            (Item('enchanted_dark_oak'), 128)],
           (get_item('dark_oak_minion', tier=9), 1),
           collection_req=('dark_oak_wood', 1)),
    Recipe('dark_oak_minion_10', 'foraging',
           [(get_item('dark_oak_minion', tier=9), 1),
            (Item('enchanted_dark_oak'), 256)],
           (get_item('dark_oak_minion', tier=10), 1),
           collection_req=('dark_oak_wood', 1)),
    Recipe('dark_oak_minion_11', 'foraging',
           [(get_item('dark_oak_minion', tier=10), 1),
            (Item('enchanted_dark_oak'), 512)],
           (get_item('dark_oak_minion', tier=11), 1),
           collection_req=('dark_oak_wood', 1)),
    RecipeGroup('dark_oak_minion', 'foraging',
                ['dark_oak_minion_1', 'dark_oak_minion_2', 'dark_oak_minion_3',
                 'dark_oak_minion_4', 'dark_oak_minion_5', 'dark_oak_minion_6',
                 'dark_oak_minion_7', 'dark_oak_minion_8', 'dark_oak_minion_9',
                 'dark_oak_minion_10', 'dark_oak_minion_11'],
                collection_req=('dark_oak_wood', 1)),

    Recipe('acacia_minion_1', 'foraging',
           [(get_item('wooden_axe'), 1),
            (Item('acacia_wood'), 80)],
           (get_item('acacia_minion', tier=1), 1),
           collection_req=('acacia_wood', 1)),
    Recipe('acacia_minion_2', 'foraging',
           [(get_item('acacia_minion', tier=1), 1),
            (Item('acacia_wood'), 160)],
           (get_item('acacia_minion', tier=2), 1),
           collection_req=('acacia_wood', 1)),
    Recipe('acacia_minion_3', 'foraging',
           [(get_item('acacia_minion', tier=2), 1),
            (Item('acacia_wood'), 320)],
           (get_item('acacia_minion', tier=3), 1),
           collection_req=('acacia_wood', 1)),
    Recipe('acacia_minion_4', 'foraging',
           [(get_item('acacia_minion', tier=3), 1),
            (Item('acacia_wood'), 512)],
           (get_item('acacia_minion', tier=4), 1),
           collection_req=('acacia_wood', 1)),
    Recipe('acacia_minion_5', 'foraging',
           [(get_item('acacia_minion', tier=4), 1),
            (Item('enchanted_acacia'), 8)],
           (get_item('acacia_minion', tier=5), 1),
           collection_req=('acacia_wood', 1)),
    Recipe('acacia_minion_6', 'foraging',
           [(get_item('acacia_minion', tier=5), 1),
            (Item('enchanted_acacia'), 16)],
           (get_item('acacia_minion', tier=6), 1),
           collection_req=('acacia_wood', 1)),
    Recipe('acacia_minion_7', 'foraging',
           [(get_item('acacia_minion', tier=6), 1),
            (Item('enchanted_acacia'), 32)],
           (get_item('acacia_minion', tier=7), 1),
           collection_req=('acacia_wood', 1)),
    Recipe('acacia_minion_8', 'foraging',
           [(get_item('acacia_minion', tier=7), 1),
            (Item('enchanted_acacia'), 64)],
           (get_item('acacia_minion', tier=8), 1),
           collection_req=('acacia_wood', 1)),
    Recipe('acacia_minion_9', 'foraging',
           [(get_item('acacia_minion', tier=8), 1),
            (Item('enchanted_acacia'), 128)],
           (get_item('acacia_minion', tier=9), 1),
           collection_req=('acacia_wood', 1)),
    Recipe('acacia_minion_10', 'foraging',
           [(get_item('acacia_minion', tier=9), 1),
            (Item('enchanted_acacia'), 256)],
           (get_item('acacia_minion', tier=10), 1),
           collection_req=('acacia_wood', 1)),
    Recipe('acacia_minion_11', 'foraging',
           [(get_item('acacia_minion', tier=10), 1),
            (Item('enchanted_acacia'), 512)],
           (get_item('acacia_minion', tier=11), 1),
           collection_req=('acacia_wood', 1)),
    RecipeGroup('acacia_minion', 'foraging',
                ['acacia_minion_1', 'acacia_minion_2', 'acacia_minion_3',
                 'acacia_minion_4', 'acacia_minion_5', 'acacia_minion_6',
                 'acacia_minion_7', 'acacia_minion_8', 'acacia_minion_9',
                 'acacia_minion_10', 'acacia_minion_11'],
                collection_req=('acacia_wood', 1)),

    Recipe('jungle_minion_1', 'foraging',
           [(get_item('wooden_axe'), 1),
            (Item('jungle_wood'), 80)],
           (get_item('jungle_minion', tier=1), 1),
           collection_req=('jungle_wood', 1)),
    Recipe('jungle_minion_2', 'foraging',
           [(get_item('jungle_minion', tier=1), 1),
            (Item('jungle_wood'), 160)],
           (get_item('jungle_minion', tier=2), 1),
           collection_req=('jungle_wood', 1)),
    Recipe('jungle_minion_3', 'foraging',
           [(get_item('jungle_minion', tier=2), 1),
            (Item('jungle_wood'), 320)],
           (get_item('jungle_minion', tier=3), 1),
           collection_req=('jungle_wood', 1)),
    Recipe('jungle_minion_4', 'foraging',
           [(get_item('jungle_minion', tier=3), 1),
            (Item('jungle_wood'), 512)],
           (get_item('jungle_minion', tier=4), 1),
           collection_req=('jungle_wood', 1)),
    Recipe('jungle_minion_5', 'foraging',
           [(get_item('jungle_minion', tier=4), 1),
            (Item('enchanted_jungle'), 8)],
           (get_item('jungle_minion', tier=5), 1),
           collection_req=('jungle_wood', 1)),
    Recipe('jungle_minion_6', 'foraging',
           [(get_item('jungle_minion', tier=5), 1),
            (Item('enchanted_jungle'), 16)],
           (get_item('jungle_minion', tier=6), 1),
           collection_req=('jungle_wood', 1)),
    Recipe('jungle_minion_7', 'foraging',
           [(get_item('jungle_minion', tier=6), 1),
            (Item('enchanted_jungle'), 32)],
           (get_item('jungle_minion', tier=7), 1),
           collection_req=('jungle_wood', 1)),
    Recipe('jungle_minion_8', 'foraging',
           [(get_item('jungle_minion', tier=7), 1),
            (Item('enchanted_jungle'), 64)],
           (get_item('jungle_minion', tier=8), 1),
           collection_req=('jungle_wood', 1)),
    Recipe('jungle_minion_9', 'foraging',
           [(get_item('jungle_minion', tier=8), 1),
            (Item('enchanted_jungle'), 128)],
           (get_item('jungle_minion', tier=9), 1),
           collection_req=('jungle_wood', 1)),
    Recipe('jungle_minion_10', 'foraging',
           [(get_item('jungle_minion', tier=9), 1),
            (Item('enchanted_jungle'), 256)],
           (get_item('jungle_minion', tier=10), 1),
           collection_req=('jungle_wood', 1)),
    Recipe('jungle_minion_11', 'foraging',
           [(get_item('jungle_minion', tier=10), 1),
            (Item('enchanted_jungle'), 512)],
           (get_item('jungle_minion', tier=11), 1),
           collection_req=('jungle_wood', 1)),
    RecipeGroup('jungle_minion', 'foraging',
                ['jungle_minion_1', 'jungle_minion_2', 'jungle_minion_3',
                 'jungle_minion_4', 'jungle_minion_5', 'jungle_minion_6',
                 'jungle_minion_7', 'jungle_minion_8', 'jungle_minion_9',
                 'jungle_minion_10', 'jungle_minion_11'],
                collection_req=('jungle_wood', 1)),
]