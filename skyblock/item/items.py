from .object import Item, Mineral, Tree, Pickaxe, Axe, Sword

__all__ = [
    'COLLECTIONS', 'RESOURCES', 'WEAPONS', 'TOOLS', 'ALL_ITEM',
]


COLLECTIONS = [
    Item('wheat', 64, 'common'),
    Item('carrot', 64, 'common'),
    Item('potato', 64, 'common'),
    Item('pumpkin', 64, 'common'),
    Item('melon', 64, 'common'),
    Item('seeds', 64, 'common'),
    Item('red_mushroom', 64, 'common'),
    Item('brown_mushroom', 64, 'common'),
    Item('cocoa_beans', 64, 'common'),
    Item('cactus', 64, 'common'),
    Item('sugar_cane', 64, 'common'),
    Item('feather', 64, 'common'),
    Item('leather', 64, 'common'),
    Item('porkchop', 64, 'common'),
    Item('chicken', 64, 'common'),
    Item('mutton', 64, 'common'),
    Item('rabbit', 64, 'common'),
    Item('nether_wart', 64, 'common'),

    Item('cobblestone', 64, 'common'),
    Item('coal', 64, 'common'),
    Item('iron_ingot', 64, 'common'),
    Item('gold_ingot', 64, 'common'),
    Item('diamond', 64, 'common'),
    Item('lapis_lazuli', 64, 'common'),
    Item('emerald', 64, 'common'),
    Item('redstone', 64, 'common'),
    Item('quartz', 64, 'common'),
    Item('obsidian', 64, 'common'),
    Item('glowstone_dust', 64, 'common'),
    Item('gravel', 64, 'common'),
    Item('ice', 64, 'common'),
    Item('netherrack', 64, 'common'),
    Item('sand', 64, 'common'),
    Item('endstone', 64, 'common'),
    Item('mithril', 64, 'common'),

    Item('oak_wood', 64, 'common'),
    Item('birch_wood', 64, 'common'),
    Item('spruce_wood', 64, 'common'),
    Item('dark_oak_wood', 64, 'common'),
    Item('acacia_wood', 64, 'common'),
    Item('jungle_wood', 64, 'common'),
]

RESOURCES = [
    Mineral('stone', 'cobblestone', 1, 1, 0, 1.5, 1),
    Mineral('coal_ore', 'coal', 1, 1, 1, 3, 5),

    Tree('oak', 'oak_wood', 2, 6),
    Tree('birch', 'birch_wood', 2, 6),
    Tree('spruce', 'spruce_wood', 2, 6),
    Tree('dark_oak', 'dark_oak_wood', 2, 6),
    Tree('acacia', 'acacia_wood', 2, 6),
    Tree('jungle', 'jungle_wood', 2, 6),
]

WEAPONS = [
    Sword('raider_axe', 'rare',
          damage=80, strength=50),

    Sword('aspect_of_the_dragons', 'legendary',
          damage=225, strength=100,
          combat_skill_req=18),

    Sword('livid_dagger', 'legendary',
          damage=210, strength=60, crit_chance=100, crit_damage=50,
          attack_speed=50,
          dungeon_completion_req=5),

    Sword('necrons_blade', 'legendary',
          damage=210, strength=60,
          defense=250, intelligence=50, true_denfense=20, ferocity=30,
          dungeon_completion_req=7, stars=0),
    Sword('astraea', 'legendary',
          damage=210, strength=60,
          defense=250, intelligence=50, true_denfense=20, ferocity=30,
          dungeon_completion_req=7, stars=0),
    Sword('hyperion', 'legendary',
          damage=260, strength=150,
          intelligence=350, ferocity=30,
          dungeon_completion_req=7, stars=0),
    Sword('scylla', 'legendary',
          damage=270, strength=150, crit_chance=12, crit_damage=35,
          intelligence=50, ferocity=30,
          dungeon_completion_req=7, stars=0),
    Sword('valkyrie', 'legendary',
          damage=270, strength=145,
          intelligence=60, ferocity=60,
          dungeon_completion_req=7, stars=0),
]

TOOLS = [
    Pickaxe('wooden_pickaxe', rarity='common',
            breaking_power=1, mining_speed=70),
    Pickaxe('golden_pickaxe', rarity='common',
            breaking_power=1, mining_speed=250),
    Pickaxe('stone_pickaxe', rarity='common',
            breaking_power=2, mining_speed=110),
    Pickaxe('iron_pickaxe', rarity='common',
            breaking_power=3, mining_speed=160),
    Pickaxe('diamond_pickaxe', rarity='uncommon',
            breaking_power=4, mining_speed=230),

    Axe('wooden_axe', rarity='common', tool_speed=2),
    Axe('stone_axe', rarity='common', tool_speed=4),
    Axe('golden_axe', rarity='common', tool_speed=12),
    Axe('iron_axe', rarity='common', tool_speed=6),
    Axe('wooden_axe', rarity='uncommon', tool_speed=8),
]

ALL_ITEM = COLLECTIONS + RESOURCES + WEAPONS + TOOLS
