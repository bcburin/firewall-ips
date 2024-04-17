from enum import Enum, auto


class Action(Enum):
    ALLOW = auto()
    BLOCK = auto()
    DROP = auto()