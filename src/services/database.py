from typing import Iterator, TypeVar, Generic, Type, Any

from fastapi.encoders import jsonable_encoder
from sqlmodel import create_engine, Session, SQLModel

from src.common.config import ServerConfig
from src.common.utils import Singleton


class DBSessionManager(metaclass=Singleton):

    def __init__(self, echo: bool = False):
        self._config: ServerConfig.DbConfig = ServerConfig.get().database
        self._engine = create_engine(self.get_uri(), echo=echo)

    def get_uri(self) -> str:
        return (f'{self._config.dbms}://{self._config.user}:{self._config.password}@'
                f'{self._config.host}:{self._config.port}/{self._config.name}')

    def get_engine(self):
        return self._engine

    def get_session(self) -> Session:
        return Session(self.get_engine())

    def create_db_and_tables(self):
        SQLModel.metadata.create_all(self._engine)


def get_session() -> Iterator[Session]:
    yield DBSessionManager(echo=ServerConfig.get().database.verbose).get_session()


ModelType = TypeVar("ModelType")
CreateModelType = TypeVar("CreateModelType")
UpdateModelType = TypeVar("UpdateModelType")


class BaseDbService(Generic[ModelType, CreateModelType, UpdateModelType]):
    def __init__(self, *, session: Session, model: Type[ModelType] | None = None):
        self.model = model
        self.session = session

    def get_by_id(self, id_value) -> ModelType | None:
        return self.session.query(self.model).get(id_value)

    def get_by_unique_attribute(
            self,
            id_value: Any,
            id_name: str = 'id'
    ) -> ModelType | None:
        return self.session.query(self.model).filter(getattr(self.model, id_name) == id_value).first()

    def get_all(
            self, *,
            skip: int = 0,
            limit: int | None = None,
            filters: dict[str, Any | set[Any]] | None = None,
            order_by: str = 'id',
            columns: list | None = None
    ) -> list[ModelType]:
        query = self.session.query(*columns) if columns else self.session.query(self.model)
        if filters:
            for col, val in filters.items():
                if isinstance(val, set):
                    query = query.filter(getattr(self.model, col).in_(val))
                else:
                    query = query.filter(getattr(self.model, col) == val)
        if hasattr(self.model, order_by):
            query = query.order_by(order_by)
        query = query.offset(skip)
        if limit:
            query = query.limit(limit)
        return query.all()

    def create(
            self,
            *,
            obj: CreateModelType,
            refresh: bool = True
    ) -> ModelType:
        obj_in_data = jsonable_encoder(obj, by_alias=False)
        db_obj = self.model(**obj_in_data)  # type: ignore
        self.session.add(db_obj)
        self.session.commit()
        if refresh:
            self.session.refresh(db_obj)
        return db_obj

    def update(
            self,
            *,
            db_obj: ModelType,
            obj: UpdateModelType | dict[str, Any]
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if not obj_data:
            self.session.refresh(db_obj)
            obj_data = jsonable_encoder(db_obj)
        if isinstance(obj, dict):
            update_data = obj
        else:
            update_data = obj.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        self.session.add(db_obj)
        self.session.commit()
        self.session.refresh(db_obj)
        return db_obj

    def remove(self, *, pk: Any) -> ModelType | None:
        obj = self.session.query(self.model).get(pk)
        if not obj:
            return None
        self.session.delete(obj)
        self.session.commit()
        return obj
