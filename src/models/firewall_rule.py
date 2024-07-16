from sqlalchemy import Column
from sqlmodel import Field, Enum as SQLModelEnum

from src.common.notification import NotifiableObject
from src.models.base import BaseUpdateModel, BaseOutModel, BaseSQLModel, BaseModel
from src.models.enums import Action


class FirewallRuleBaseModel(BaseModel, table=False):
    protocol: str | None = None
    src_address: str | None = None
    des_address: str | None = None
    src_port: int | None = None
    des_port: int | None = None
    nat_src_port: int | None = None
    nat_des_port: int | None = None
    action: Action = Field(sa_column=Column(SQLModelEnum(Action)))


class FirewallRuleCreateModel(FirewallRuleBaseModel):
    pass


class FirewallRuleUpdateModel(FirewallRuleBaseModel, BaseUpdateModel):
    action: Action | None = Field(sa_column=Column(SQLModelEnum(Action)), default=None)


class FirewallRuleOutModel(FirewallRuleBaseModel, BaseOutModel, NotifiableObject):
    pass


class GetAllFirewallRules(BaseModel):
    data: list[FirewallRuleOutModel]
    total: int


class FirewallRule(FirewallRuleOutModel, BaseSQLModel, table=True):
    pass
