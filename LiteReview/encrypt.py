import hashlib

from django.conf import settings


def md5(data):
    data_md5 = hashlib.md5(settings.SECRET_KEY.encode('utf-8'))
    data_md5.update(data.encode('utf-8'))
    return data_md5.hexdigest()
