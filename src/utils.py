from pathlib import Path


def get_project_dir() -> Path:
    current_dir = Path(__file__)
    return current_dir.parent.parent


def get_data_dir() -> Path:
    return get_project_dir() / 'data'


def get_config_dir() -> Path:
    return get_project_dir() / 'config'


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
