from datetime import datetime

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


class UserUpdateModel(UserBaseModel, BaseUpdateModel):
    password: str | None
    active: bool | None


class UserOutModel(UserBaseModel, BaseOutModel):
    last_login: datetime | None
    login_attempts: int = 0


class User(UserOutModel, table=True):
    password_hash: str
    # external_auth_id: str | None = None
    # external_auth_data: dict | None = None
