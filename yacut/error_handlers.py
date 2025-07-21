from flask import jsonify, render_template

from . import app, db


class InvalidAPIUsage(Exception):
    def __init__(self, message, status_code=400):
        super().__init__()
        self.message = message
        self.status_code = status_code

    def to_dict(self):
        return {'message': self.message}


@app.errorhandler(InvalidAPIUsage)
def invalid_api_usage(error):
    return jsonify(error.to_dict()), error.status_code


@app.errorhandler(404)
def not_found(_):
    return render_template('error_pages/404.html'), 404


@app.errorhandler(500)
def internal_error(_):
    db.session.rollback()
    return render_template('error_pages/500.html'), 500