import pandas as pd
from sklearn.metrics import confusion_matrix
import numpy as np
from sklearn.model_selection import cross_val_predict
from abc import ABC, abstractmethod

from src.ai_module.utils.dataset import stratified_sample
from src.common.config import BaseAIModelConfig


class AiModel(ABC):

    def __init__(self, num_class: int) -> None:
        self.n_class = num_class

    @abstractmethod
    def train(self, df : pd.DataFrame) -> np.ndarray:
        pass
    
    @abstractmethod
    def evaluate(self, row: pd.DataFrame) -> int:
        pass

    def sample_data(self, df: pd.DataFrame):
        df = stratified_sample(df, 10000, self.n_class)
        x_matrix = df.drop('label', axis=1) 
        y_vector = df['label']
        return x_matrix,y_vector




class ScikitLearnAIModel(AiModel, ABC):

    def __init__(self, config: BaseAIModelConfig, model) -> None:
        super().__init__(config.num_class)
        self.model = model(**config.model_dump())
    
    def train(self, df : pd.DataFrame) -> np.ndarray:
        x_matrix, y_vector = self.sample_data(df)
        predicted = cross_val_predict(self.model, x_matrix, y_vector, cv=5)
        return confusion_matrix(y_vector, predicted)
    
    def evaluate(self, row: pd.DataFrame) -> int:
        return self.model.predict(row)[0]
    