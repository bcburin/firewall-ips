import uvicorn

from src.api.api import api
from src.common.config import ConfigurationManager
from src.models.user import User
from src.services.auth import TokenAuthManager
from src.services.database import DBSessionManager
from src.services.task import TaskManager


def build_task_manager() -> TaskManager:
    tm = TaskManager()
    tm.add_startup_task(ConfigurationManager().load, name="LoadConfigs")\
      .add_startup_task(DBSessionManager().load, name="LoadDBSessionManager")\
      .add_startup_task(DBSessionManager().create_db_and_tables, name="CreateDBAndTables")\
      .add_asynchronous_task(User.create_admin_if_none_exists, name="CreateAdminIfNoneExists",
                             session=DBSessionManager().get_session())\
      .add_asynchronous_task(TokenAuthManager().load, name="LoadTokenAuthManager")
    return tm


def main():
    tm = build_task_manager()
    tm.run_all_tasks()
    # run server
    config = ConfigurationManager().get_server_config()
    uvicorn.run("src.main:api", host=config.host, port=config.port, reload=config.dev_mode)


if __name__ == '__main__':
    main()
