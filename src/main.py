import uvicorn

from src.api.api import api
from src.common.config import ConfigurationManager
from src.services.auth import TokenAuthManager
from src.services.database import DBSessionManager


def main():
    # load configurations from config files
    ConfigurationManager().load_configs()
    config = ConfigurationManager().get_server_config()
    # load database and create tables from metadata
    DBSessionManager().load()
    DBSessionManager().create_db_and_tables()
    # load authentication service
    TokenAuthManager().load()
    # run server
    uvicorn.run("src.main:api", host=config.host, port=config.port, reload=config.dev_mode)


if __name__ == '__main__':
    main()
