from __future__ import annotations

import random
from datetime import datetime, timedelta

from faker import Faker
from pydantic import model_validator
from sqlalchemy import Column
from sqlmodel import Field, Enum as SQLModelEnum, SQLModel

from src.models.base import BaseOutModel, BaseUpdateModel, BaseSQLModel, BaseModel
from src.models.enums import Action


MIN_PORT_NUMBER = 0
MAX_PORT_NUMBER = 65535


class CriticalRuleBaseModel(BaseModel, table=False):
    protocol: str | None = None
    src_address: str | None = None
    des_address: str | None = None
    src_port: int | None = Field(default=None, ge=MIN_PORT_NUMBER, le=MAX_PORT_NUMBER)
    des_port: int | None = Field(default=None, ge=MIN_PORT_NUMBER, le=MAX_PORT_NUMBER)
    action: Action = Field(sa_column=Column(SQLModelEnum(Action)))
    title: str
    description: str | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None

    @model_validator(mode='after')
    def check_start_and_end_times(self):
        start_time = self.start_time
        end_time = self.end_time
        if start_time and end_time and end_time < start_time:
            raise ValueError('end_time must be greater than start_time')
        return self


class CriticalRuleCreateModel(CriticalRuleBaseModel):
    pass


class CriticalRuleOutModel(CriticalRuleBaseModel, BaseOutModel):
    pass


class GetAllCriticalRules(SQLModel):
    total: int
    data: list[CriticalRuleOutModel]


class CriticalRuleUpdateModel(CriticalRuleBaseModel, BaseUpdateModel, table=False):
    action: Action | None = Field(sa_column=Column(SQLModelEnum(Action)), default=None)
    title: str | None = None


class CriticalRule(CriticalRuleOutModel, BaseSQLModel, table=True):

    @classmethod
    def mock(cls) -> CriticalRule:
        fake = Faker()
        protocol = random.choice(['tcp', 'udp', None])
        description = fake.text(max_nb_chars=random.randint(a=5, b=40))
        # network parameters
        src_address = fake.ipv4_public() if random.random() < 0.6 else None
        des_address = fake.ipv4_public() if random.random() < 0.4 else None
        src_port = fake.port_number() if random.random() < 0.3 else None
        des_port = fake.port_number() if random.random() < 0.3 else None
        # action
        action = random.choice(list(Action))
        action_str = action.value.capitalize()
        # mock start and end time
        prev_days = random.randint(a=0, b=5)
        next_days = random.randint(a=0, b=5)
        start_time = datetime.now() - timedelta(days=prev_days) if random.random() < 0.8 else None
        end_time = datetime.now() + timedelta(days=next_days) if random.random() < 0.8 else None
        # mock title
        from_str = src_address if src_address else ''
        from_str += ':' if src_address and src_port else ''
        from_str += str(src_port) if src_port else ''
        dest_str = des_address if des_address else ''
        dest_str += ':' if des_address and des_port else ''
        dest_str += str(des_port) if des_port else ''
        title = action_str + (f' from {from_str}' if from_str else '') + (f' to {dest_str}' if dest_str else '')
        return CriticalRule(
            action=action, protocol=protocol, src_address=src_address, des_address=des_address, src_port=src_port,
            des_port=des_port, title=title, description=description, start_time=start_time, end_time=end_time)
