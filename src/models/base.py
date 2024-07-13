from __future__ import annotations

from datetime import datetime

from pydantic.alias_generators import to_camel
from sqlmodel import SQLModel, Field, Session


class BaseModel(SQLModel):
    class Config:
        alias_generator = to_camel
        populate_by_name = True


class BaseSQLModel(BaseModel):

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

    def update_from(self, update_model: BaseUpdateModel) -> BaseSQLModel:
        for field, new_val in update_model.__dict__.items():
            if not update_model.should_update_field(field, new_val):
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


class BaseOutModel(BaseModel):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)


allow_empty_str_fields = {'description'}


class BaseUpdateModel(BaseModel):

    @classmethod
    def should_update_str_field(cls, field: str, new_val: str):
        if new_val == '' and field not in allow_empty_str_fields:
            return False
        return True

    @classmethod
    def should_update_field(cls, field: str, new_val: any) -> bool:
        if new_val is None:
            return False
        if isinstance(new_val, str) and not cls.should_update_str_field(field, new_val):
            return False
        return True

    def has_updates(self):
        return any(value for field, value in self.__dict__.items() if self.should_update_field(field, value))
