__all__ = [
    'CLN', 'BOLD',
    'BLACK', 'DARK_BLUE', 'DARK_GREEN', 'DARK_AQUA', 'DARK_RED', 'DARK_PURPLE',
    'GOLD', 'GRAY', 'DARK_GRAY', 'BLUE', 'GREEN', 'AQUA', 'RED', 'LIGHT_PURPLE',
    'YELLOW', 'WHITE',
    'RARITY_COLORS',
]

CLN = '\x1b[0m'
BOLD = '\x1b[1m'

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

RARITY_COLORS = {
    'common': f'{BOLD}{WHITE}',
    'uncommon': f'{BOLD}{GREEN}',
    'rare': f'{BOLD}{BLUE}',
    'epic': f'{BOLD}{DARK_PURPLE}',
    'legendary': f'{BOLD}{GOLD}',
    'mythic': f'{BOLD}{LIGHT_PURPLE}',
    'supreme': f'{BOLD}{DARK_RED}',
    'special': f'{BOLD}{RED}',
    'very_special': f'{BOLD}{RED}',

    'rngesus': f'{BOLD}{LIGHT_PURPLE}',
}
