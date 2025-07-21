from random import choice

from .constants import SHORT_LINK_LENGTH, VALID_SYMBOLS_IN_SHORT_LINK
from .models import URLMap


def get_unique_short_id():
    while True:
        short_link = ''.join(
            [
                choice(VALID_SYMBOLS_IN_SHORT_LINK)
                for _ in range(SHORT_LINK_LENGTH)
            ]
        )
        if URLMap.query.filter_by(short=short_link).first() is None:
            return short_link
