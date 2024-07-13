from __future__ import annotations

from datetime import datetime

import bcrypt
from sqlmodel import Session, SQLModel

from src.common.config import ConfigurationManager
from src.common.exceptions.auth import LoginTriesLimitExceeded, IncorrectCredentialsException
from src.models.base import BaseUpdateModel, BaseOutModel, BaseSQLModel


class UserBaseModel(BaseSQLModel):
    username: str
    email: str
    first_name: str
    last_name: str
    active: bool


class UserCreateModel(UserBaseModel):
    password: str
    active: bool = True


class UserUpdateModel(SQLModel, BaseUpdateModel):
    username: str | None = None
    email: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    password: str | None = None
    active: bool | None = None


class UserOutModel(UserBaseModel, BaseOutModel):
    last_login: datetime | None
    login_attempts: int = 0


class GetAllUsers(SQLModel):
    data: list[User]
    total: int


class User(UserOutModel, table=True):
    password_hash: str

    # noinspection PyTypeChecker
    @classmethod
    def create_from(cls, create_model: UserCreateModel) -> User:
        user: User = BaseSQLModel.create_from.__func__(cls, create_model)
        user.password_hash = cls.hash_password(create_model.password)
        return user

    # noinspection PyTypeChecker
    def update_from(self, update_model: UserUpdateModel) -> User:
        password = update_model.password
        if password is not None:
            self.password_hash = self.hash_password(password)
        return super().update_from(update_model)

    @staticmethod
    def hash_password(password: str) -> str:
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password.decode('utf-8')

    @staticmethod
    def check_password(password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

    # noinspection PyTypeChecker
    @staticmethod
    def get_by_username_or_email(session: Session, identifier: str):
        user = session.query(User).filter(User.email == identifier).first()
        if user is not None:
            return user
        return session.query(User).filter(User.username == identifier).first()

    @classmethod
    def authenticate(cls, session: Session, identifier: str, password: str) -> User:
        user = cls.get_by_username_or_email(session, identifier)
        if user is not None and not cls.check_password(password=password, hashed_password=user.password_hash):
            user.login_attempts += 1
            max_tries = ConfigurationManager().get_server_config().authentication.login.max_login_tries
            if user.login_attempts > max_tries:
                user.active = False
                user.update(session)
                raise LoginTriesLimitExceeded()
            user.update(session)
            raise IncorrectCredentialsException()
        if user is None:
            raise IncorrectCredentialsException()
        user.login_attempts = 0
        user.last_login = datetime.now()
        user.update(session)
        return user
