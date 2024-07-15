import pickle
from typing import List, Tuple

import pandas as pd
import numpy as np
from sklearn.ensemble import VotingClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import GridSearchCV
from sklearn.base import BaseEstimator

from src.common.utils import filter_dict
from src.common.config import BaseAIModelConfig


class AiModule():

    def __init__(self, list_models: List[Tuple[str, BaseEstimator]], config: BaseAIModelConfig, df: pd.DataFrame) -> None:
        self.config = config.model_dump()
        print(self.config)
        for i, tupla in enumerate(list_models):
            name, model = tupla
            if name == "dt":
                continue
            self.config[name][0] = filter_dict(self.config[name][0], model.__init__)
            #list_models[i] = (name, self.select_hyperparameter(model, self.config[name], df))
        self.ensemble_model = VotingClassifier(estimators=list_models, voting='soft')
    
    def _load(self, model_bytes: bytes) -> None:
        self.ensemble_model = pickle.loads(model_bytes)
        
    def _dump(self) -> bytes:
        return pickle.dumps(self.ensemble_model)     

    def train(self,  df : pd.DataFrame) -> np.ndarray:
        x_train = df.drop('Label', axis=1)
        y_train = df['Label']
        return self.ensemble_model.fit(x_train, y_train)
    
    def predict(self, row: pd.DataFrame) -> int:
        return self.ensemble_model.predict(row)
    
    def evaluate(self, df : pd.DataFrame) -> None:
        x_test = df.drop('Label', axis=1)
        y_test = df['Label']
        y_pred = self.ensemble_model.predict(x_test)
        print(classification_report(y_test, y_pred))
    
    def change_model(self, list_models) -> None:
        self.ensemble_model = list_models

    def select_hyperparameter(self, model: BaseEstimator, param_grid: dict, df: pd.DataFrame) -> BaseEstimator:
        x_train = df.drop('Label', axis=1)
        y_train = df['Label']
        grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=5, scoring='accuracy', verbose=2, n_jobs=-1)
        grid_search.fit(x_train, y_train)
        return grid_search.best_estimator_