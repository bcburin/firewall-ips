import pickle
from threading import Lock
from typing import Any

from pandas import DataFrame, Series
from sklearn.ensemble import VotingClassifier
from sklearn.metrics import classification_report, confusion_matrix

from src.ai_module.utils.estimator import create_ensamble
from src.common.config import ConfigurationManager
from src.common.persistence import PersistableObject


class EnsembleModel(PersistableObject):
    def __init__(self):
        self._models_config = ConfigurationManager().get_ai_models_training_config()
        self._ensemble_model: VotingClassifier | None = None
        self._lock = Lock()
        self._ensamble_is_trained: bool = False

    def _load(self, model_bytes: bytes) -> None:
        with self._lock:
            self._ensemble_model, self.columns = pickle.loads(model_bytes)

    def _dump(self) -> bytes:
        with self._lock:
            if self._ensemble_model is None:
                raise RuntimeError()
            return pickle.dumps([self._ensemble_model, self.columns])

    def train(self, df_training: DataFrame):
        with self._lock:
            self._ensemble_model = create_ensamble(models_config=self._models_config, df=df_training)
            x_train = df_training.drop('Label', axis=1)
            y_train = df_training['Label']
            self._ensemble_model.fit(x_train, y_train)
            self._ensamble_is_trained = True

    def predict(self, row: Series):
        if not self._ensamble_is_trained:
            raise RuntimeError()
        with self._lock:
            return self._ensemble_model.predict(row)

    def evaluate(self, df_test: DataFrame) -> tuple[str | dict, Any]:
        if not self._ensamble_is_trained:
            raise RuntimeError()
        with self._lock:
            x_test = df_test.drop('Label', axis=1)
            y_test = df_test['Label']
            y_pred = self._ensemble_model.predict(x_test)
            return (
                classification_report(y_test, y_pred),
                confusion_matrix(y_test, y_pred)
            )
