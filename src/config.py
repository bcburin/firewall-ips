import json
from functools import cache

from pydantic import BaseModel, TypeAdapter

from src.utils import get_config_dir


class BaseConfig(BaseModel):

    __config__filename__ = None

    @classmethod
    @cache
    def load(cls):
        with open(get_config_dir() / cls.__config__filename__) as f:
            data = json.load(f)
        return TypeAdapter(cls).validate_python(data)


class ServerConfig(BaseConfig):
    __config__filename__ = 'server.json'

    class DbConfig(BaseModel):
        name: str
        host: str
        port: str
        dbms: str
        user: str
        password: str

    database: DbConfig
