import pickle
from typing import List, Tuple
import json
import ast

import pandas as pd
import numpy as np
from sklearn.ensemble import VotingClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import GridSearchCV
from sklearn.base import BaseEstimator

from src.common.utils import filter_dict
from src.common.config import BaseAIModelConfig
from src.ai_module.models import select_hyperparameter


class AiModule():

    def __init__(self, list_models: List[Tuple[str, BaseEstimator]], config: BaseAIModelConfig, df: pd.DataFrame) -> None:
        self.config = config.model_dump()
        self.col = df.columns
        self.list_models = list_models
    
    def create_ensemble(self, df):
        for i, tupla in enumerate(self.list_models):
            name, model = tupla
            if name == "dt":
                continue
            self.config[name][0] = filter_dict(self.config[name][0], model.__init__)
            self.list_models[i] = (name, select_hyperparameter(model, self.config[name], df))
        self.ensemble_model = VotingClassifier(estimators=self.list_models, voting='soft')
    
    def _load(self, model_bytes: bytes) -> None:
        self.ensemble_model = pickle.loads(model_bytes)
        
    def _dump(self) -> bytes:
        return pickle.dumps(self.ensemble_model)     

    def train(self,  df : pd.DataFrame) -> np.ndarray:
        x_train = df.drop('Label', axis=1)
        y_train = df['Label']
        self.ensemble_model.fit(x_train, y_train)
    
    def predict(self, row: pd.DataFrame) -> int:
        return self.ensemble_model.predict(row)
    
    def evaluate(self, df : pd.DataFrame) -> None:
        x_test = df.drop('Label', axis=1)
        y_test = df['Label']
        y_pred = self.ensemble_model.predict(x_test)
        print(classification_report(y_test, y_pred))
        print(confusion_matrix(y_test, y_pred))
    
    def change_model(self, file_path, col_path) -> None:
        with open(file_path, 'rb') as file:
            model_byte = file.read()
        self._load(model_byte)
        with open(col_path, 'r') as file:
            list_col = file.read()
        self.col = ast.literal_eval(list_col)

    
    def save_model(self, file_path, col_path):
        model_byte = self._dump()
        column_list = self.col.to_list()
        with open(file_path, 'wb') as file:
            file.write(model_byte)
        with open(col_path, 'w') as file:
            json.dump(column_list, file)
    
