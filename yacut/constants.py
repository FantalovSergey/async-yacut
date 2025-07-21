from . import app

SHORT_LINK_LENGTH = 6
USER_SHORT_LINK_MIN_LENGTH = 1
USER_SHORT_LINK_MAX_LENGTH = 16
SHORT_LINK_MAX_LENGTH = 32
VALID_SYMBOLS_IN_SHORT_LINK = (
    'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890')

AUTH_HEADERS = {'Authorization': f'OAuth {app.config["DISK_TOKEN"]}'}
DISK_INFO_URL = 'https://cloud-api.yandex.net/v1/disk/'
REQUEST_UPLOAD_URL = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
DOWNLOAD_LINK_URL = 'https://cloud-api.yandex.net/v1/disk/resources/download'
