from datetime import datetime

from pydantic import model_validator
from sqlalchemy import Column
from sqlmodel import SQLModel, Field, Enum as SQLModelEnum

from src.models.base import BaseOutModel, BaseUpdateModel
from src.models.enums import Action


MIN_PORT_NUMBER = 0
MAX_PORT_NUMBER = 65535


class CriticalRuleBaseModel(SQLModel, table=False):
    protocol: str | None = None
    src_address: str | None = None
    des_address: str | None = None
    src_port: int | None = Field(default=None, ge=MIN_PORT_NUMBER, le=MAX_PORT_NUMBER)
    des_port: int | None = Field(default=None, ge=MIN_PORT_NUMBER, le=MAX_PORT_NUMBER)
    nat_src_port: int | None = Field(default=None, ge=MIN_PORT_NUMBER, le=MAX_PORT_NUMBER)
    nat_des_port: int | None = Field(default=None, ge=MIN_PORT_NUMBER, le=MAX_PORT_NUMBER)
    action: Action = Field(sa_column=Column(SQLModelEnum(Action)))
    title: str
    description: str | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None

    @model_validator(mode='after')
    def check_start_and_end_times(self):
        start_time = self.start_time
        end_time = self.end_time
        if start_time and end_time and end_time <= start_time:
            raise ValueError('end_time must be greater than start_time')
        return self


class CriticalRuleCreateModel(CriticalRuleBaseModel):
    pass


class CriticalRuleOutModel(CriticalRuleBaseModel, BaseOutModel):
    pass


class CriticalRuleUpdateModel(CriticalRuleBaseModel, BaseUpdateModel, table=False):
    action: Action | None = Field(sa_column=Column(SQLModelEnum(Action)), default=None)
    title: str | None = None


class CriticalRule(CriticalRuleOutModel, table=True):
    pass
