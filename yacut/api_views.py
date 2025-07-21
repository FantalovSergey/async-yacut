import re

from flask import jsonify, request, url_for

from . import app, db
from .constants import USER_SHORT_LINK_MAX_LENGTH
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .utils import get_unique_short_id


@app.route('/api/id/', methods=['POST'])
def create_link():
    if not request.get_data():
        raise InvalidAPIUsage('Отсутствует тело запроса')
    data = request.get_json()
    try:
        url = data['url']
    except KeyError:
        raise InvalidAPIUsage('"url" является обязательным полем!')
    short_link = data.get('custom_id')
    if short_link:
        max_length = USER_SHORT_LINK_MAX_LENGTH
        invalid_symbols = re.sub(r'^[a-zA-Z0-9]+$', '', short_link)
        if invalid_symbols or len(short_link) > max_length:
            raise InvalidAPIUsage(
                'Указано недопустимое имя для короткой ссылки')
        if (
            short_link == 'files'
            or URLMap.query.filter_by(short=short_link).first() is not None
        ):
            raise InvalidAPIUsage(
                'Предложенный вариант короткой ссылки уже существует.')
    else:
        short_link = get_unique_short_id()
    url_map = URLMap(original=url, short=short_link)
    db.session.add(url_map)
    db.session.commit()
    short_link = url_for('redirect_view', link=short_link, _external=True)
    return jsonify({'url': url, 'short_link': short_link}), 201


@app.route('/api/id/<string:short_id>/')
def get_original_link(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first()
    if not url_map:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    return jsonify({'url': url_map.original}), 200
