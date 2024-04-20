from sqlalchemy import Column
from sqlmodel import SQLModel, Field, Enum as SQLModelEnum

from src.models.base import BaseSQLModel, BaseUpdateModel
from src.models.enums import Action


class FirewallRuleBaseModel(SQLModel, table=False):
    src_port: int | None = None
    des_port: int | None = None
    nat_src_port: int | None = None
    nat_des_port: int | None = None
    action: Action = Field(sa_column=Column(SQLModelEnum(Action)))


class FirewallRuleCreateModel(FirewallRuleBaseModel):
    pass


class FirewallRuleUpdateModel(FirewallRuleBaseModel, BaseUpdateModel):
    action: Action | None = Field(sa_column=Column(SQLModelEnum(Action)), default=None)


class FirewallRuleOutModel(FirewallRuleBaseModel):
    pass


class FirewallRule(FirewallRuleBaseModel, BaseSQLModel, table=True):
    pass
