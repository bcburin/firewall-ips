import gzip
import re
import shutil
import zipfile
from abc import ABC, abstractmethod
from functools import cache
from pathlib import Path
from typing import Callable
import inspect


def create_dir_if_not_exists(f: Callable[..., Path]) -> Callable[..., Path]:
    def inner(*args, **kwargs) -> Path:
        path = f(*args, **kwargs)
        if not path.is_dir():
            path.mkdir(parents=True, exist_ok=True)
        return path

    return inner


def get_subdir_factory(subdir: str) -> Callable[[], Path]:
    @cache
    @create_dir_if_not_exists
    def inner() -> Path:
        return get_project_dir() / subdir

    return inner


@cache
def get_project_dir() -> Path:
    current_dir = Path(__file__)
    return current_dir.parent.parent.parent


get_data_dir = get_subdir_factory('data')
get_config_dir = get_subdir_factory('config')
get_statics_dir = get_subdir_factory('statics')


_path_vars = {
    '$root': get_project_dir(),
    '$data': get_data_dir(),
    '$config': get_config_dir(),
    '$statics': get_statics_dir(),
}


def resolve_variables_in_path(f: Callable[..., Path]) -> Callable[..., Path]:
    def inner(*args, **kwargs):
        path_str = str(f(*args, **kwargs))
        for var, val in _path_vars.items():
            if var in path_str:
                path_str = path_str.replace(var, str(val))
        return Path(path_str)

    return inner


def convert_str_camel_to_snake(s: str) -> str:
    s = re.sub(r'(.)([A-Z][a-z]+)', r'\1_\2', s)
    s = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', s)
    return re.sub(r'([a-z])([A-Z])', r'\1_\2', s).lower()


def convert_dict_keys_camel_to_snake(d):
    if isinstance(d, list):
        return [convert_dict_keys_camel_to_snake(i) if isinstance(i, (dict, list)) else i for i in d]
    return {convert_str_camel_to_snake(a):
            convert_dict_keys_camel_to_snake(b)
            if isinstance(b, (dict, list))
            else b for a, b in d.items()}


def convert_str_camel_to_hyphen(s: str) -> str:
    return re.sub(r'(?<!^)(?=[A-Z][a-z])', '-', s).lower()


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class CompressionTool(ABC):
    @staticmethod
    @abstractmethod
    def compress(filepath: Path | str):
        ...

    @staticmethod
    @abstractmethod
    def decompress(compressed_filepath: Path, output_filepath: Path) -> None:
        ...


class ZipCompressionTool(CompressionTool):
    @staticmethod
    def compress(filepath: Path):
        with zipfile.ZipFile(str(filepath) + '.zip', 'w') as zip_file:
            zip_file.write(filepath, arcname=filepath.name)

    @staticmethod
    def decompress(compressed_filepath: Path, output_filepath: Path) -> None:
        with zipfile.ZipFile(compressed_filepath, 'r') as zip_file:
            # Extract the only file in the zip file to a temporary directory
            temp_dir = output_filepath.parent
            zip_file.extractall(path=temp_dir)
            # Move the extracted file to the specified output filepath
            extracted_file = temp_dir / zip_file.namelist()[0]
            extracted_file.rename(output_filepath)


class GzipCompressionTool(CompressionTool):
    @staticmethod
    def compress(filepath: Path) -> None:
        with open(filepath, 'rb') as f_in:
            with gzip.open(str(filepath) + '.gz', 'wb') as f_out:
                f_out.writelines(f_in)

    @staticmethod
    def decompress(compressed_filepath: Path, output_filepath: Path) -> None:
        with gzip.open(compressed_filepath, 'rb') as f_in:
            with open(output_filepath, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)


def filter_dict(dict_to_filter, thing_with_kwargs):
    sig = inspect.signature(thing_with_kwargs)
    filter_keys = [param.name for param in sig.parameters.values() if param.kind == param.POSITIONAL_OR_KEYWORD]
    filtered_dict = {filter_key:dict_to_filter[filter_key] for filter_key in filter_keys if filter_key in dict_to_filter}
    return filtered_dict
