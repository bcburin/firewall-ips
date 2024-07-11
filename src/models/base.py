from datetime import datetime

from pydantic.alias_generators import to_camel
from sqlmodel import SQLModel, Field


class BaseSQLModel(SQLModel):
    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class BaseOutModel(BaseSQLModel):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)


class BaseUpdateModel:

    def has_updates(self):
        return any(value is not None for value in self.__dict__.values() if value is not None)
