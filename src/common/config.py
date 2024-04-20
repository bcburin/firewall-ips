import json
from enum import Enum
from functools import cache

from pydantic import BaseModel, TypeAdapter

from src.common.utils import get_config_dir, get_archive_dir, get_data_dir, convert_dict_keys_camel_to_snake


class CompressionToolOption(str, Enum):
    ZIP = 'zip'
    GZIP = 'gzip'


class TrainingDataTypeOption(str, Enum):
    FILE = 'file'


class BaseConfig(BaseModel):

    __config__filename__ = None

    @classmethod
    @cache
    def load(cls):
        with open(get_config_dir() / cls.__config__filename__) as f:
            data = convert_dict_keys_camel_to_snake(json.load(f))
        return TypeAdapter(cls).validate_python(data)


class ServerConfig(BaseConfig):
    __config__filename__ = 'server.json'

    class DbConfig(BaseModel):
        name: str
        host: str
        port: int
        dbms: str
        user: str
        password: str

    class AIModelConfig(BaseModel):
        class TrainingConfig(BaseModel):
            class TrainingDataConfig(BaseModel):
                type: TrainingDataTypeOption = TrainingDataTypeOption.FILE
                path: str = get_data_dir() / 'log.xlsx'

            cron_string: str
            run_on_start: bool = False
            data: TrainingDataConfig

        class PersistenceConfig(BaseModel):
            class CompressionConfig(BaseModel):
                enable: bool = True
                tool: CompressionToolOption = CompressionToolOption.ZIP
                compress_latest_model: bool = False

            directory: str = get_archive_dir()
            max_saved_models: int | None = None
            compression: CompressionConfig

        training: TrainingConfig
        persistence: PersistenceConfig

    host: str
    port: int
    database: DbConfig
    ai_model: AIModelConfig
    dev_mode: bool = False


if __name__ == '__main__':
    sc = ServerConfig.load()
    print(sc)
