from ...constant.color import GREEN, AQUA, RED, WHITE
from ...object.item import get_item, get_scroll
from ...object.object import Item
from ...object.mob import get_mob
from ...object.resource import get_resource

from ..object import Npc, Region, Island, add_dist


__all__ = ['HUB']

AUCTION_HOUSE = Region('auction_house', -18, -90)
BANK = Region('bank', -20, -65)
BAZAAR_ALLEY = Region(
    'bazaar_alley', -32, -76,
    npcs=[
        Npc('adventurer',
            init_dialog=[
                ("I've seen it all - every island"
                 " from here to the edge of the world!"),
                ("Over the years I've acquired"
                 " a variety of Talismans and Artifacts."),
                'For a price, you can have it all!',
                'Talk to me again to open the Adventurer Shop!'],
            trades=[
                (8, Item('rotten_flesh')),
                (8, Item('bone')),
                (10, Item('string')),
                (14, Item('slime_ball')),
                (10, Item('gunpowder'))]),
        Npc('lumber_merchant',
            init_dialog=[
                'Buy and sell wood and axes with me!',
                'Talk to me again to open the Lumberjack Shop!'],
            trades=[
                (5, Item('oak_wood')),
                (5, Item('birch_wood')),
                (5, Item('spruce_wood')),
                (5, Item('dark_oak_wood')),
                (5, Item('acacia_wood')),
                (5, Item('jungle_wood')),
                (12, Item('rookie_axe')),
                (35, Item('promising_axe')),
                (100, Item('sweet_axe')),
                (100, Item('efficient_axe'))])])
BLACKSMITH = Region('blacksmith', -28, -125)
BUILDERS_HOUSE = Region(
    'builders_house', -50, -36,
    npcs=[
        Npc('builder',
            init_dialog=[
                'If you build, they will come!',
                'Talk to me again to open the Builder Shop!'],
            trades=[
                (22, Item('gravel')),
                (69, Item('obsidian')),
                (1, Item('cobblestone')),
                (1, Item('sand'))])])
COAL_MINE = Region(
    'coal_mine', -20, -160,
    resources=[get_resource('stone'), get_resource('coal_ore')],
    portal='gold')
COLOSSEUM = Region('colosseum', -58, -58)
COMMUNITY_CENTER = Region('community_center', 0, -100)
CRYPT = Region(
    'crypt', -120, -100,
    mobs=[get_mob('crypt_ghoul'),
          get_mob('golden_ghoul')])
FARM = Region(
    'farm', 41, -137,
    resources=[get_resource('wheat')],
    portal='barn')
FARMHOUSE = Region(
    'farmhouse', 23, -80,
    npcs=[
        Npc('farm_merchant',
            init_dialog=[
                'You can buy and sell harvested crops with me!',
                'Wheat, carrots, potatoes, and melon are my specialties!',
                'Talk to me again to open the Farmer Shop!'],
            trades=[
                (7/3, Item('wheat')),
                (7/3, Item('carrot')),
                (7/3, Item('potato')),
                (8, Item('pumpkin')),
                (2, Item('melon')),
                (12, Item('red_mushroom')),
                (12, Item('brown_mushroom')),
                (5, Item('cocoa_beans')),
                (5, Item('sugar_cane')),
                (4, Item('sand')),
                (10, get_item('rookie_hoe'))]),
        Npc('jacob',
            dialog=[[
                'Howdy!',
                'I organize farming contests once every few days!',
                'You need Farming X to participate! :)']]),
        Npc('anita')])
FASHION_SHOP = Region(
    'fashion_shop', 27, -44,
    npcs=[
        Npc('seymour',
            init_dialog=['Looking to buy something fancy?'],
            trades=[
                (3_000_000, [get_item('cheap_tuxedo_jacket'),
                             get_item('cheap_tuxedo_pants'),
                             get_item('cheap_tuxedo_oxfords')]),
                (20_000_000, [get_item('fancy_tuxedo_jacket'),
                              get_item('fancy_tuxedo_pants'),
                              get_item('fancy_tuxedo_oxfords')]),
                (79_999_999, [get_item('elegant_tuxedo_jacket'),
                              get_item('elegant_tuxedo_pants'),
                              get_item('elegant_tuxedo_oxfords')])]),
        Npc('taylor',
            dialog=[
                'Hello!',
                'You look dashing today!',
                'Would you like to buy something?']), ])
FLOWER_HOUSE = Region(
    'flower_house', -7, -25,
    resources=[get_resource('dandelion'), get_resource('poppy')])
FOREST = Region(
    'forest', -95, -40,
    resources=[get_resource('oak_wood')],
    portal='park')
GRAVEYARD = Region(
    'graveyard', -99, -54,
    npcs=[
        Npc('pat',
            init_dialog=[
                'You like flint? I like flint! I sell flint!',
                ("My brother is mining the gravel from the Spider's Den."
                 " We are the Flint Bros!"),
                'Click me again to open my shop!'],
            trades=[
                (6, Item('flint')),
                (4, Item('gravel'))])],
    mobs=[get_mob('zombie', level=1)],
    portal='spider')
HIGH_LEVEL = Region(
    'high_level', 0, 150,
    mobs=[get_mob('skeleton', level=6)])
HUB_CASTLE = Region(
    'castle', -280, -60,
    npcs=[
        Npc('armorsmith',
            init_dialog=['To fast travel or not to fast travel?'],
            trades=[(150_000, get_scroll('castle'))])],
    mobs=[get_mob('wolf'),
          get_mob('old_wolf')])
LIBRARY = Region(
    'library', 37, -111,
    npcs=[
        Npc('librarian',
            init_dialog=[
                'Greetings! Welcome to the Library!',
                ('The Library is your one-stop shop for all things enchanting.'
                 ' Enchant items, purchase Enchanted Books, and more'),
                ('You can enchant items with `enchant`.'
                 ' Enchanting costs experience levels -'
                 ' the more levels you spend, the better enchantments'
                 ' you will receive.'),
                'Use `enchant` to enchant an item!'],
            trades=[
                (30, Item('experience_bottle'))])])
MOUNTAIN = Region('mountain', 0, 0)
PETS_BUILDING = Region(
    'pets_building', 24, -90,
    npcs=[
        Npc('bea',
            init_dialog=[
                'Hello! Do you have a pet?',
                'Pets are little companions for your adventures in SkyBlock!',
                'Personally, I prefer the bee pet!'],
            trades=[
                ((4_999,
                  (Item('coal_block'), 2),
                  (Item('gold_block'), 2)),
                 get_item('bee_pet', rarity='common')),
                ((50_000,
                  (Item('coal_block'), 128),
                  (Item('gold_block'), 128)),
                 get_item('bee_pet', rarity='rare')),
                ((200_000,
                  (Item('enchanted_coal_block'), 1),
                  (Item('enchanted_gold_block'), 1)),
                 get_item('bee_pet', rarity='epic')),
                ((650_000,
                  (Item('enchanted_coal_block'), 8),
                  (Item('enchanted_gold_block'), 8)),
                 get_item('bee_pet', rarity='legendary'))])])
POTION_SHOP = Region(
    'potion_shop', 41, -63,
    resources=[get_resource('nether_wart')],
    npcs=[
        Npc('alchemist',
            init_dialog=[
                'There is a darkness in you, adventurer',
                "I've seen it in my flames, you are destined for great things.",
                "For now, you shouldn't let it get to your head.",
                'Talk to me again to open the Alchemist Shop!'],
            trades=[
                (10, Item('nether_wart')),
                (6, Item('bottle')),
                (4, Item('sugar')),
                (10, Item('rabbit_foot')),
                (12, Item('spider_eye')),
                (12, Item('blaze_powder')),
                (200, Item('ghast_tear')),
                (20, Item('magma_cream'))])])
RUINS = Region(
    'ruins', -250, -80,
    mobs=[get_mob('wolf'),
          get_mob('old_wolf')])
TAVERN = Region('tavern', -85, -69)
VILLAGE = Region(
    'village', -3, -85,
    npcs=[
        Npc('andrew',
            dialog=[
                (f"This game is still under heavy development,"
                 f" don't forget to check"
                 f" {GREEN}GitHub{WHITE} often for updates!"),
                (f"If you'd like to discuss SkyBlock with other players"
                 f" then check out the SkyBlock respository"
                 f" on {GREEN}GitHub{WHITE}!")]),
        Npc('armorsmith',
            init_dialog=[
                'A great warrior is nothing without their armor!',
                'Talk to me again to open the Armorsmith Shop!'],
            trades=[
                (8, get_item('leather_helmet')),
                (14, get_item('leather_chestplate')),
                (16, get_item('leather_leggings')),
                (10, get_item('leather_boots')),
                (15, get_item('iron_helmet')),
                (20, get_item('iron_chestplate')),
                (30, get_item('iron_leggings')),
                (20, get_item('iron_boots')),
                (350, get_item('diamond_helmet',
                               enchantments={'growth': 1})),
                (440, get_item('diamond_chestplate',
                               enchantments={'growth': 1})),
                (400, get_item('diamond_leggings',
                               enchantments={'growth': 1})),
                (320, get_item('diamond_boots',
                               enchantments={'growth': 1}))]),
        Npc('duke',
            dialog=[
                'Are you new here? As you can see there is a lot to explore!',
                (f'My advice is to start by visiting the {AQUA}Farm{WHITE},'
                 f' or the {AQUA}Coal Mine{WHITE} both North of here.'),
                (f'If you do need some wood, the best place '
                 f'to get some is West of the {AQUA}Village{WHITE}!')]),
        Npc('fish_merchant',
            init_dialog=[
                ('Fishing is my trade. I buy and sell any fish,'
                 ' rod, or treasure you can find!'),
                'Click me again to open the Fisherman Shop!'],
            trades=[
                (100, get_item('fishing_rod', enchantments={'magnet': 1})),
                (20, Item('raw_fish')),
                (30, Item('raw_salmon')),
                (100, Item('clownfish')),
                (40, Item('pufferfish'))]),
        Npc('jack',
            dialog=[
                "Use 'stats' to show details about your current stats!",
                (f'There are 7 stats in total,'
                 f' including {RED}❤ Health{WHITE}, {RED}❁  Strength{WHITE},'
                 f' and {GREEN}❈ Defense{WHITE}.'),
                ('Equipped armor, weapons, and accessories in your inventory'
                 ' all improve your stats.'),
                ('Additionally, leveling your Skills can permanently'
                 ' boost some of your stats!')]),
        Npc('jamie',
            init_dialog=[
                'You might have noticed that you have a Mana bar!',
                'Some items have mysterious properties, called Abilities.',
                ("Abilities use your Mana as a resource. "
                 "Here, take this Rogue Sword. I don't need it!")],
            claim_item=get_item('rogue_sword')),
        Npc('liam',
            dialog=[
                ('One day those houses in the Village'
                 ' will be rentable for Coins!'),
                ('Anyone will be able to rent them,'
                 ' players, co-ops, even Guilds!')]),
        Npc('mine_merchant',
            init_dialog=[
                'My specialties are ores, stone, and mining equipment.',
                'Talk to me again to open the Miner Shop!'],
            trades=[
                (4, Item('coal')),
                (5.5, Item('iron')),
                (6, Item('gold')),
                (12, get_item('rookie_pickaxe')),
                (35, get_item('promising_pickaxe')),
                (((Item('gold'), 3),),
                 get_item('golden_pickaxe')),
                (6, Item('gravel')),
                (3, Item('cobblestone'))]),
        Npc('ryu',
            dialog=[
                'There are 9 Skills in SkyBlock!',
                ('Farming, Mining, Foraging, Fishing, Combat,'
                 ' Enchanting, Alchemy, Carpentry and Runecrafting.'),
                f"You can learn all about them with {GREEN}'skills'{WHITE}."]),
        Npc('weaponsmith',
            init_dialog=[
                ("You'll need some strong weapons to survive out in the wild! "
                 "Lucky for you, I've got some!"),
                'Talk to me again to open the Weaponsmith Shop!'],
            trades=[
                (100, get_item('undead_sword')),
                (150, get_item('end_sword')),
                (100, get_item('spider_sword')),
                (60, get_item('diamond_sword')),
                (25, get_item('bow')),
                (10/3, Item('arrow')),
                (250, get_item('wither_bow'))])])
WILDERNESS = Region('wilderness', 75, -11)
WIZARD_TOWER = Region('wizard_tower', 40, 70)


HUB_JOINTS = [
    AUCTION_HOUSE, BANK, BAZAAR_ALLEY, BLACKSMITH, BUILDERS_HOUSE, COAL_MINE,
    COMMUNITY_CENTER, FARM, FARMHOUSE, FASHION_SHOP, FLOWER_HOUSE, FOREST,
    GRAVEYARD, HIGH_LEVEL, HUB_CASTLE, CRYPT, LIBRARY, MOUNTAIN, PETS_BUILDING,
    POTION_SHOP, RUINS, TAVERN, VILLAGE, WILDERNESS, WIZARD_TOWER]

HUB_CONNS = [
    (AUCTION_HOUSE, BAZAAR_ALLEY),
    (AUCTION_HOUSE, LIBRARY),
    (AUCTION_HOUSE, VILLAGE),
    (BANK, BAZAAR_ALLEY),
    (BANK, BUILDERS_HOUSE),
    (BANK, FLOWER_HOUSE),
    (BANK, VILLAGE),
    (BAZAAR_ALLEY, BUILDERS_HOUSE),
    (BAZAAR_ALLEY, FOREST),
    (BAZAAR_ALLEY, VILLAGE),
    (BLACKSMITH, COAL_MINE),
    (BLACKSMITH, LIBRARY),
    (BLACKSMITH, VILLAGE),
    (BUILDERS_HOUSE, VILLAGE),
    (COAL_MINE, FARM),
    (COAL_MINE, GRAVEYARD),
    (COAL_MINE, VILLAGE),
    (COLOSSEUM, FARM),
    (COLOSSEUM, WILDERNESS),
    (COMMUNITY_CENTER, VILLAGE),
    (CRYPT, FOREST),
    (CRYPT, GRAVEYARD),
    (FARM, PETS_BUILDING),
    (FARM, VILLAGE),
    (FARMHOUSE, VILLAGE),
    (FASHION_SHOP, VILLAGE),
    (FLOWER_HOUSE, VILLAGE),
    (FOREST, GRAVEYARD),
    (FOREST, HIGH_LEVEL),
    (FOREST, MOUNTAIN),
    (FOREST, RUINS),
    (FOREST, TAVERN),
    (FOREST, VILLAGE),
    (HIGH_LEVEL, MOUNTAIN),
    (HIGH_LEVEL, RUINS),
    (HIGH_LEVEL, WILDERNESS),
    (HIGH_LEVEL, WIZARD_TOWER),
    (HUB_CASTLE, RUINS),
    (LIBRARY, VILLAGE),
    (MOUNTAIN, RUINS),
    (MOUNTAIN, VILLAGE),
    (MOUNTAIN, WILDERNESS),
    (MOUNTAIN, WIZARD_TOWER),
    (PETS_BUILDING, VILLAGE),
    (POTION_SHOP, VILLAGE),
    (TAVERN, VILLAGE),
    (WILDERNESS, WIZARD_TOWER)]

HUB_DISTS = {}

for conn in HUB_CONNS:
    add_dist(*conn, HUB_DISTS)

HUB = Island('hub', 'village', HUB_JOINTS, HUB_CONNS, HUB_DISTS)
