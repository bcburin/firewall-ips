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
    resolve_variables_in_path, create_dir_if_not_exists, CompressionTool, ZipCompressionTool, GzipCompressionTool
from src.common.singleton import LoadableSingleton


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
    DIRECTORY = 'directory'


T = TypeVar('T', bound='BaseConfig')


class BaseConfig(BaseModel):

    __config__filename__ = None

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

        @property
        def resolved_tool(self) -> CompressionTool:
            return CompressionToolOption.get_tool_implementation(self.tool)

    directory: str = '$root/repository'
    load_latest_on_start: bool = True
    max_saved_models: int | None = None
    compression: CompressionConfig

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
    cron_string: str
    methods: MethodsConfig

    def has_any_method(self):
        if self.methods.email is not None:
            return True
        return False


class AIModuleConfig(BaseModel):
    class PeriodicDataReadingConfig(BaseModel):
        class DataConfig(BaseModel):
            type: TrainingDataTypeOption = TrainingDataTypeOption.FILE
            path: str = '$data/log.xlsx'

            @cached_property
            @resolve_variables_in_path
            def resolved_path(self) -> Path:
                return Path(self.path)

        cron_string: str
        run_on_start: bool = False
        data: DataConfig

    training: PeriodicDataReadingConfig
    static_rule_creation: PeriodicDataReadingConfig
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

class firewall_config(BaseModel):
    chain: str
    table: str

class executor_config(BaseModel):
    ssh_host: str
    ssh_user: str
    ssh_key_path: str

class ServerConfig(BaseConfig):
    __config__filename__ = 'server.json'

    host: str
    port: int
    database: DbConfig
    ai_module: AIModuleConfig
    notification: NotificationConfig
    dev_mode: bool = False
    authentication: AuthConfig
    firewall_info: firewall_config
    executor_credentials: executor_config


class BaseAIModelConfig(BaseModel):
    num_class: list[int]


class LightgbmConfig(BaseAIModelConfig):
    num_leaves: list[int]
    learning_rate: list[float]
    n_estimators: list[int]


class GradientBoostConfig(BaseModel):
    learning_rate: list[float]
    n_estimators: list[int]
    subsample: list[float]
    max_depth: list[int]


class LogisticRegressionConfig(BaseAIModelConfig):
    penalty: list[str]


class MultiLayerPerceptronConfig(BaseAIModelConfig):
    hidden_layer: list[int]
    momentum: list[float]
    early_stopping: list[bool]


class RandomForestConfig(BaseAIModelConfig):
    n_estimators: list[int]
    criterion: list[str]


class SVMConfig(BaseAIModelConfig):
    kernel: list[str]
    degree: list[int]


class KNNConfig(BaseAIModelConfig):
    n_neighbors: list[int]


class NNConfig(BaseAIModelConfig):
    learning_rate: list[float]


class AIModelsTrainingConfig(BaseConfig):
    __config__filename__ = 'models.json'

    lightgbm: LightgbmConfig
    gradientboost: GradientBoostConfig
    logisticregression: LogisticRegressionConfig
    multilayerperceptron: MultiLayerPerceptronConfig
    randomforest: RandomForestConfig
    svm: SVMConfig
    knn: KNNConfig


class ColumnType(str, Enum):
    FLOAT = "float"
    INT = "int"


class DatasetConfig(BaseConfig):
    __config__filename__ = "dataset.json"

    class ColumnDescription(BaseModel):
        name: str
        type: ColumnType
        must_include: bool = False

    class MappingConfig(BaseModel):
        label: str
        value: int

    columns: list[ColumnDescription]
    mapping: list[MappingConfig]
    protocol: list[str]
    sample_size: int

    @property
    def num_classes(self) -> int:
        return len(set([mapping.value for mapping in self.mapping]))

    @property
    def columns_not_to_remove(self) -> list[str]:
        return [col.name for col in self.columns if col.must_include]


class ConfigurationManager(LoadableSingleton):

    def __init__(self):
        self._server_config: ServerConfig | None = None
        self._ai_models_config: AIModelsTrainingConfig | None = None
        self._dataset_config: DatasetConfig | None = None
        super().__init__()

    def _load(self):
        self._server_config = ServerConfig.read_file()
        self._ai_models_config = AIModelsTrainingConfig.read_file()
        self._dataset_config = DatasetConfig.read_file()

    def _loaded(self) -> bool:
        return (self._server_config is not None and
                self._ai_models_config is not None and
                self._dataset_config is not None)

    @property
    def _not_loaded_exception(self) -> Exception:
        return ConfigurationNotLoaded("cannot load configs")

    def get_server_config(self, redact_sensitive_data: bool = False) -> ServerConfig:
        with self.load_guard():
            if redact_sensitive_data:
                return self._get_redacted_copy_of_server_config()
            return self._server_config

    def get_database_config(self, redact_sensitive_data: bool = False) -> DbConfig:
        return self.get_server_config(redact_sensitive_data=redact_sensitive_data).database

    def get_notification_config(self) -> NotificationConfig:
        return self.get_server_config().notification

    def get_auth_config(self) -> AuthConfig:
        return self.get_server_config().authentication

    def _get_redacted_copy_of_server_config(self):
        config_copy = self._server_config.model_copy(deep=True)
        config_copy.database.password = "<password>"
        if config_copy.notification.methods.email:
            config_copy.notification.methods.email.sender.email = "<email>"
            config_copy.notification.methods.email.sender.password = "<password>"
        config_copy.authentication.token.key = "<key>"
        return config_copy

    def get_ai_models_training_config(self) -> AIModelsTrainingConfig:
        with self.load_guard():
            return self._ai_models_config

    def get_dataset_config(self) -> DatasetConfig:
        with self.load_guard():
            return self._dataset_config


configuration_manager = ConfigurationManager()


InjectedServerConfig = Annotated[
    ServerConfig, Depends(lambda: configuration_manager.get_server_config())]

InjectedAuthConfig = Annotated[
    AuthConfig, Depends(lambda: configuration_manager.get_server_config().authentication)]

InjectedTokenConfig = Annotated[
    AuthConfig.TokenConfig, Depends(lambda: configuration_manager.get_server_config().authentication.token)]
