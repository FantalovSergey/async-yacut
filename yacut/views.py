from flask import flash, redirect, render_template

from . import app, db
from .cloud import upload_files
from .forms import FileForm, MainForm
from .models import URLMap
from .utils import get_unique_short_id


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = MainForm()
    if form.validate_on_submit():
        short_link = form.custom_id.data or get_unique_short_id()
        if (
            not form.custom_id.data
            or short_link != 'files'
            and URLMap.query.filter_by(short=short_link).first() is None
        ):
            url_map = URLMap(
                original=form.original_link.data, short=short_link,
            )
            db.session.add(url_map)
            db.session.commit()
            return render_template(
                'pages/index.html', form=form, short_links=short_link,
            )
        flash('Предложенный вариант короткой ссылки уже существует.')
    return render_template('pages/index.html', form=form)


@app.route('/files', methods=['GET', 'POST'])
async def add_files_view():
    form = FileForm()
    if form.validate_on_submit():
        form_data = form.files.data
        urls = await upload_files(form_data)
        links_to_files = []
        url_map = []
        for index, (cloud_link, short_link) in enumerate(urls):
            links_to_files.append((form_data[index].filename, short_link))
            url_map.append(URLMap(original=cloud_link, short=short_link))
        db.session.add_all(url_map)
        db.session.commit()
        return render_template(
            'pages/files.html', form=form, short_links=links_to_files,
        )
    return render_template('pages/files.html', form=form)


@app.route('/<string:link>')
def redirect_view(link):
    url_map = URLMap.query.filter_by(short=link).first_or_404()
    return redirect(url_map.original)
