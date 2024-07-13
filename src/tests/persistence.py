import pickle

from src.common.config import PersistenceConfig, ConfigurationManager
from src.services.persistence import PersistableObjectLifeCycleManager
from src.common.persistence import PersistableObject


class TestClass(PersistableObject):
    def __init__(self, n: int = 0):
        super().__init__()
        self.n = n

    def _dump(self) -> bytes:
        return pickle.dumps(self.n)

    def _load(self, serialized_state: bytes):
        n = pickle.loads(serialized_state)
        self.n = n


class TestClassLCManager(PersistableObjectLifeCycleManager[TestClass]):
    def __init__(self, persistence_config: PersistenceConfig = None):
        super().__init__(persistable_object_cls=TestClass, persistence_config=persistence_config)

    def get_number(self) -> int:
        return self.get_object().n


if __name__ == '__main__':
    tcm = TestClassLCManager(persistence_config=ConfigurationManager().get_server_config().ai_module.persistence)

    # test create, load and persist object
    tc = TestClass(n=3)
    tcm.load_object(obj=tc)
    tcm.persist_current_object()

    # test load object from latest saved file
    # tcm.load_object_from_latest_file()
    # print(tcm.get_object().n)

    # test managers are singletons
    # tc = TestClass(n=5)
    # tcm.load_object(obj=tc)
    # tcm1 = TestClassLCManager()
    # print(tcm1.get_object().n)
