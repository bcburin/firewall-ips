import re
from functools import cache
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


_path_vars = {
    '$root': get_project_dir(),
    '$data': get_data_dir(),
    '$config': get_config_dir(),
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
    s = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', s).lower()
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s).lower()


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
