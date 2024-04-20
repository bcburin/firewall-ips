import re
from pathlib import Path
from typing import Callable


def create_dir_if_not_exists(f: Callable[..., Path]) -> Callable[..., Path]:
    def inner(*args, **kwargs) -> Path:
        path = f(*args, **kwargs)
        if not path.is_dir():
            path.mkdir(parents=True, exist_ok=True)
        return path

    return inner


def get_subdir_factory(subdir: str) -> Callable[[], Path]:
    @create_dir_if_not_exists
    def inner() -> Path:
        return get_project_dir() / subdir

    return inner


def get_project_dir() -> Path:
    current_dir = Path(__file__)
    return current_dir.parent.parent.parent


get_data_dir = get_subdir_factory('data')
get_config_dir = get_subdir_factory('config')
get_archive_dir = get_subdir_factory('archive')


def convert_str_camel_to_snake(s: str) -> str:
    s = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', s).lower()
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s).lower()


def convert_dict_keys_camel_to_snake(d):
    if isinstance(d, list):
        return [convert_dict_keys_camel_to_snake(i) if isinstance(i, (dict, list)) else i for i in d]
    return {convert_str_camel_to_snake(a):
            convert_dict_keys_camel_to_snake(b)
            if isinstance(b, (dict, list))
            else b for a, b in d.items()}


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
