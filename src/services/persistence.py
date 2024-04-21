import logging
import pickle
import re
from datetime import datetime
from pathlib import Path
from threading import Lock
from typing import TypeVar, Generic, Type

from src.common.config import ServerConfig, CompressionToolOption
from src.common.utils import convert_str_camel_to_hyphen


class PersistableObject:
    __logging_name__ = 'entity'

    def __init__(self):
        self._lock = Lock()

    def serialize(self) -> bytes | None:
        """
        Serialize the object's state.
        """
        with self._lock:
            try:
                serialized_data = pickle.dumps(self.__dict__)
                return serialized_data
            except Exception as e:
                print(f"Couldn't serialize {self.__logging_name__}: {e}")
                return None

    def deserialize(self, serialized_state: bytes):
        """
        Deserialize and restore the object's state.
        """
        with self._lock:
            try:
                self.__dict__ = pickle.loads(serialized_state)
            except Exception as e:
                logging.error(f"Couldn't deserialize {self.__logging_name__}: {e}")

    def save_to_file(self, file_path: Path):
        """
        Save the serialized state to a file.
        """
        serialized_data = self.serialize()
        if serialized_data is not None:
            try:
                with open(file_path, 'wb') as file:
                    file.write(serialized_data)
                logging.info(f"Serialized {self.__logging_name__} successfully saved to {file_path}")
            except Exception as e:
                logging.error(f"Error saving {self.__logging_name__} to {file_path}: {e}")

    @classmethod
    def load_from_file(cls, file_path: Path):
        """
        Load serialized state from a file and create a new object instance.
        """
        if not file_path.exists():
            logging.error(f"File not found for deserialization of {cls.__logging_name__}: {file_path}")
            return None

        try:
            with open(file_path, 'rb') as file:
                serialized_data = file.read()
            new_object = cls()
            new_object.deserialize(serialized_data)
            logging.info(f"Object {cls.__logging_name__} loaded successfully from: {file_path}")
            return new_object
        except Exception as e:
            logging.error(f"Error loading {cls.__logging_name__} from {file_path}: {e}")
            return None

    @classmethod
    def get_hyphen_separated_name(cls):
        return convert_str_camel_to_hyphen(cls.__name__)


PersistableObjectType = TypeVar("PersistableObjectType", bound=PersistableObject)


class PersistableObjectLifeCycleManager(Generic[PersistableObjectType]):
    _dt_format = "%Y-%m-%d_%H-%M-%S"

    def __init__(
            self, obj: Type[PersistableObjectType], persistence_config: ServerConfig.AIModelConfig.PersistenceConfig):
        self._obj = obj
        self._config = persistence_config

    @classmethod
    def _get_datetime_from_filename(cls, filename: str) -> datetime | None:
        obj_cls_name = PersistableObjectType.get_hyphen_separated_name()
        possible_extensions = ['bytes']
        possible_extensions.extend([str(co) for co in CompressionToolOption])
        pattern = rf'^(\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2})_{obj_cls_name}\.{"|".join(possible_extensions)}$'
        match = re.match(pattern, filename)
        if match:
            datetime_str = match.group(1)
            try:
                datetime_obj = datetime.strptime(datetime_str, cls._dt_format)
                return datetime_obj
            except ValueError:
                logging.error(f"Invalid datetime format in filename: {filename}")
                return None
        logging.warning(f"File that doesn't match format {cls._dt_format}_{obj_cls_name} was found: {filename}")
        return None

    @classmethod
    def _get_filename_from_datetime(cls, dt: datetime) -> str:
        dt_str = dt.strftime(cls._dt_format)
        return f"{dt_str}_{PersistableObjectType.get_hyphen_separated_name()}.bytes"

    def _get_persisted_filepaths_sorted(self) -> list[Path]:
        dt_filenames = []
        for path in self._config.resolved_directory.iterdir():
            if not path.is_file():
                continue
            dt_file = self._get_datetime_from_filename(filename=path.name)
            if dt_file is None:
                continue
            dt_filenames.append((dt_file, path))
        dt_filenames.sort(key=lambda t: t[0])
        return [p for dt, p in dt_filenames]

    @staticmethod
    def _purge_old_files(sorted_filepaths: list[Path], n: int):
        for filepath in sorted_filepaths[:-n]:
            filepath.unlink()

    def persist(self):
        if not self._config.enable:
            return
        sorted_filepaths = self._get_persisted_filepaths_sorted()
        num_files = len(sorted_filepaths)
        max_files = self._config.max_saved_models
        if num_files >= max_files:
            num_files_to_delete = num_files - max_files + 1
            self._purge_old_files(sorted_filepaths=sorted_filepaths, n=num_files_to_delete)
        save_filename = self._get_filename_from_datetime(dt=datetime.now())
        save_path = self._config.resolved_directory / save_filename
        self._obj.save_to_file(file_path=save_path)
