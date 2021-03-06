__all__ = [
    'CLN', 'BOLD', 'ITALIC',
    'BLACK', 'DARK_BLUE', 'DARK_GREEN', 'DARK_AQUA', 'DARK_RED', 'DARK_PURPLE',
    'GOLD', 'GRAY', 'DARK_GRAY', 'BLUE', 'GREEN', 'AQUA', 'RED', 'LIGHT_PURPLE',
    'YELLOW', 'WHITE',
    'COLOR_CODE', 'RARITY_COLORS', 'STAT_COLORS', 'CRIT_COLORS',
]

CLN = '\x1b[0m'
BOLD = '\x1b[1m'
ITALIC = '\x1b[3m'

BLACK = '\x1b[0;38;2;0;0;0m'
DARK_BLUE = '\x1b[0;38;2;0;0;170m'
DARK_GREEN = '\x1b[0;38;2;0;170;0m'
DARK_AQUA = '\x1b[0;38;2;0;170;170m'
DARK_RED = '\x1b[0;38;2;170;0;0m'
DARK_PURPLE = '\x1b[0;38;2;170;0;170m'
GOLD = '\x1b[0;38;2;255;170;0m'
GRAY = '\x1b[0;38;2;170;170;170m'
DARK_GRAY = '\x1b[0;38;2;85;85;85m'
BLUE = '\x1b[0;38;2;85;85;255m'
GREEN = '\x1b[0;38;2;85;255;85m'
AQUA = '\x1b[0;38;2;85;255;255m'
RED = '\x1b[0;38;2;255;85;85m'
LIGHT_PURPLE = '\x1b[0;38;2;255;85;255m'
YELLOW = '\x1b[0;38;2;255;255;85m'
WHITE = '\x1b[0;38;2;255;255;255m'

COLOR_CODE = {}
for color in ('bold', 'italic', 'black', 'dark_blue', 'dark_green', 'dark_aqua',
              'dark_red', 'dark_purple', 'gold', 'gray', 'dark_gray', 'blue',
              'green', 'aqua', 'red', 'light_purple', 'yellow', 'white'):
    COLOR_CODE[color] = globals()[color.upper()]

RARITY_COLORS = {
    'common': f'{BOLD}{WHITE}',
    'uncommon': f'{BOLD}{GREEN}',
    'rare': f'{BOLD}{BLUE}',
    'epic': f'{BOLD}{DARK_PURPLE}',
    'legendary': f'{BOLD}{GOLD}',
    'mythic': f'{BOLD}{LIGHT_PURPLE}',
    'divine': f'{BOLD}{AQUA}',
    'special': f'{BOLD}{RED}',
    'very_special': f'{BOLD}{RED}',

    'rngesus': f'{BOLD}{LIGHT_PURPLE}',
    'pray_rngesus': f'{BOLD}{LIGHT_PURPLE}',

    'good_catch': f'{BOLD}{GREEN}',
    'great_catch': f'{BOLD}{LIGHT_PURPLE}',
}

STAT_COLORS = {
    'health': f'{RED}❤',
    'damage': f'{RED}❁',
    'defense': f'{GREEN}❈',
    'true_defense': f'{WHITE}❂',
    'strength': f'{RED}❁',
    'speed': f'{WHITE}✦',
    'crit_chance': f'{BLUE}☣',
    'crit_damage': f'{BLUE}☠',
    'intelligence': f'{AQUA}✎',
    'mining_speed': f'{GOLD}⸕',
    'attack_speed': f'{YELLOW}⚔',
    'sea_creature_chance': f'{DARK_AQUA}α',
    'magic_find': f'{AQUA}✯',
    'pet_luck': f'{LIGHT_PURPLE}♣',
    'ability_damage': f'{RED}๑',
    'ferocity': f'{RED}⫽',
    'mining_fortune': f'{GOLD}☘',
    'farming_fortune': f'{GOLD}☘',
    'foraging_fortune': f'{GOLD}☘',
}

CRIT_COLORS = WHITE, YELLOW, GOLD, RED, RED, WHITE
