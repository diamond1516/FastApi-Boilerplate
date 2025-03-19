import os
from dataclasses import dataclass
from typing import Any

from config import APP_SETTINGS
from utils.customs.formats import BaseFormat
from utils.storages.base import StorageManager


@dataclass(slots=True)
class FileObject(BaseFormat):
    path: Any
    MEDIA_URL = APP_SETTINGS.MEDIA_URL
    SERVER_HOST = APP_SETTINGS.SERVER_HOST
    storage: type[StorageManager]
    json_schema = {
        "type": "string", "format": "string",
        "description": "URL to the file.", 'example': 'https://drivers.uz/media/profiles/image.png'
    }

    __visit_name__ = "string"

    def __str__(self):
        return str(self.path)

    def __repr__(self):
        return str(self.path)

    @property
    def filename(self):
        return os.path.basename(self.path)

    @property
    def url(self):
        return f'{self.storage.file_host}{self.MEDIA_URL}{self.path}' if self.path else None

    @property
    def extension(self):
        return os.path.splitext(self.path)[1]

    @property
    def size(self):
        file_path = os.path.join(self.MEDIA_URL, self.path)
        assert os.path.exists(file_path), f'File {file_path} does not exist'
        return os.path.getsize(file_path)

    @property
    def file(self):
        file_path = os.path.join(self.MEDIA_URL, self.path)
        return open(file_path, 'rb')

    @property
    def python_type(self):
        return str

    @classmethod
    def validate(cls, v=None, *args, **kwargs):
        if v is None:
            return None
        if isinstance(v, FileObject):
            return v.url
        return f'{cls.MEDIA_URL}{str(v)}'
