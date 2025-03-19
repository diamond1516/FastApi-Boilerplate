from abc import ABC, abstractmethod

from config import APP_SETTINGS


class StorageManager(ABC):
    MEDIA_URL: str = APP_SETTINGS.MEDIA_URL
    MEDIA_DIR = APP_SETTINGS.MEDIA_DIR

    file_host = ...

    @abstractmethod
    def save(self, file, upload_folder):
        raise NotImplementedError()

    @abstractmethod
    def delete(self, file_path, upload_folder):
        raise NotImplementedError()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if not cls.file_host:
            raise ValueError("Storage type must be defined")
