from ...function.io import red

from ..object import TravelScroll


__all__ = ['TRAVEL_SCROLLS', 'get_scroll']

TRAVEL_SCROLLS = [
    TravelScroll('hub', 'castle', rarity='epic'),
    TravelScroll('barn'),
    TravelScroll('desert'),
    TravelScroll('gold'),
    TravelScroll('deep'),
    TravelScroll('park'),
    TravelScroll('park', 'howl', rarity='epic'),
    TravelScroll('park', 'jungle', rarity='epic'),
    TravelScroll('spider'),
    TravelScroll('spider', 'nest', rarity='epic'),
    TravelScroll('nether'),
    TravelScroll('nether', 'magma', rarity='epic'),
    TravelScroll('end'),
    TravelScroll('end', 'drag', rarity='epic'),
    TravelScroll('mines'),
]


def get_scroll(name: str) -> TravelScroll:
    for scroll in TRAVEL_SCROLLS:
        scroll_name = scroll.island if scroll.region is None else scroll.region
        if name == scroll_name:
            return scroll
    red(f'Invalid travel scroll: {name!r}')
