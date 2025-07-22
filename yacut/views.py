from flask import flash, redirect, render_template

from . import app, db
from .cloud import upload_files_and_get_download_links
from .forms import FileForm, MainForm
from .models import URLMap


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = MainForm()
    if form.validate_on_submit():
        try:
            url_map = URLMap.get_url_map(
                create=True,
                original=form.original_link.data,
                short=form.custom_id.data,
            )
        except ValueError as error:
            flash(error)
        else:
            return render_template(
                'pages/index.html', form=form, short_links=url_map.short,
            )
    return render_template('pages/index.html', form=form)


@app.route('/files', methods=['GET', 'POST'])
async def add_files_view():
    form = FileForm()
    if form.validate_on_submit():
        form_data = form.files.data
        download_links = await upload_files_and_get_download_links(form_data)
        short_links_to_files = []
        for index, download_link in enumerate(download_links):
            url_map = URLMap.get_url_map(
                create=True, commit=False, original=download_link,
            )
            short_links_to_files.append(
                (form_data[index].filename, url_map.short)
            )
        db.session.commit()
        return render_template(
            'pages/files.html', form=form, short_links=short_links_to_files,
        )
    return render_template('pages/files.html', form=form)


@app.route('/<string:link>')
def redirect_view(link):
    url_map = URLMap.query.filter_by(short=link).first_or_404()
    return redirect(url_map.original)
