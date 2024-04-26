import joblib

from lightgbm import LGBMClassifier
import pandas as pd
from sklearn.metrics import confusion_matrix
import numpy as np

from ai_module import AiModule
from dataset import split_data

class LightgbmModule(AiModule):

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
        X_train, X_test, y_train, y_test = split_data(df=df)
        self.model.fit(X_train, y_train)
        y_pred = self.model.predict(X_test)
        cm = confusion_matrix(y_test, y_pred)
        return cm
    
    def evaluate(self, row: pd.DataFrame) -> int:
        return self.model.predict(row)[0]
    
    def load(self) -> None:
        joblib.dump(self.model, 'model.pkl')

    def get(self) -> None:
        self.model = joblib.load('model.pkl')
        