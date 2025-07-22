import asyncio
import urllib
from time import time_ns

import aiohttp

from . import constants


async def upload_files_and_get_download_links(files):
    tasks = []
    async with aiohttp.ClientSession() as session:
        for file in files:
            filename_unique_part = time_ns() // 10**3
            tasks.append(
                asyncio.ensure_future(
                    upload_file_and_get_download_link(
                        session, file, filename_unique_part,
                    )
                )
            )
        urls = await asyncio.gather(*tasks)
    return urls


async def upload_file_and_get_download_link(
    session, file, filename_unique_part
):
    async with session.get(
        headers=constants.AUTH_HEADERS,
        params={
            'path': f'app:/{filename_unique_part}_{file.filename}',
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
    return response_file_url['href']