from sklearn.linear_model import LogisticRegression
import pandas as pd
from sklearn.metrics import confusion_matrix
import numpy as np
from sklearn.model_selection import cross_val_predict

from src.ai_module.ai_model import AiModel


class LogisticRegressionClassifier(AiModel):
    def __init__(self, n_class: int, C: int) -> None:
        super().__init__(n_class)
        self.model = LogisticRegression(
            C=C
        )

    def train(self, df : pd.DataFrame) -> np.ndarray:
        X, y = self.sample_data(df)
        predicted = cross_val_predict(self.model, X, y, cv=5)
        return confusion_matrix(y, predicted)


    def evaluate(self, row: pd.DataFrame) -> int:
        return self.model.predict(row)[0]