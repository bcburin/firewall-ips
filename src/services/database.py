from typing import Iterator,Annotated

from fastapi import Depends
from sqlmodel import create_engine, Session, SQLModel

from src.common.config import ConfigurationManager, DbConfig
from src.common.exceptions.db import DbManagerNotLoadedException
from src.common.utils import Singleton


class DBSessionManager(metaclass=Singleton):

    def __init__(self):
        self._config: DbConfig | None = None
        self._engine = None
        self._loaded = False

    def load(self):
        self._config = ConfigurationManager().get_server_config().database
        self._engine = create_engine(self.get_uri(), echo=self._config.verbose)
        self._loaded = True

    def try_load(self):
        if self._loaded:
            return
        n_tries = 0
        while not self._loaded and n_tries < 3:
            self.load()

    def get_uri(self) -> str:
        return (f'{self._config.dbms}://{self._config.user}:{self._config.password}@'
                f'{self._config.host}:{self._config.port}/{self._config.name}')

    def get_engine(self):
        return self._engine

    def get_session(self) -> Session:
        if not self._loaded:
            self.try_load()
            if not self._loaded:
                raise DbManagerNotLoadedException()
        return Session(self.get_engine())

    def create_db_and_tables(self):
        SQLModel.metadata.create_all(self._engine)


def get_session() -> Iterator[Session]:
    yield DBSessionManager().get_session()


InjectedSession = Annotated[Session, Depends(get_session)]
