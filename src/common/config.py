from __future__ import annotations

import json
from enum import Enum
from functools import cached_property
from pathlib import Path
from typing import TypeVar, Type, Annotated

from fastapi import Depends
from pydantic import BaseModel, TypeAdapter, Field

from src.common.exceptions.config import ConfigurationNotLoaded
from src.common.utils import get_config_dir, convert_dict_keys_camel_to_snake, \
    resolve_variables_in_path, create_dir_if_not_exists, CompressionTool, ZipCompressionTool, GzipCompressionTool, \
    Singleton


class CompressionToolOption(str, Enum):
    ZIP = 'zip'
    GZIP = 'gz'

    @staticmethod
    def get_tool_implementation(tool_option: CompressionToolOption | str) -> CompressionTool:
        if isinstance(tool_option, str):
            tool_option = CompressionToolOption(tool_option)
        _map = {
            CompressionToolOption.ZIP: ZipCompressionTool(),
            CompressionToolOption.GZIP: GzipCompressionTool(),
        }
        return _map[tool_option]


class TrainingDataTypeOption(str, Enum):
    FILE = 'file'


T = TypeVar('T', bound='BaseConfig')


class BaseConfig(BaseModel):

    __config__filename__ = None

    @classmethod
    def get(cls):
        raise NotImplemented

    @classmethod
    def read_file(cls: Type[T]) -> T:
        with open(get_config_dir() / cls.__config__filename__) as f:
            data = convert_dict_keys_camel_to_snake(json.load(f))
        return TypeAdapter(cls).validate_python(data)


class DbConfig(BaseModel):
    name: str
    host: str
    port: int
    dbms: str
    user: str
    password: str
    verbose: bool = False


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


class EmailNotificationConfig(BaseModel):

    class SmtpConfig(BaseModel):
        server: str
        port: int
        ehlo: str | None = None

    class SenderConfig(BaseModel):
        email: str
        password: str

    enable: bool = True
    subject: str
    template_path: str
    smtp: SmtpConfig
    sender: SenderConfig
    mailing_list: list[str]

    @cached_property
    @resolve_variables_in_path
    def resolved_template_path(self) -> Path:
        return Path(self.template_path)


class NotificationConfig(BaseModel):
    class MethodsConfig(BaseModel):
        email: EmailNotificationConfig | None = None

    enable: bool = True
    max_queue_size: int = 128
    methods: MethodsConfig


class AIModuleConfig(BaseModel):
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

    training: TrainingConfig
    persistence: PersistenceConfig


class AuthConfig(BaseModel):

    class TokenConfig(BaseModel):
        key: str
        algorithm: str
        expiration_time_in_minutes: int = Field(gt=0, default=360)

    class LoginConfig(BaseModel):
        method: str
        max_login_tries: int | None = None
        notify_on_max_tries: bool = True

    token: TokenConfig
    login: LoginConfig


class ServerConfig(BaseConfig):
    __config__filename__ = 'server.json'

    host: str
    port: int
    database: DbConfig
    ai_module: AIModuleConfig
    notification: NotificationConfig
    dev_mode: bool = False
    authentication: AuthConfig


class BaseAIModelConfig(BaseModel):
    num_class: int


class LightgbmConfig(BaseAIModelConfig):
    objective: list[str]
    boosting_type: list[str]
    num_leaves: list[int]
    learning_rate: list[float]
    n_estimators: list[int]


class GradientBoostConfig(BaseAIModelConfig):
    loss: list[str]
    learning_rate: list[float]
    n_estimators: list[int]
    subsample: list[float]
    max_depth: list[int]


class LogisticRegressionConfig(BaseAIModelConfig):
    penalty: list[str]


class MultiLayerPerceptronConfig(BaseAIModelConfig):
    solver: list[str]
    hidden_layer: list[int]
    activation: list[str]
    learning_rate: list[str]
    learning_rate_init: list[float]
    momentum: list[float]
    early_stopping: list[bool]


class RandomForestConfig(BaseAIModelConfig):
    n_estimators: list[int]
    criterion: list[str]


class SVMConfig(BaseAIModelConfig):
    kernel: list[str]
    degree: list[int]


class AIModelsTrainingConfig(BaseConfig):
    __config__filename__ = 'models.json'

    lightgbm: list[LightgbmConfig]
    gradientboost: list[GradientBoostConfig]
    logisticregression: list[LogisticRegressionConfig]
    multilayerperceptron: list[MultiLayerPerceptronConfig]
    randomforest: list[RandomForestConfig]
    svm: list[SVMConfig]


class ConfigurationManager(metaclass=Singleton):

    def __init__(self):
        self._server_config: ServerConfig | None = None

    def load_configs(self):
        self._server_config = ServerConfig.read_file()

    def get_server_config(self):
        if self._server_config is None:
            raise ConfigurationNotLoaded("cannot retrieve server configs")
        return self._server_config


configuration_manager = ConfigurationManager()


InjectedServerConfig = Annotated[
    ServerConfig, Depends(lambda: configuration_manager.get_server_config())]

InjectedAuthConfig = Annotated[
    AuthConfig, Depends(lambda: configuration_manager.get_server_config().authentication)]

InjectedTokenConfig = Annotated[
    AuthConfig.TokenConfig, Depends(lambda: configuration_manager.get_server_config().authentication.token)]