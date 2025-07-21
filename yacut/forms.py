from flask_wtf import FlaskForm
from flask_wtf.file import MultipleFileField
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, Regexp

from .constants import USER_SHORT_LINK_MAX_LENGTH, USER_SHORT_LINK_MIN_LENGTH


class MainForm(FlaskForm):
    original_link = URLField(
        'Оригинальная длинная ссылка',
        validators=[DataRequired(message='Обязательное поле')],
    )
    custom_id = StringField(
        'Короткая ссылка (опционально)',
        validators=[
            Length(USER_SHORT_LINK_MIN_LENGTH, USER_SHORT_LINK_MAX_LENGTH),
            Regexp(
                r'^[a-zA-Z0-9]+$',
                message=(
                    'Недопустимые символы. Разрешено использовать цифры '
                    'и латинские буквы в нижнем и верхнем регистрах.'
                ),
            ),
            Optional(),
        ],
    )
    submit = SubmitField('Создать')


class FileForm(FlaskForm):
    files = MultipleFileField(
        validators=[DataRequired(message='Обязательное поле')])
    submit = SubmitField('Загрузить')
