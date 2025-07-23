from flask import jsonify, request, url_for

from . import app
from .error_handlers import InvalidAPIUsage
from .models import URLMap


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
    try:
        url_map = URLMap.create_url_map(original=url, short=short_link)
    except ValueError as error:
        raise InvalidAPIUsage(str(error))
    short_link = url_for('redirect_view', link=url_map.short, _external=True)
    return jsonify({'url': url, 'short_link': short_link}), 201


@app.route('/api/id/<string:short_id>/')
def get_original_link(short_id):
    try:
        url_map = URLMap.get_url_map(short_id)
    except ValueError as error:
        raise InvalidAPIUsage(str(error), 404)
    return jsonify({'url': url_map.original}), 200
