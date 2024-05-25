from abc import ABC, abstractmethod

from sqlmodel import Session

from src.common.config import AuthConfig
from src.models.user import User


class TokenAuthService(ABC):

    def __init__(self, session: Session, config: AuthConfig.TokenConfig):
        self._s = session
        self._config = config

    @abstractmethod
    def generate_token(self, user: User) -> str:
        pass

    @abstractmethod
    def authenticate_token(self, token: str) -> User | None:
        pass
