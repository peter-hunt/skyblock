from typing import Dict, List, Optional

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
    visited_zones: List[str] = []

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
    collection: Dict[str, int] = {
        collection.name: 0 for collection in COLLECTIONS
    }

    crafted_minions: List[str] = []
    fast_travel: List[str] = [('hub', None)]

    play_time: int = 0
    stats: Dict[str, int] = {
        'deaths': 0, 'kills': 0, 'ore_mined': 0, 'sea_creature_killed': 0,
    }

    armor: List[Armor] = [Empty() for _ in range(4)]
    pets: List[Pet] = []
    ender_chest: List[Item] = []
    inventory: List[Item] = [Empty() for _ in range(80)]
    quiver: List[Item] = []
    stash: List[Item] = []
    accessory_bag: List[Item] = []
    minion_bag: List[Item] = []
    wardrobe: List[Item] = []
    wardrobe_slot: Optional[int] = None

    crafted_minions: List[str] = []
    placed_minions: List[str] = [Empty() for _ in range(5)]

    npc_talked: List[str] = []
