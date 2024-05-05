from abc import ABC
from typing import TypeVar


class NotifiableObject(ABC):
    pass


NotifiableObjectType = TypeVar("NotifiableObjectType", bound=NotifiableObject)
