from ..constant.util import Number
from ..object.collection import COLLECTIONS
from ..object.object import *

from .wrapper import profile_wrapper


__all__ = ['Profile']


@profile_wrapper
class Profile:
    name: str
    last_update: int = 0

    # starter | gold | deluxe | super_deluxe | premier | luxurious | palatial
    bank_level: str = 'starter'
    experience: Number = 0
    balance: Number = 0
    purse: Number = 0
    mithril_powder: Number = 0

    island: str = 'hub'
    zone: str = 'village'
    visited_zones: list[str] = []

    experience_skill_alchemy: Number = 0
    experience_skill_carpentry: Number = 0
    experience_skill_catacombs: Number = 0
    experience_skill_combat: Number = 0
    experience_skill_enchanting: Number = 0
    experience_skill_farming: Number = 0
    experience_skill_fishing: Number = 0
    experience_skill_foraging: Number = 0
    experience_skill_mining: Number = 0
    experience_skill_taming: Number = 0
    collection: dict[str, int] = {
        collection.name: 0 for collection in COLLECTIONS
    }

    reaper_peppers: int = 0

    crafted_minions: list[str] = []
    fast_travel: list[str] = [('hub', None)]

    play_time: int = 0
    stats: dict[str, int] = {
        'deaths': 0, 'kills': 0, 'ore_mined': 0, 'sea_creature_killed': 0,
    }

    armor: list[Armor] = [Empty() for _ in range(4)]
    pets: list[Pet] = []
    ender_chest: list[Item] = []
    inventory: list[Item] = [Empty() for _ in range(80)]
    quiver: list[Item] = []
    stash: list[Item] = []
    accessory_bag: list[Item] = []
    minion_bag: list[Item] = []
    wardrobe: list[Item] = []
    wardrobe_slot: int | None = None

    crafted_minions: list[str] = []
    placed_minions: list[str] = [Empty() for _ in range(5)]

    npc_talked: list[str] = []
