from typing import Type

from src.common.persistence import PersistableObject


class NotLoadedException(Exception):
    pass


class UnexpectedPersistableObjectTypeException(Exception):

    def __init__(self, *, unexpected_type: Type[PersistableObject] | str, expected_type: Type[PersistableObject] | str):
        self._unexpected_type = unexpected_type if isinstance(unexpected_type, str) else unexpected_type.__name__
        self._expected_type = expected_type if isinstance(expected_type, str) else expected_type.__name__
        super().__init__(self.get_msg())

    def get_msg(self):
        return f"Tried to persist unexpected type {self._unexpected_type}. Expected type: {self._expected_type}"
