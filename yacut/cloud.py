import asyncio
import urllib

import aiohttp

from . import constants
from .utils import get_unique_short_id


async def upload_files(files) -> list[tuple]:
    """Возвращает список ссылок (длинную и короткую) на файлы."""
    short_links = []
    tasks = []
    async with aiohttp.ClientSession() as session:
        for file in files:
            while True:
                short_link = get_unique_short_id()
                if short_link not in short_links:
                    break
            short_links.append(short_link)
            tasks.append(
                asyncio.ensure_future(
                    upload_file(session, file, short_link)
                )
            )
        urls = await asyncio.gather(*tasks)
    return urls


async def upload_file(session, file, short_link):
    async with session.get(
        headers=constants.AUTH_HEADERS,
        params={
            'path': f'app:/{short_link}_{file.filename}',
            'fields': 'href',
        },
        url=constants.REQUEST_UPLOAD_URL,
    ) as response:
        response_upload_url = await response.json()
        upload_url = response_upload_url['href']
    async with session.put(data=file.stream._file, url=upload_url) as response:
        location = response.headers['Location']
        location = urllib.parse.unquote(location).replace('/disk', '')
    async with session.get(
        headers=constants.AUTH_HEADERS,
        params={
            'path': location,
            'fields': 'href',
        },
        url=constants.DOWNLOAD_LINK_URL,
    ) as response:
        response_file_url = await response.json()
    return response_file_url['href'], short_link