from enum import Enum


class Action(str, Enum):
    ALLOW = 'allow'
    BLOCK = 'block'
