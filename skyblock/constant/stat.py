"""
Names of stats of a player.
"""

__all__ = ['ALL_STAT', 'HIDDEN_STATS', 'PERC_STATS']

# names of all stats
ALL_STAT = [
    'health',
    'defense',
    'true_defense',
    'strength',
    'speed',
    'crit_chance',
    'crit_damage',
    'intelligence',
    'mining_speed',
    'attack_speed',
    'sea_creature_chance',
    'magic_find',
    'pet_luck',
    'ability_damage',
    'ferocity',
    'mining_fortune',
    'farming_fortune',
    'foraging_fortune']

# stats not shown if are zero
HIDDEN_STATS = [
    'true_defense',
    'attack_speed',
    'ferocity']

# stats shown with percentage sign
PERC_STATS = [
    'crit_chance',
    'crit_damage',
    'attack_speed',
    'sea_creature_chance',
    'ability_damage']
