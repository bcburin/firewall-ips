from sqlalchemy import Column
from sqlmodel import SQLModel, Field, Enum as SQLModelEnum

from src.models.base import BaseSQLModel, BaseUpdateModel
from src.models.enums import Action


class CriticalRuleBaseModel(SQLModel, table=False):
    src_port: int | None = None
    des_port: int | None = None
    nat_src_port: int | None = None
    nat_des_port: int | None = None
    action: Action = Field(sa_column=Column(SQLModelEnum(Action)))
    title: str
    description: str | None = None


class CriticalRuleCreateModel(CriticalRuleBaseModel):
    pass


class CriticalRuleOutModel(CriticalRuleBaseModel):
    pass


class CriticalRuleUpdateModel(CriticalRuleBaseModel, BaseUpdateModel, table=False):
    action: Action | None = Field(sa_column=Column(SQLModelEnum(Action)), default=None)
    title: str | None = None


class CriticalRule(CriticalRuleBaseModel, table=True):
    id: int = Field(default=None, primary_key=True)
