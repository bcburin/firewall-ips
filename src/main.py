import uvicorn

from src.api.api import api
from src.common.config import ServerConfig
from src.services.database import DBSessionManager


if __name__ == '__main__':
    config: ServerConfig = ServerConfig.get()
    DBSessionManager(echo=config.database.verbose).create_db_and_tables()
    uvicorn.run("src.main:api", host=config.host, port=config.port, reload=config.dev_mode)
