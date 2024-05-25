from datetime import datetime

from pydantic import EmailStr
from sqlalchemy import Column, String
from sqlmodel import SQLModel, AutoString, Field

from src.models.base import BaseUpdateModel, BaseOutModel


class UserBaseModel(SQLModel):
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
    pass


class User(UserOutModel, table=True):
    password_hash: str
    last_login: datetime | None
    login_attempts: int = 0
    # external_auth_id: str | None = None
    # external_auth_data: dict | None = None
