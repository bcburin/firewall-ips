from datetime import datetime
from pathlib import Path
from threading import Lock
from typing import Generic, Iterable, Type

from src.common.config import CompressionToolOption, PersistenceConfig, ConfigurationManager
from src.common.persistence import PersistableObject, PersistableObjectType
from src.common.utils import LoadableSingleton


class VersionedObjectManager(Generic[PersistableObjectType], LoadableSingleton):
    _dt_format = "%Y-%m-%dT%H-%M-%S"

    def __init__(self, cls: Type[PersistableObject]):
        self._cls = cls
        self._suffix = cls.generate_hyphen_separated_name() + '.bytes'
        self._config: PersistenceConfig | None = None
        self._obj: PersistableObject | None = None
        self._obj_lock = Lock()
        self._repository_lock = Lock()
        super().__init__()

    def _load(self):
        self._config = ConfigurationManager().get_server_config().ai_module.persistence
        if self._config is None:
            return
        if not self.empty_repository and self._config.load_latest_on_start:
            with self._obj_lock:
                self._obj = self._read_savefile()

    def _loaded(self):
        with self._obj_lock:
            return self._config is not None and (
                    self._obj is not None or self.empty_repository or not self._config.load_latest_on_start)

    def load_latest_version(self):
        with self.load_guard(), self._obj_lock:
            self._obj = self._read_savefile()

    def load_version(self, dt: datetime | None):
        if dt is None:
            self.load_latest_version()
        with self.load_guard(), self._obj_lock:
            self._obj = self._read_savefile(dt)

    def load_new_version(self, obj: PersistableObject):
        if not isinstance(obj, self._cls):
            raise Exception()
        with self._obj_lock:
            self._obj = obj
        with self.load_guard(), self._repository_lock:
            # remove oldest savefiles if max is reached
            savefile_paths = self._get_savefiles_dict()
            while len(savefile_paths) >= self._config.max_saved_models:
                dt = min(savefile_paths.keys())
                savefile_paths[dt].unlink()
                del savefile_paths[dt]
            # write new savefile
            self._write_savefile(obj)

    def get_loaded_version(self):
        with self._obj_lock:
            return self._obj

    def delete_version(self, dt: datetime):
        with self.load_guard(), self._repository_lock:
            self._delete_savefile(dt)

    def delete_all_versions(self):
        with self.load_guard(), self._repository_lock:
            self._delete_all_savefiles()

    def _write_savefile(self, obj: PersistableObject, dt: datetime | None = None):
        if dt is None:
            dt = datetime.now()
        savefile_path = self._config.resolved_directory / self._get_savefile_name(dt)
        obj.save_to_file(filepath=savefile_path)
        if self._config.compression and self._config.compression.enable:
            compression_tool = self._config.compression.resolved_tool
            compression_tool.compress(filepath=savefile_path)
            savefile_path.unlink()

    def _read_savefile(self, dt: datetime | None = None) -> PersistableObject:
        savefile_paths = self._get_savefiles_dict()
        if not savefile_paths:
            raise FileNotFoundError()
        if dt is None:
            # read most recent saved file, if no date is given
            dt = max(savefile_paths.keys())
        savefile_path = savefile_paths.get(dt)
        if savefile_path is None:
            raise FileNotFoundError()
        if self._is_compressed_savefile(savefile_path):
            compression_tool = CompressionToolOption.get_tool_implementation(savefile_path.suffix[1:])
            extracted_savefile = Path(savefile_path.parent) / savefile_path.stem
            compression_tool.decompress(savefile_path, output_filepath=extracted_savefile)
            obj = self._cls.load_from_file(extracted_savefile)
            extracted_savefile.unlink()
            return obj
        return self._cls.load_from_file(savefile_path)

    def _get_savefile_name(self, dt: datetime):
        return f"{dt.strftime(self._dt_format)}_{self._suffix}"

    def _delete_savefile(self, dt: datetime):
        path = self._config.resolved_directory / self._get_savefile_name(dt)
        if not self._is_savefile(path):
            raise FileNotFoundError()
        path.unlink()

    def _delete_all_savefiles(self):
        for path in self._iter_savefiles():
            path.unlink()

    def _is_savefile(self, path: Path):
        if not path.exists() or not path.is_file():
            return False
        if path.name.endswith(self._suffix):
            return True
        if self._is_compressed_savefile(path):
            return True
        return False

    def _is_compressed_savefile(self, path: Path):
        for compression_tool_option in CompressionToolOption:
            cto_suffix = '.' + compression_tool_option.value
            if path.name.endswith(self._suffix + cto_suffix):
                return True
        return False

    def _iter_savefiles(self) -> Iterable[Path]:
        for path in self._config.resolved_directory.iterdir():
            if not self._is_savefile(path):
                continue
            yield path

    def _get_savefiles_dict(self) -> dict[datetime, Path]:
        saved_obj_paths = dict()
        for path in self._iter_savefiles():
            dt_str, _ = path.name.split('_')
            dt = datetime.strptime(dt_str, self._dt_format)
            saved_obj_paths[dt] = path
        return saved_obj_paths

    @property
    def empty_repository(self) -> bool:
        with self._repository_lock:
            for _ in self._iter_savefiles():
                return False
        return True
