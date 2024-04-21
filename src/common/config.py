import json
from enum import Enum
from functools import cache, cached_property
from pathlib import Path
from typing import TypeVar, Type

from pydantic import BaseModel, TypeAdapter

from src.common.utils import get_config_dir, convert_dict_keys_camel_to_snake, \
    resolve_variables_in_path, create_dir_if_not_exists


class CompressionToolOption(str, Enum):
    ZIP = 'zip'
    GZIP = 'gz'


class TrainingDataTypeOption(str, Enum):
    FILE = 'file'


T = TypeVar('T', bound='BaseConfig')


class BaseConfig(BaseModel):

    __config__filename__ = None

    @classmethod
    @cache
    def get(cls: Type[T]) -> T:
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
        verbose: bool = False

    class AIModelConfig(BaseModel):
        class TrainingConfig(BaseModel):
            class TrainingDataConfig(BaseModel):
                type: TrainingDataTypeOption = TrainingDataTypeOption.FILE
                path: str = '$data/log.xlsx'

                @cached_property
                @resolve_variables_in_path
                def resolved_path(self) -> Path:
                    return Path(self.path)

            cron_string: str
            run_on_start: bool = False
            data: TrainingDataConfig

        class PersistenceConfig(BaseModel):
            class CompressionConfig(BaseModel):
                enable: bool = True
                tool: CompressionToolOption = CompressionToolOption.ZIP
                compress_latest_model: bool = False

            directory: str = '$root/archive'
            max_saved_models: int | None = None
            compression: CompressionConfig
            enable: bool = True

            @cached_property
            @create_dir_if_not_exists
            @resolve_variables_in_path
            def resolved_directory(self) -> Path:
                return Path(self.directory)

        training: TrainingConfig
        persistence: PersistenceConfig

    host: str
    port: int
    database: DbConfig
    ai_model: AIModelConfig
    dev_mode: bool = False


if __name__ == '__main__':
    sc = ServerConfig.get()
    print(sc)
