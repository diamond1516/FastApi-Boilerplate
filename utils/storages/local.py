import os
from typing import Union

from starlette.datastructures import UploadFile

from config import APP_SETTINGS
from .base import StorageManager


class LocalStorageManager(StorageManager):
    file_classes = (UploadFile,)
    file_host = APP_SETTINGS.SERVER_HOST

    @classmethod
    def save(cls, file: Union[file_classes], upload_folder):

        new_filename = cls._generate_new_filename(file.filename)
        folder_path = os.path.join(cls.MEDIA_DIR, upload_folder)
        file_path = os.path.join(str(folder_path), new_filename)
        os.makedirs(folder_path, exist_ok=True)

        if isinstance(file, cls.file_classes):
            with open(file_path, 'wb') as f:
                f.write(file.file.read())
            return upload_folder + new_filename
        raise ValueError("File type not supported")


    @classmethod
    def delete(cls, path):
        file_path = os.path.join(cls.MEDIA_DIR, path)
        if os.path.exists(file_path):
            os.remove(file_path)

