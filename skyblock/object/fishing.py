from .item import get_item
from .object import Item


__all__ = ['FISHING_TABLE']

FISHING_TABLE = [
    # item, amount, rarity, weight, fishing exp
    (Item('clay'), 1, 'normal', 0.04, 30),
    (Item('fish'), 1, 'normal', 0.28, 25),
    (Item('salmon'), 1, 'normal', 0.13, 35),
    (Item('pufferfish'), 1, 'normal', 0.07, 50),
    (Item('prismarine_shard'), 1, 'good_catch', 0.01, 160),
    (Item('prismarine_crystals'), 1, 'good_catch', 0.01, 160),
    (Item('clownfish'), 1, 'normal', 0.02, 100),
    (Item('golden_apple'), 1, 'good_catch', 0.005, 160),
    ((5_000, 10_000), 1, 'good_catch', 0.03, 160),
    (Item('grand_experience_bottle'), 1, 'great_catch', 0.005, 160),
    (Item('titanic_experience_bottle'), 1, 'great_catch', 0.001, 300),
    (get_item('fairys_fedora'), 1, 'great_catch', 0.01, 300),
    (get_item('fairys_polo'), 1, 'great_catch', 0.01, 300),
    (get_item('fairys_trousers'), 1, 'great_catch', 0.01, 300),
    (get_item('fairys_galoshes'), 1, 'great_catch', 0.01, 300),
    (Item('enchanted_clay'), 1, 'great_catch', 0.01, 300),
    (Item('enchanted_iron'), 1, 'great_catch', 0.01, 300),
    (Item('enchanted_gold'), 1, 'great_catch', 0.01, 300),
    (Item('enchanted_diamond'), 1, 'great_catch', 0.01, 300),
    (Item('enchanted_pufferfish'), 1, 'great_catch', 0.01, 300),
    ((10_000, 20_000), 1, 'great_catch', 0.01, 300),
    (get_item('guardian_pet', rarity='epic'), 1, 'great_catch', 0.01, 300),
    (get_item('guardian_pet', rarity='legendary'), 1, 'great_catch', 0.01, 300),
    (get_item('squid_pet', rarity='epic'), 1, 'great_catch', 0.02, 300),
    (get_item('squid_pet', rarity='legendary'), 1, 'great_catch', 0.02, 300),
    (Item('treasurite'), 1, 'good_catch', 0.01, 300),
]
