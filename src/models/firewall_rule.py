from __future__ import annotations

import random

from faker import Faker
from sqlalchemy import Column
from sqlmodel import Field, Enum as SQLModelEnum

from src.common.notification import NotifiableObject
from src.models.base import BaseUpdateModel, BaseOutModel, BaseSQLModel, BaseModel
from src.models.enums import Action


class FirewallRuleBaseModel(BaseModel, table=False):
    dst_port: int | None = None
    protocol: str | None = None
    min_fl_byt_s: float | None = None
    max_fl_byt_s: float | None = None
    min_fl_pkt_s: float | None = None
    max_fl_pkt_s: float | None = None
    min_tot_fw_pk: int | None = None
    max_tot_fw_pk: int | None = None
    min_tot_bw_pk: int | None = None
    max_tot_bw_pk: int | None = None
    action: Action = Field(sa_column=Column(SQLModelEnum(Action)))


class FirewallRuleCreateModel(FirewallRuleBaseModel):
    pass


class FirewallRuleUpdateModel(FirewallRuleBaseModel, BaseUpdateModel):
    action: Action | None = Field(sa_column=Column(SQLModelEnum(Action)), default=None)


class FirewallRuleOutModel(FirewallRuleBaseModel, BaseOutModel, NotifiableObject):
    pass


class GetAllFirewallRules(BaseModel):
    total: int
    data: list[FirewallRuleOutModel]


class FirewallRule(FirewallRuleOutModel, BaseSQLModel, table=True):

    @classmethod
    def mock(cls) -> FirewallRule:
        fake = Faker()
        protocol = random.choice(['tcp', 'udp', None])
        # network parameters
        src_address = fake.ipv4_public() if random.random() < 0.7 else None
        des_address = fake.ipv4_public() if random.random() < 0.6 else None
        src_port = fake.port_number() if random.random() < 0.5 else None
        des_port = fake.port_number() if random.random() < 0.5 else None
        # action
        action = random.choice(list(Action))
        action_str = action.value.capitalize()
        return FirewallRule(
            action=action, protocol=protocol, src_address=src_address, des_address=des_address,
            src_port=src_port, des_port=des_port)
