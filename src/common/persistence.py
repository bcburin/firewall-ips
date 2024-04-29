import logging
from abc import ABC, abstractmethod
from pathlib import Path
from threading import Lock
from typing import TypeVar

from src.common.utils import convert_str_camel_to_hyphen


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
