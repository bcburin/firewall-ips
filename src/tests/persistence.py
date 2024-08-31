import pickle

from src.common.config import PersistenceConfig, ConfigurationManager
from src.services.persistence import VersionedObjectManager
from src.common.persistence import PersistableObject


class TClass(PersistableObject):
    def __init__(self, n: int = 0):
        super().__init__()
        self.n = n

    def _dump(self) -> bytes:
        return pickle.dumps(self.n)

    def _load(self, serialized_state: bytes):
        n = pickle.loads(serialized_state)
        self.n = n


class TClassVersionManager(VersionedObjectManager[TClass]):
    def __init__(self, persistence_config: PersistenceConfig = None):
        super().__init__(cls=TClass)

    def get_number(self) -> int:
        return self.get_loaded_version().n


if __name__ == '__main__':
    ConfigurationManager().load()
    tcm = TClassVersionManager(persistence_config=ConfigurationManager().get_server_config().ai_module.persistence)

    # test create, load and persist object
    tc = TClass(n=3)
    tcm.load_new_version(obj=tc)
    tc1 = tcm.get_loaded_version()
    print(tc1.n)

    # test load object from latest saved file
    tcm.load_latest_version()
    print(tcm.get_loaded_version().n)

    # test managers are singletons
    # tc = TestClass(n=5)
    # tcm.load_object(obj=tc)
    # tcm1 = TestClassLCManager()
    # print(tcm1.get_object().n)
