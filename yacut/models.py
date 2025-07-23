import re
from datetime import datetime
from random import choice

from . import db
from . import constants


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.Text, nullable=False)
    short = db.Column(
        db.String(constants.SHORT_LINK_MAX_LENGTH),
        unique=True,
        nullable=False,
    )
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now)

    @staticmethod
    def create_url_map(original, short=None, commit=True) -> 'URLMap':
        if short:
            if (
                re.sub(r'^[a-zA-Z0-9]+$', '', short)
                or len(short) > constants.USER_SHORT_LINK_MAX_LENGTH
            ):
                raise ValueError(
                    'Указано недопустимое имя для короткой ссылки')
            if (
                short == 'files'
                or URLMap.query.filter_by(short=short).first() is not None
            ):
                raise ValueError(
                    'Предложенный вариант короткой ссылки уже существует.')
        else:
            short = URLMap.get_unique_short_id()
        url_map = URLMap(original=original, short=short)
        db.session.add(url_map)
        if commit:
            db.session.commit()
        return url_map

    @staticmethod
    def get_unique_short_id():
        while True:
            short_id = ''.join(
                [
                    choice(constants.VALID_SYMBOLS_IN_SHORT_LINK)
                    for _ in range(constants.SHORT_LINK_LENGTH)
                ]
            )
            if URLMap.query.filter_by(short=short_id).first() is None:
                return short_id

    @staticmethod
    def get_url_map(short):
        url_map = URLMap.query.filter_by(short=short).first()
        if not url_map:
            raise ValueError('Указанный id не найден')
        return url_map
