__all__ = [
    'CLN', 'BOLD', 'ITALIC',
    'BLACK', 'DARK_BLUE', 'DARK_GREEN', 'DARK_AQUA', 'DARK_RED', 'DARK_PURPLE',
    'GOLD', 'GRAY', 'DARK_GRAY', 'BLUE', 'GREEN', 'AQUA', 'RED', 'LIGHT_PURPLE',
    'YELLOW', 'WHITE',
    'COLOR_CODE', 'RARITY_COLORS', 'STAT_COLORS', 'CRIT_COLORS', 'DYE_COLORS',
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

    'extraodinary': f'{BOLD}{DARK_PURPLE}',
    'pray_rngesus': f'{BOLD}{LIGHT_PURPLE}',
    'rngesus_incarnate': f'{BOLD}{RED}',

    'good_catch': f'{BOLD}{GREEN}',
    'great_catch': f'{BOLD}{DARK_PURPLE}',
    'outstanding_catch': f'{BOLD}{LIGHT_PURPLE}',
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
    'pristine': f'{DARK_PURPLE}✧',
}

CRIT_COLORS = WHITE, YELLOW, GOLD, RED, RED, WHITE

DYE_COLORS = {
    'aquamarine': f'\x1b[0;38;2;127;255;212m',
    'bingo_blue': f'\x1b[0;38;2;0;47;167m',
    'brick_red': f'\x1b[0;38;2;203;65;84m',
    'bone': f'\x1b[0;38;2;227;218;201m',
    'byzantium': f'\x1b[0;38;2;112;41;99m',
    'carmine': f'\x1b[0;38;2;150;0;24m',
    'celadon': f'\x1b[0;38;2;172;225;175m',
    'celeste': f'\x1b[0;38;2;178;255;255m',
    'cyclamen': f'\x1b[0;38;2;245;111;161m',
    'dark_purple': f'\x1b[0;38;2;48;25;52m',
    'emerald': f'\x1b[0;38;2;80;200;120m',
    'flame': f'\x1b[0;38;2;226;88;34m',
    'iceberg': f'\x1b[0;38;2;113;166;210m',
    'livid': f'\x1b[0;38;2;102;153;204m',
    'mango': f'\x1b[0;38;2;253;190;2m',
    'midnight': f'\x1b[0;38;2;112;38;112m',
    'nadeshiko': f'\x1b[0;38;2;246;173;198m',
    'nyanza': f'\x1b[0;38;2;233;255;219m',
    'necron': f'\x1b[0;38;2;231;65;60m',
    'pure_black': f'\x1b[0;38;2;0;0;0m',
    'pure_blue': f'\x1b[0;38;2;0;0;255m',
    'pure_white': f'\x1b[0;38;2;255;255;255m',
    'pure_yellow': f'\x1b[0;38;2;255;255;0m',
    'wild_strawberry': f'\x1b[0;38;2;255;67;164m',
}
