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
from src.common.exceptions.auth import AuthenticationServiceNotLoadedException, UnknownAuthenticationService
from src.common.utils import LoadableSingleton
from src.models.user import UserOutModel, User
from src.services.database import InjectedSession

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
            return User.get_by_username_or_email(self._s, identifier=username)
        except (JWTError, ValidationError):
            return None


class TokenAuthManager(LoadableSingleton):

    def __init__(self):
        self._config: AuthConfig | None = None
        self._service: Type[TokenAuthService] | None = None
        super().__init__()

    def _load(self):
        self._config = ConfigurationManager().get_auth_config()
        if self._config is None:
            return
        if self._config.login.method == "JWTAuthService":
            self._service = JWTAuthService
        else:
            raise UnknownAuthenticationService(self._config.login.method)

    def _loaded(self) -> bool:
        return self._config is not None and self._service is not None

    @property
    def _not_loaded_exception(self) -> Exception:
        return AuthenticationServiceNotLoadedException()

    def get_service(self, session: Session, config: AuthConfig.TokenConfig) -> TokenAuthService:
        with self.load_guard():
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
