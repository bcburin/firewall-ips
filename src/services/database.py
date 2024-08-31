from typing import Iterator, Annotated

from fastapi import Depends
from sqlmodel import create_engine, Session, SQLModel

from src.common.config import ConfigurationManager, DbConfig
from src.common.exceptions.db import DbManagerNotLoadedException
from src.common.utils import LoadableSingleton


class DBSessionManager(LoadableSingleton):

    def __init__(self):
        self._config: DbConfig | None = None
        self._engine = None
        super().__init__()

    def _load(self):
        self._config = ConfigurationManager().get_database_config()
        self._engine = create_engine(self.get_uri(), echo=self._config.verbose)

    def _loaded(self) -> bool:
        return self._config is not None and self._engine is not None

    def _not_loaded_exception(self) -> Exception:
        return DbManagerNotLoadedException()

    def get_uri(self) -> str:
        return (f'{self._config.dbms}://{self._config.user}:{self._config.password}@'
                f'{self._config.host}:{self._config.port}/{self._config.name}')

    def get_session(self) -> Session:
        with self.load_guard():
            return Session(self._engine)

    def create_db_and_tables(self):
        SQLModel.metadata.create_all(self._engine)


def get_session() -> Iterator[Session]:
    yield DBSessionManager().get_session()


InjectedSession = Annotated[Session, Depends(get_session)]
