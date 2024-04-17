from sqlalchemy import Column
from sqlmodel import SQLModel, Field, Enum as SQLModelEnum

from src.models.enums import Action


class CriticalRule(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    src_port: int | None
    des_port: int | None
    nat_src_port: int | None
    nat_des_port: int | None
    action: Action = Field(sa_column=Column(SQLModelEnum(Action)))
    title: str
    description: str | None
