import logging
import re
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from threading import Lock
from typing import Type, TypeVar, Generic

from src.common.config import CompressionToolOption, PersistenceConfig
from src.common.utils import convert_str_camel_to_hyphen, Singleton


class PersistableObject(ABC):

    def __init__(self):
        self._lock = Lock()

    @abstractmethod
    def _dump(self) -> bytes:
        ...

    @abstractmethod
    def _load(self, serialized_state: bytes):
        ...

    def dump(self) -> bytes | None:
        with self._lock:
            try:
                serialized_data = self._dump()
                return serialized_data
            except Exception as e:
                logging.error(f"[{self.__class__.__name__}] couldn't serialize object: {e}")
                return None

    def load(self, serialized_state: bytes):
        with self._lock:
            try:
                self._load(serialized_state)
            except Exception as e:
                logging.error(f"[{self.__class__.__name__}] couldn't deserialize into object: {e}")

    def save_to_file(self, filepath: Path):
        serialized_data = self.dump()
        if serialized_data is not None:
            try:
                with open(filepath, 'wb') as file:
                    file.write(serialized_data)
                logging.info(f"[{self.__class__.__name__}] serialized object successfully saved to {filepath}")
            except Exception as e:
                logging.error(f"[{self.__class__.__name__}] error saving object to {filepath}: {e}")

    @classmethod
    def load_from_file(cls, filepath: Path):
        if not filepath.exists():
            logging.error(f"[{cls.__name__}] file not found for deserialization of object: {filepath}")
            return None
        try:
            with open(filepath, 'rb') as file:
                serialized_data = file.read()
            new_object = cls()
            new_object.load(serialized_data)
            logging.info(f"[{cls.__name__}] object loaded successfully from: {filepath}")
            return new_object
        except Exception as e:
            logging.error(f"[{cls.__name__}] error loading from {filepath}: {e}")
            return None

    @classmethod
    def generate_hyphen_separated_name(cls):
        return convert_str_camel_to_hyphen(cls.__name__)


PersistableObjectType = TypeVar("PersistableObjectType", bound=PersistableObject)


class PersistableObjectLifeCycleManager(Generic[PersistableObjectType], metaclass=Singleton):
    _dt_format = "%Y-%m-%d_%H-%M-%S"

    def __init__(self,
                 persistable_object_cls: Type[PersistableObject] = None,
                 persistence_config: PersistenceConfig = None):
        self._obj_lock = Lock()
        self._persisted_files_lock = Lock()
        self._obj = None
        self._cls = persistable_object_cls
        self._config = persistence_config

    def object_is_loaded(self) -> bool:
        with self._obj_lock:
            return self._obj is not None

    def has_persisted_objects(self) -> bool:
        return len(self.list_sorted_persisted_filepaths()) != 0

    def get_object(self) -> PersistableObjectType:
        with self._obj_lock:
            return self._obj

    @staticmethod
    def _get_possible_file_extensions():
        possible_extensions = ['bytes']
        possible_extensions.extend(['bytes.' + co.value for co in CompressionToolOption])
        return possible_extensions

    def _extract_datetime_from_filename(self, filename: str) -> datetime | None:
        obj_cls_name = self._cls.generate_hyphen_separated_name()
        pattern = (r'^(\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2})_' + obj_cls_name +
                   r'\.(' + "|".join(self._get_possible_file_extensions()) + r')$')
        match = re.match(pattern, filename)
        if match:
            datetime_str = match.group(1)
            try:
                datetime_obj = datetime.strptime(datetime_str, self._dt_format)
                return datetime_obj
            except ValueError:
                logging.error(f"[{self._cls.__name__}] invalid datetime format in filename: {filename}")
                return None
        else:
            logging.warning(f"[{self._cls.__name__}] file that doesn't match format {self._dt_format}_{obj_cls_name} "
                            f"was found: {filename}")
        return None

    def _generate_filename_from_datetime(self, dt: datetime) -> str:
        dt_str = dt.strftime(self.__class__._dt_format)
        return f"{dt_str}_{self._cls.generate_hyphen_separated_name()}.bytes"

    def _list_sorted_persisted_filepaths_unsafe(self) -> list[Path]:
        dt_filenames = []
        for path in self._config.resolved_directory.iterdir():
            if not path.is_file():
                continue
            dt_file = self._extract_datetime_from_filename(filename=path.name)
            if dt_file is None:
                continue
            dt_filenames.append((dt_file, path))
        dt_filenames.sort(key=lambda t: t[0])
        return [p for dt, p in dt_filenames]

    def list_sorted_persisted_filepaths(self) -> list[Path]:
        with self._persisted_files_lock:
            return self._list_sorted_persisted_filepaths_unsafe()

    def _delete_oldest_files_if_max_is_reached(self):
        sorted_filepaths = self.list_sorted_persisted_filepaths()
        num_files = len(sorted_filepaths)
        max_files = self._config.max_saved_models
        if num_files < max_files:
            return
        num_files_to_delete = num_files - max_files + 1
        logging.info(f'[{self._cls.__name__}] initiating old file purge.')
        with self._persisted_files_lock:
            for filepath in sorted_filepaths[:num_files_to_delete]:
                logging.info(f'[{self._cls.__name__}] deleting file: {filepath}')
                filepath.unlink()

    def _compress_files_and_delete_unsafe(self):
        compression_tool = CompressionToolOption.get_tool_implementation(self._config.compression.tool)
        sorted_filepaths = self._list_sorted_persisted_filepaths_unsafe()
        if not self._config.compression.compress_latest_model:
            sorted_filepaths = sorted_filepaths[:-1]
        for filepath in sorted_filepaths:
            if not str(filepath).endswith('bytes'):
                continue
            compression_tool.compress(filepath)
            filepath.unlink()

    def compress_files_and_delete(self):
        with self._persisted_files_lock:
            self._compress_files_and_delete_unsafe()

    def persist_current_object(self):
        if not self._config.enable:
            return
        self._delete_oldest_files_if_max_is_reached()
        filename = self._generate_filename_from_datetime(dt=datetime.now())
        self._obj.save_to_file(filepath=self._config.resolved_directory / filename)
        if self._config.compression.enable:
            self.compress_files_and_delete()

    def _uncompress_file_if_compressed_and_get_filepath(self, filepath: Path) -> Path | None:
        if not any(str(filepath).endswith(ext) for ext in self._get_possible_file_extensions()):
            logging.error(f'[{self._cls.__name__}] file with unidentified extension: {filepath}')
            return None
        if str(filepath).endswith('bytes'):
            return filepath
        file_extension = str(filepath).split('.')[-1]
        compression_tool = CompressionToolOption.get_tool_implementation(file_extension)
        extracted_path = Path('.'.join(str(filepath).split('.')[:-1]))
        with self._persisted_files_lock:
            compression_tool.decompress(compressed_filepath=filepath, output_filepath=extracted_path)
            filepath.unlink()
        return extracted_path

    def load_object(self, obj: PersistableObject):
        if not isinstance(obj, self._cls):
            logging.error(f'[{self._cls.__name__}] tried to load object of invalid type: {obj.__class__.__name__}')
            return
        with self._obj_lock:
            self._obj = obj

    def load_object_from_file(self, filepath: Path):
        filepath = self._uncompress_file_if_compressed_and_get_filepath(filepath=filepath)
        new_obj = self._cls.load_from_file(filepath) if filepath is not None else None
        if new_obj is None:
            logging.error(f'[{self.__class__.__name__}] unable to load latest file: {filepath}')
            return
        self.load_object(obj=new_obj)
        logging.info(f'[{self.__class__.__name__}] file loaded successfully: {filepath}')

    def load_object_from_latest_file(self):
        sorted_filepaths = self.list_sorted_persisted_filepaths()
        latest_file_path = sorted_filepaths[-1]
        logging.info(f'[{self._cls.__name__}] started to load latest file: {latest_file_path}')
        self.load_object_from_file(filepath=latest_file_path)
