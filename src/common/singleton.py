from abc import abstractmethod
from contextlib import contextmanager
from threading import Lock

from src.common.exceptions.persistence import NotLoadedException
from src.common.utils import Singleton


class LoadableSingleton(metaclass=Singleton):
    def __init__(self):
        self.load_lock = Lock()

    @abstractmethod
    def _load(self):
        raise NotImplemented()

    @abstractmethod
    def _loaded(self):
        raise NotImplemented()

    @property
    def _not_loaded_exception(self) -> Exception:
        return NotLoadedException()

    def load(self):
        with self.load_lock:
            for _ in range(3):
                if self._loaded():
                    break
                self._load()

    @property
    def loaded(self) -> bool:
        with self.load_lock:
            return self._loaded()

    @contextmanager
    def load_guard(self):
        with self.load_lock:
            if not self._loaded():
                self._load()
                if not self._loaded():
                    raise self._not_loaded_exception
        yield
