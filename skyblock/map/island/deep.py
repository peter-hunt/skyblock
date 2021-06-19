from ...object.mob import get_mob
from ...object.resource import get_resource

from ..object import Npc, Region, Island, add_dist

__all__ = ['DEEP']


DEEP_ENTRENCE = Region(
    'deep_entrence', 0, 90,
    portal='gold',
)
GUNPOWDER_MINES = Region(
    'gunpowder_mines', 5, 20,
    resources=[get_resource('stone'), get_resource('coal_ore'),
               get_resource('iron_ore'), get_resource('gold_ore')],
    mobs=[get_mob('sneaky_creeper')],
)
LAPIS_QUARRY = Region(
    'lapis_quarry', -30, -35,
    resources=[get_resource('stone'), get_resource('lapis_ore')],
    mobs=[get_mob('lapis_zombie')],
)
PIGMANS_DEN = Region(
    'pigmans_den', -10, 70,
    resources=[get_resource('stone'), get_resource('redstone_ore')],
    mobs=[get_mob('redstone_pigman')],
)
SLIMEHILL = Region(
    'slilmehill', 20, -10,
    resources=[get_resource('stone'), get_resource('emerald_ore')],
    mobs=[get_mob('small_emerald_slime'),
          get_mob('medium_emerald_slime'),
          get_mob('large_emerald_slime')],
)
DIAMOND_RESERVE = Region(
    'diamond_reserve', -35, 15,
    resources=[get_resource('stone'), get_resource('diamond_ore')],
    mobs=[get_mob('diamond_zombie'),
          get_mob('diamond_skeleton')],
)
OBSIDIAN_SANCTUARY = Region(
    'obsidian_sanctuary', -10, 70,
    resources=[get_resource('stone'), get_resource('diamond_ore'),
               get_resource('diamond_block'), get_resource('obsidian')],
    mobs=[get_mob('enchanted_diamond_zombie'),
          get_mob('enchanted_diamond_skeleton')],
)
LIFT = Region(
    'lift', 50, 0,
    npcs=[
        Npc('life_operator',
            init_dialog=[
                'Hey Feller!',
                'I control this lift here behind me.',
                ("Once you've explored an area"
                 " I can give you a safe ride back there."),
                ("Be careful not to fall down the shaft though,"
                 " it's a long fall!"),
                'Good luck on your adventures.',
            ])
    ]
)

DEEP_JOINTS = [
    DEEP_ENTRENCE, DIAMOND_RESERVE, GUNPOWDER_MINES, LAPIS_QUARRY, LIFT,
    OBSIDIAN_SANCTUARY, PIGMANS_DEN, SLIMEHILL,
]
DEEP_CONNS = [
    (DIAMOND_RESERVE, LIFT),
    (DIAMOND_RESERVE, OBSIDIAN_SANCTUARY),
    (DIAMOND_RESERVE, SLIMEHILL),
    (DEEP_ENTRENCE, GUNPOWDER_MINES),
    (GUNPOWDER_MINES, LAPIS_QUARRY),
    (GUNPOWDER_MINES, LIFT),
    (LAPIS_QUARRY, PIGMANS_DEN),
    (LAPIS_QUARRY, LIFT),
    (LIFT, OBSIDIAN_SANCTUARY),
    (LIFT, PIGMANS_DEN),
    (LIFT, SLIMEHILL),
    (PIGMANS_DEN, SLIMEHILL),
]

DEEP_DISTS = {}

for conn in DEEP_CONNS:
    add_dist(*conn, DEEP_DISTS)

DEEP = Island(
    'deep', 'deep_entrence', DEEP_JOINTS, DEEP_CONNS, DEEP_DISTS,
    skill_req=('mining', 5),
)
