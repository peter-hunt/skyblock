from ...constant.color import BLUE, GREEN, AQUA, RED, WHITE
from ...object.mob import get_mob
from ...object.resource import get_resource

from ..object import Npc, Region, Island, add_dist


__all__ = ['SPIDER']

FOSSIL = Region(
    'fossil', -340, -255,
    npcs=[
        Npc('bramass_beastslayer',
            init_dialog=[
                (f"Hello, adventurer! I am {RED}Bramass Beastslayer{WHITE}!"
                 f" I've slain beasts of all sorts across SkyBlock"),
                ('I sure wish there was a record all of'
                 ' my accomplishments in one place!'),
                'Oh wait...there is!',
                (f'Your {BLUE}Bestiary{WHITE} is'
                 f' a compendium of all of the mobs in SkyBlock!'),
                'View your mob stats, unlock rewards, and more!',
                f"You can find the Bestiary with {GREEN}/bestiary{WHITE}!"],
            dialog=[[
                (f'Killing enough mobs in a given {GREEN}Family{WHITE}'
                 f' unlocks {GREEN}rewards{WHITE}!'),
                (f'You can unlock {AQUA}Magic Find{WHITE}, Strength bonuses,'
                 f' and loot drop information for that Family!'),
                ('Reach Milestones in your Beastiary'
                 ' by unlocking unique Family tiers'),
                (f'Reaching Milestones rewards Health,'
                 f' {BLUE}Combat Exp{WHITE}, and more!'),
                (f'You can always view your Beastiary'
                 f' with {GREEN}/bestiary{WHITE}!'),
                (f'Killing mobs in a Family enough times rewards you '
                 f'with {AQUA}Magic Find{WHITE} towards that mob!'),
                ('This increases your chance to find rare loot'
                 ' when killing this mob!')]])],
    portal='end')
SPIDERS_PATH = Region(
    'spiders_path', -315, -240,
    npcs=[
        Npc('haysmith',
            init_dialog=[
                'Easy there, adventurer! Lots of spiders creeping about!',
                'Personally I love them, collecting string is my passion.',
                'You should try it!'],
            dialog=[
                'String! Yes! Wow!',
                ("The gravel on this island seems to magically reappear"
                 " when you break it. I don't ask questions"),
                ('Those Dashing Spiders are pretty obnoxious.'
                 ' I find a well-placed arrow can help with that.')])],
    mobs=[get_mob('gravel_skeleton'),
          get_mob('rainy_slime')],
    portal='hub')
SPIDER_TOWER = Region(
    'spider_tower', -380, -210,
    mobs=[get_mob('weaver_spider'),
          get_mob('voracious_spider'),
          get_mob('dasher_spider')])
GRAVEL_MINE = Region(
    'gravel_mine', -250, -320,
    npcs=[
        Npc('rick',
            dialog=[
                'Careful when it rains around here, it gets dangerous!',
                "Have you met Pat? He's my brother, We're the Flint Bros!",
                'Mining gravel is hard work, but the flint is worth it.']),
    ],
    resources=[get_resource('gravel')],
    portal='nether')
TOP_OF_NEST = Region(
    'nest', -365, -220,
    mobs=[get_mob('splitter_spider'),
          get_mob('weaver_spider'),
          get_mob('dasher_spider')])

SPIDER_REGIONS = [FOSSIL, SPIDERS_PATH, SPIDER_TOWER, GRAVEL_MINE, TOP_OF_NEST]
SPIDER_CONNS = [
    (FOSSIL, SPIDERS_PATH),
    (GRAVEL_MINE, SPIDERS_PATH),
    (SPIDER_TOWER, SPIDERS_PATH),
    (TOP_OF_NEST, SPIDER_TOWER)]

SPIDER_DISTS = {}

for conn in SPIDER_CONNS:
    add_dist(*conn, SPIDER_DISTS)

SPIDER = Island(
    'spider', 'spiders_path', SPIDER_REGIONS, SPIDER_CONNS, SPIDER_DISTS,
    skill_req=('combat', 1))
