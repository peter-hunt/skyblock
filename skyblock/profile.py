from dataclasses import dataclass, field
from json import dump, load
from os.path import join
from pathlib import Path
from time import time
from typing import Any, Dict, List, Optional

from .func import red


ItemTyping = Dict[str, Any]


def exist_dir(*names, warn=False):
    if not Path(join(Path.home(), 'skyblock', *names)).is_dir():
        path = join('~', 'skyblock', *names)
        if warn:
            print(f'Warning: folder {path} not found.')
        return False
    return True


def exist_file(*names, warn=False):
    if not Path(join(Path.home(), 'skyblock', *names)).is_file():
        path = join('~', 'skyblock', *names)
        if warn:
            print(f'Warning: file {path} not found.')
        return False
    return True


@dataclass
class Profile:
    name: str
    last_update: Optional[int] = None

    # starter | gold | deluxe | super_deluxe | premier
    bank_level: str = 'starter'
    balance: float = 0.0
    purse: float = 0.0

    skill_xp_alchemy: float = 0.0
    skill_xp_carpentry: float = 0.0
    skill_xp_combat: float = 0.0
    skill_xp_enchanting: float = 0.0
    skill_xp_farming: float = 0.0
    skill_xp_fishing: float = 0.0
    skill_xp_foraging: float = 0.0
    skill_xp_mining: float = 0.0
    skill_xp_runecrafting: float = 0.0
    skill_xp_taming: float = 0.0
    collection: Dict[str, int] = field(default_factory=dict)

    crafted_minions: List[str] = field(default_factory=list)

    armor: List[ItemTyping] = field(
        default_factory=lambda: [{} for _ in range(4)]
    )
    pets: List[ItemTyping] = field(default_factory=list)
    ender_chest: List[ItemTyping] = field(default_factory=list)
    inventory: List[ItemTyping] = field(
        default_factory=lambda: [{} for _ in range(36)]
    )
    potion_bag: List[ItemTyping] = field(default_factory=list)
    quiver: List[ItemTyping] = field(default_factory=list)
    talisman_bag: List[ItemTyping] = field(default_factory=list)
    wardrobe: List[ItemTyping] = field(default_factory=list)
    wardrobe_slot: Optional[int] = None

    @staticmethod
    def is_valid(name, warn=False):
        if not exist_dir(warn=warn):
            return False
        if not exist_dir('saves', warn=warn):
            return False
        if not exist_file('saves', f'{name}.json', warn=warn):
            return False

        return True

    @classmethod
    def load(cls, name):
        if not cls.is_valid(name, warn=True):
            print('Error: Profile not found.')
            return

        with open(join(Path.home(), 'skyblock',
                       'saves', f'{name}.json')) as file:
            data = load(file)

        return cls(
            name=name, last_update=data.get('last_update'),
            bank_level=data.get('bank_level', 'starter'),
            balance=data.get('balance', 0.0),
            purse=data.get('purse', 0.0),

            collection=data.get('collection', {}),
            skill_xp_alchemy=data.get('skill_xp_alchemy', 0.0),
            skill_xp_carpentry=data.get('skill_xp_carpentry', 0.0),
            skill_xp_combat=data.get('skill_xp_combat', 0.0),
            skill_xp_enchanting=data.get('skill_xp_enchanting', 0.0),
            skill_xp_farming=data.get('skill_xp_farming', 0.0),
            skill_xp_fishing=data.get('skill_xp_fishing', 0.0),
            skill_xp_foraging=data.get('skill_xp_foraging', 0.0),
            skill_xp_mining=data.get('skill_xp_mining', 0.0),
            skill_xp_runecrafting=data.get('skill_xp_runecrafting', 0.0),
            skill_xp_taming=data.get('skill_xp_taming', 0.0),

            crafted_minions=data.get('crafted_minions', []),

            armor=data.get('armor', []),
            pets=data.get('wardrobe', []),
            ender_chest=data.get('ender_chest', []),
            inventory=data.get('inventory', []),
            potion_bag=data.get('potion_bag', []),
            quiver=data.get('quiver', []),
            talisman_bag=data.get('talisman_bag', []),
            wardrobe=data.get('wardrobe', []),
            wardrobe_slot=data.get('wardrobe_slot', 0),
        )

    def dump(self):
        with open(join(Path.home(), 'skyblock',
                       'saves', f'{self.name}.json'), 'w') as file:
            dump({
                'last_update': self.last_update,
                'bank_level': self.bank_level,
                'balance': self.balance,
                'purse': self.purse,

                'collection': self.collection,
                'skill_xp_alchemy': self.skill_xp_alchemy,
                'skill_xp_carpentry': self.skill_xp_carpentry,
                'skill_xp_combat': self.skill_xp_combat,
                'skill_xp_enchanting': self.skill_xp_enchanting,
                'skill_xp_farming': self.skill_xp_farming,
                'skill_xp_fishing': self.skill_xp_fishing,
                'skill_xp_foraging': self.skill_xp_foraging,
                'skill_xp_mining': self.skill_xp_mining,
                'skill_xp_runecrafting': self.skill_xp_runecrafting,
                'skill_xp_taming': self.skill_xp_taming,

                'crafted_minions': self.crafted_minions,

                'armor': self.armor,
                'pets': self.pets,
                'ender_chest': self.ender_chest,
                'inventory': self.inventory,
                'potion_bag': self.potion_bag,
                'quiver': self.quiver,
                'talisman_bag': self.talisman_bag,
                'wardrobe': self.wardrobe,
                'wardrobe_slot': self.wardrobe_slot,
            }, file, indent=4, sort_keys=True)

    def update(self):
        now = time()
        last = now if self.last_update is None else self.last_update
        dt = now - last

        self.last_update = time()

    def mainloop(self):
        while True:
            self.update()
            words = input(':> ').split()
            if words[0] in {'exit', 'quit'}:
                if len(words) == 1:
                    self.dump()
                    break
                else:
                    red(f'Invalid usage of command {words[0]!r}.')
            else:
                red(f'Unknown command: {words[0]!r}')
