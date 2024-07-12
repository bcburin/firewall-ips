from __future__ import annotations

from datetime import datetime

from pydantic.alias_generators import to_camel
from sqlalchemy import orm
from sqlmodel import SQLModel, Field, Session


class BaseSQLModel(SQLModel):

    def save(self, session: Session, commit: bool = True) -> BaseSQLModel:
        session.add(self)
        if commit:
            try:
                session.commit()
            except Exception as e:
                session.rollback()
                raise e
            session.refresh(self)
        return self

    def update(self, session: Session) -> BaseSQLModel:
        session.commit()
        session.refresh(self)
        return self

    def delete(self, session: Session, commit=True):
        session.delete(self)
        if commit:
            session.commit()

    @classmethod
    def create_from(cls, create_model: SQLModel) -> BaseSQLModel:
        obj = cls()
        for field, val in create_model.__dict__.items():
            if hasattr(obj, field):
                setattr(obj, field, val)
        return obj

    def update_from(self, update_model: SQLModel) -> BaseSQLModel:
        for field, new_val in update_model.__dict__.items():
            if new_val is None:
                continue
            if hasattr(self, field):
                old_val = getattr(self, field)
                if new_val == old_val:
                    continue
                setattr(self, field, new_val)
        return self

    class Config:
        alias_generator = to_camel
        populate_by_name = True


class BaseOutModel(BaseSQLModel):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)


class BaseUpdateModel:

    def has_updates(self):
        return any(value is not None for value in self.__dict__.values() if value is not None)
