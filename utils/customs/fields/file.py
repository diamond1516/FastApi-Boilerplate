from typing import Optional

from sqlalchemy import String
from sqlalchemy.types import TypeDecorator
from starlette.datastructures import UploadFile

from utils.customs.formats.file import FileObject
from ..storages import LocalStorageManager


class FileField(TypeDecorator):
    impl = String
    cache_ok = True

    def __init__(
            self,
            upload_to='',
            storage=LocalStorageManager,
            *args,
            **kwargs
    ):
        """
        :param upload_to:  folder name
        :param storage: storage class
        :param args: extra arguments
        :param kwargs: extra keyword arguments
        """
        self.storage = storage
        self.upload_folder = upload_to
        super().__init__(*args, **kwargs)

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        if isinstance(value, (UploadFile, FileObject)):
            file_path = self.storage.save(value, self.upload_folder)
            return file_path
        return str(value)

    def process_result_value(self, value, dialect) -> Optional[FileObject]:
        return FileObject(path=value, storage=self.storage) if value else None