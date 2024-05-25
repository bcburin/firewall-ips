from datetime import datetime

from sqlmodel import SQLModel, Field


class BaseOutModel(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)


class BaseUpdateModel:

    def has_updates(self):
        return any(value is not None for value in self.__dict__.values() if value is not None)
