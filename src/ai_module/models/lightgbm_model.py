from lightgbm import LGBMClassifier
import pandas as pd
from sklearn.metrics import confusion_matrix
import numpy as np
from sklearn.model_selection import cross_val_predict

from ai_model import AiModel
from dataset import stratified_sample


class LightgbmModel(AiModel):
    def __init__(self, objective: str, num_class : int, boosting_type: str, num_leaves: int, learning_rate: float,
                 n_estimators: int, max_depth: int, verbose: int) -> None:
        super().__init__()
        self.model = LGBMClassifier(
            objective = objective,
            num_class=num_class,
            boosting_type=boosting_type,
            num_leaves=num_leaves,
            learning_rate=learning_rate,
            n_estimators=n_estimators,
            max_depth=max_depth,
            verbose=verbose
        )
        self.n_class = num_class

    def train(self, df : pd.DataFrame) -> np.ndarray:
        df = stratified_sample(df, 10000, self.n_class)
        X = df.drop('label', axis=1) 
        y = df['label']
        predicted = cross_val_predict(self.model, X, y, cv=5)
        return confusion_matrix(y, predicted)


    def evaluate(self, row: pd.DataFrame) -> int:
        return self.model.predict(row)[0]