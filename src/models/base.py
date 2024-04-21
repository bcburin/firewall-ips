from datetime import datetime

from sqlalchemy import DateTime, Column, func
from sqlmodel import SQLModel, Field


class BaseSQLModel:
    id: int = Field(default=None, primary_key=True)
    created_at: datetime | None = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=True))
    updated_at: datetime | None = Field(
        sa_column=Column(DateTime(timezone=True), onupdate=func.now(), nullable=True))


class BaseUpdateModel:

    def has_updates(self):
        return any(value is not None for value in self.__dict__.values() if value is not None)
