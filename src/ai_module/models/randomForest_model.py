from sklearn.ensemble import RandomForestClassifier
import pandas as pd
from sklearn.metrics import confusion_matrix
import numpy as np
from sklearn.model_selection import cross_val_predict

from ai_model import AiModel
from dataset import stratified_sample


class RandomForestModel(AiModel):
    def __init__(self, n_estimator: int, criterion : str, min_sample_split: int, min_samples_leaf: int, 
                 bootstrap: bool, verbose: int, n_class) -> None:
        super().__init__()
        self.model = RandomForestClassifier(
            n_estimators=n_estimator,
            criterion=criterion,
            min_samples_split=min_sample_split,
            min_samples_leaf=min_samples_leaf,
            bootstrap=bootstrap,
            verbose=verbose
        )
        self.n_class = n_class

    def train(self, df : pd.DataFrame) -> np.ndarray:
        df = stratified_sample(df, 10000, self.n_class)
        X = df.drop('label', axis=1) 
        y = df['label']
        predicted = cross_val_predict(self.model, X, y, cv=5)
        return confusion_matrix(y, predicted)


    def evaluate(self, row: pd.DataFrame) -> int:
        return self.model.predict(row)[0]