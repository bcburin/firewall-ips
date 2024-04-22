from lightgbm import LGBMClassifier
import pandas as pd
from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score
import numpy as np

from ai_module import AiModule
from dataset import split_data

class LightgbmModule(AiModule):

    def __init__(self, num_leaves, learning_rate, n_estimators, max_depth, feature_fraction, bagging_fraction, bagging_freq) -> None:
        super().__init__()
        self.model = LGBMClassifier(
            num_class=1,
            boosting_type='gbdt',
            num_leaves=num_leaves,
            learning_rate=learning_rate,
            n_estimators=n_estimators,
            max_depth=max_depth,
            feature_fraction=feature_fraction,
            bagging_fraction=bagging_fraction,
            bagging_freq=bagging_freq,
            verbose=-1
        )

    def train(self, df : pd.DataFrame) -> np.ndarray:
        X_train, X_test, y_train, y_test = split_data(df=df)
        self.model.fit(X_train, y_train)
        y_pred = self.model.predict(X_test)
        cm = confusion_matrix(y_test, y_pred)
        return cm