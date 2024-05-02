from sklearn.ensemble import GradientBoostingClassifier
import pandas as pd
from sklearn.metrics import confusion_matrix
import numpy as np
from sklearn.model_selection import cross_val_predict

from src.ai_module.ai_model import AiModel


class Xgbbost(AiModel):
    def __init__(self, n_class: int, loss: str, learning_rate: float, n_estimator: int, subsample: float,
                 max_depth) -> None:
        super().__init__(n_class)
        self.model = GradientBoostingClassifier(
            loss = loss,
            learning_rate= learning_rate,
            n_estimators=n_estimator,
            subsample=subsample,
            max_depth=max_depth
        )

    def train(self, df : pd.DataFrame) -> np.ndarray:
        X, y = self.sample_data(df)
        predicted = cross_val_predict(self.model, X, y, cv=5)
        return confusion_matrix(y, predicted)


    def evaluate(self, row: pd.DataFrame) -> int:
        return self.model.predict(row)[0]