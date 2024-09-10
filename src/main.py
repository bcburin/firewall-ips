import uvicorn

from src.ai_module.ensamble_manager import EnsembleManager
from src.ai_module.pipeline import train_pipeline
from src.api.api import api
from src.common.config import ConfigurationManager, ServerConfig
from src.models.user import User
from src.services.auth import TokenAuthManager
from src.services.database import DBSessionManager
from src.services.notification import FWRuleNotificationServiceManager
from src.services.task import TaskManager, PeriodicTask


def build_task_manager(config: ServerConfig) -> TaskManager:
    tm = TaskManager()
    # create periodic tasks
    retraining_task = PeriodicTask(
        cron_string=config.ai_module.training.cron_string,
        task=train_pipeline,
        run_on_start=config.ai_module.training.run_on_start,
    )
    send_enqueued_fw_notifications = PeriodicTask(
        cron_string=config.notification.cron_string,
        task=lambda: FWRuleNotificationServiceManager().send_notifications(),
        run_on_start=False,
    )
    # add tasks
    tm.add_startup_task(DBSessionManager().load, name="LoadDBSessionManager")\
      .add_startup_task(DBSessionManager().create_db_and_tables, name="CreateDBAndTables")\
      .add_asynchronous_task(User.create_admin_if_none_exists, name="CreateAdminIfNoneExists",
                             session=DBSessionManager().get_session())\
      .add_asynchronous_task(TokenAuthManager().load, name="LoadTokenAuthManager")\
      .add_asynchronous_task(EnsembleManager().load, name="LoadEnsembleManager")\
      .add_periodic_task(retraining_task, name="ModelRetrainingTask")\
      .add_periodic_task(send_enqueued_fw_notifications, name="SendEnqueuedFWNotifications")
    return tm


def main():
    # load configs
    ConfigurationManager().load()
    config = ConfigurationManager().get_server_config()
    # run tasks at startup
    tm = build_task_manager(config)
    tm.run_all_tasks()
    # run server
    uvicorn.run("src.main:api", host=config.host, port=config.port, reload=config.dev_mode)


if __name__ == '__main__':
    main()
