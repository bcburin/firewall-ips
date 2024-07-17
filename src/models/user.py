from __future__ import annotations

from datetime import datetime

import bcrypt
from faker import Faker
from sqlmodel import Session, SQLModel

from src.common.config import ConfigurationManager
from src.common.exceptions.auth import LoginTriesLimitExceeded, IncorrectCredentialsException, UserInactiveException, \
    InvalidPasswordException
from src.models.base import BaseUpdateModel, BaseOutModel, BaseSQLModel, BaseModel


class UserBaseModel(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    active: bool


class UserCreateModel(UserBaseModel):
    password: str
    active: bool = True


class UserUpdateModel(BaseUpdateModel):
    username: str | None = None
    email: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    new_password: str | None = None
    old_password: str | None = None
    active: bool | None = None


class UserOutModel(UserBaseModel, BaseOutModel):
    last_login: datetime | None
    login_attempts: int = 0


class GetAllUsers(SQLModel):
    total: int
    data: list[User]


class User(UserOutModel, BaseSQLModel, table=True):
    password_hash: str

    # noinspection PyTypeChecker
    @classmethod
    def create_from(cls, create_model: UserCreateModel) -> User:
        user: User = BaseSQLModel.create_from.__func__(cls, create_model)
        user.password_hash = cls.hash_password(create_model.password)
        return user

    # noinspection PyTypeChecker
    def update_from(self, update_model: UserUpdateModel) -> User:
        if (update_model.new_password is not None
                and update_model.should_update_str_field('password', update_model.new_password)):
            if update_model.old_password is None or not self.check_password(update_model.old_password):
                raise InvalidPasswordException()
            new_password_hash = User.hash_password(password=update_model.new_password)
            self.update_field('password_hash', new_password_hash)
        return super().update_from(update_model)

    @classmethod
    def mock(cls) -> User:
        fake = Faker()
        first_name = fake.first_name()
        last_name = fake.last_name()
        username = first_name[0:1].lower() + last_name.lower()
        email = username + '@domain.com'
        password_hash = cls.hash_password(password=f'{first_name[0:2].lower()}')
        return User(first_name=first_name, last_name=last_name, username=username,
                    email=email, active=True, password_hash=password_hash)

    @classmethod
    def create_admin_if_none_exists(cls, session: Session):
        total_users = session.query(User).count()
        if total_users != 0:
            return
        password_hash = cls.hash_password('admin')
        first_admin = User(
            username='admin.delete.me', email='admin@delete.me', password_hash=password_hash, first_name='Admin',
            last_name='Delete', active=True)
        first_admin.save(session)

    @staticmethod
    def hash_password(password: str) -> str:
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password.decode('utf-8')

    def check_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

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
        if user is None:
            raise IncorrectCredentialsException()
        if user.active and not user.check_password(password):
            user.login_attempts += 1
            login_configs = ConfigurationManager().get_server_config().authentication.login
            if user.login_attempts > login_configs.max_login_tries:
                user.active = False
                user.update(session)
                if login_configs.notify_on_max_tries:
                    # TODO: implement notification on max tries
                    pass
                raise LoginTriesLimitExceeded()
            user.update(session)
            raise IncorrectCredentialsException()
        if not user.active:
            raise UserInactiveException(user.username)
        user.login_attempts = 0
        user.last_login = datetime.now()
        user.update(session)
        return user
