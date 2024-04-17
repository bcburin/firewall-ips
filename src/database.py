from sqlmodel import create_engine, Session, SQLModel

from src.config import ServerConfig
from src.utils import Singleton


class DBManager(metaclass=Singleton):

    def __init__(self, echo: bool = False):
        self._config: ServerConfig.DbConfig = ServerConfig.load().database
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


if __name__ == '__main__':
    from src.models.firewall_rule import FirewallRule
    from src.models.critical_rule import CriticalRule
    from src.models.enums import Action

    db_manager = DBManager(echo=True)
    db_manager.create_db_and_tables()

    http_rule = CriticalRule(des_port=80, action=Action.ALLOW, title='HTTP Rule')
    https_rule = CriticalRule(des_port=443, action=Action.ALLOW, title='HTTPS Rule', description='2 important 2 block')

    with db_manager.get_session() as session:
        session.add(http_rule)
        session.add(https_rule)
        session.commit()