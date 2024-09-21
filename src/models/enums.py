from __future__ import annotations
from enum import Enum, auto

from src.common.config import ConfigurationManager


class Action(str, Enum):
    ALLOW = 'allow'
    BLOCK = 'block'


class AttackType(Enum):
    BENIGN = auto()
    BRUTEFORCE = auto()
    WEB = auto()
    DOS = auto()
    DDOS = auto()
    BOTNET = auto()
    INFILTERATION = auto()

    @staticmethod
    def get_from_mapping(value: int) -> AttackType:
        if value == 1:
            return AttackType.BRUTEFORCE
        elif value == 2:
            return AttackType.WEB
        elif value == 3:
            return AttackType.DOS
        elif value == 4:
            return AttackType.DDOS
        elif value == 5:
            return AttackType.BOTNET
        elif value == 6:
            return AttackType.INFILTERATION
        else:
            return AttackType.BENIGN
        