from lightgbm import LGBMClassifier
import pandas as pd
from sklearn.metrics import confusion_matrix
import numpy as np
from sklearn.model_selection import cross_val_predict

from ai_model import AiModel
class LightgbmModel(AiModel):

    def __init__(self, objective: str, num_class : int, metric: str, boosting_type: str, num_leaves: int, learning_rate: float,
                 n_estimators: int, max_depth: int, feature_fraction : float, bagging_fraction: float, bagging_freq: int, verbose: int) -> None:
        super().__init__()
        self.model = LGBMClassifier(
            objective = objective,
            num_class=num_class,
            metric = metric,
            boosting_type=boosting_type,
            num_leaves=num_leaves,
            learning_rate=learning_rate,
            n_estimators=n_estimators,
            max_depth=max_depth,
            feature_fraction=feature_fraction,
            bagging_fraction=bagging_fraction,
            bagging_freq=bagging_freq,
            verbose=verbose
        )

    def train(self, df : pd.DataFrame) -> np.ndarray:
        X = df.drop('label', axis=1) 
        y = df['label']
        predicted = cross_val_predict(self.model, X, y, cv=5)
        return confusion_matrix(y, predicted)


    def evaluate(self, row: pd.DataFrame) -> int:
        return self.model.predict(row)[0]