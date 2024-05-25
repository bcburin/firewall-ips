from datetime import timedelta, datetime
from typing import Annotated, Type

from jose import jwt, JWTError
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError
from sqlmodel import Session
from starlette.status import HTTP_401_UNAUTHORIZED

from src.common.auth import TokenAuthService
from src.common.config import InjectedTokenConfig, AuthConfig, ConfigurationManager
from src.common.exceptions.auth import AuthenticationServiceNotLoadedException
from src.common.utils import Singleton
from src.models.user import UserOutModel, User
from src.services.database import InjectedSession
from src.services.models import UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


class JWTAuthService(TokenAuthService):

    def generate_token(self, user: User) -> str:
        to_encode = {'sub': user.username}
        expire = datetime.utcnow() + timedelta(minutes=self._config.expiration_time_in_minutes)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self._config.key, algorithm=self._config.algorithm)
        return encoded_jwt

    def authenticate_token(self, token: str) -> User | None:
        try:
            payload = jwt.decode(token, self._config.key, algorithms=[self._config.algorithm])
            username: str = payload.get('sub')
            if username is None:
                return None
            return UserService(self._s).get_by_username_or_email(identifier=username)
        except (JWTError, ValidationError):
            return None


class TokenAuthManager(metaclass=Singleton):

    def __init__(self):
        self._service: Type[TokenAuthService] | None = None

    def load(self):
        config = ConfigurationManager().get_server_config().authentication
        self._service = JWTAuthService if config.login.method == "JWTAuthService" else None

    def get_service(self, session: Session, config: AuthConfig.TokenConfig) -> TokenAuthService:
        if self._service is None:
            raise AuthenticationServiceNotLoadedException()
        return self._service(session, config)

    def generate_token(self, user: User, session: Session, config: AuthConfig.TokenConfig):
        return self.get_service(session, config).generate_token(user)

    def authenticate_token(self, token: str, session: Session, config: AuthConfig.TokenConfig):
        return self.get_service(session, config).authenticate_token(token)


def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)], session: InjectedSession, config: InjectedTokenConfig):
    current_user = TokenAuthManager().authenticate_token(token, session, config)
    if current_user is None:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return current_user


InjectedCurrentUser = Annotated[UserOutModel, Depends(get_current_user)]