from lightgbm import LGBMClassifier
import pandas as pd
from sklearn.metrics import confusion_matrix
import numpy as np
from sklearn.model_selection import cross_val_predict

from src.ai_module.ai_model import AiModel
from src.common.config import LightgbmConfig


class LightgbmModel(AiModel):
    def __init__(self, config: LightgbmConfig) -> None:
        super().__init__(config.num_class)
        self.model = LGBMClassifier(**config.dict())

    def train(self, df : pd.DataFrame) -> np.ndarray:
        X, y = self.sample_data(df)
        predicted = cross_val_predict(self.model, X, y, cv=5)
        return confusion_matrix(y, predicted)


    def evaluate(self, row: pd.DataFrame) -> int:
        return self.model.predict(row)[0]