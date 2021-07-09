from typing import Dict, List, Optional

from ..constant.util import Number
from ..object.collection import COLLECTIONS
from ..object.object import Item, Empty, Armor

from .wrapper import profile_wrapper


__all__ = ['Profile']


@profile_wrapper
class Profile:
    name: str
    last_update: int = 0

    bank_level: str = 'starter'
    balance: Number = 0.0
    purse: Number = 0.0

    experience: Number = 0

    island: str = 'hub'
    zone: str = 'village'
    visited_zones: List[str] = []

    experience_skill_alchemy: float = 0.0
    experience_skill_carpentry: float = 0.0
    experience_skill_catacombs: float = 0.0
    experience_skill_combat: float = 0.0
    experience_skill_enchanting: float = 0.0
    experience_skill_farming: float = 0.0
    experience_skill_fishing: float = 0.0
    experience_skill_foraging: float = 0.0
    experience_skill_mining: float = 0.0
    experience_skill_taming: float = 0.0
    collection: Dict[str, int] = {
        collection.name: 0
        for collection in COLLECTIONS
    }

    crafted_minions: List[str] = []
    fast_travel: List[str] = [('hub', None)]

    play_time: int = 0
    stats: Dict[str, int] = {
        'deaths': 0,
        'kills': 0,
    }

    armor: List[Armor] = [Empty() for _ in range(4)]
    pets: List[Item] = []
    ender_chest: List[Item] = []
    inventory: List[Item] = [Empty() for _ in range(36)]
    potion_bag: List[Item] = []
    quiver: List[Item] = []
    stash: List[Item] = []
    talisman_bag: List[Item] = []
    wardrobe: List[Item] = []
    wardrobe_slot: Optional[int] = None

    npc_talked: List[str] = []
