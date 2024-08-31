from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import TypeVar

from src.common.utils import convert_str_camel_to_hyphen


class PersistableObject(ABC):

    @abstractmethod
    def _dump(self) -> bytes:
        ...

    @abstractmethod
    def _load(self, serialized_state: bytes):
        ...

    def save_to_file(self, filepath: Path):
        serialized_data = self._dump()
        if serialized_data is None:
            return
        with open(filepath, 'wb') as file:
            file.write(serialized_data)

    @classmethod
    def load_from_file(cls, filepath: Path) -> PersistableObject | None:
        if not filepath.exists():
            raise FileNotFoundError()
        with open(filepath, 'rb') as file:
            serialized_data = file.read()
        new_object = cls()
        new_object._load(serialized_data)
        return new_object

    @classmethod
    def generate_hyphen_separated_name(cls):
        return convert_str_camel_to_hyphen(cls.__name__)


PersistableObjectType = TypeVar("PersistableObjectType", bound=PersistableObject)
