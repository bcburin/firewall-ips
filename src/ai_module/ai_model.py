import pandas as pd
from sklearn.metrics import confusion_matrix
import numpy as np
from sklearn.model_selection import cross_val_predict
from abc import ABC, abstractmethod
from sklearn.model_selection import RandomizedSearchCV

from src.ai_module.utils.dataset import stratified_sample
from src.common.config import BaseAIModelConfig
from src.common.utils import filter_dict


class AiModel(ABC):

    def __init__(self, num_class: int) -> None:
        self.n_class = num_class

    @abstractmethod
    def train(self, df : pd.DataFrame) -> np.ndarray:
        pass
    
    @abstractmethod
    def evaluate(self, row: pd.DataFrame) -> int:
        pass

    def sample_data(self, df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
        df = stratified_sample(df, 10000, self.n_class)
        x_matrix = df.drop('label', axis=1) 
        y_vector = df['label']
        return x_matrix,y_vector




class ScikitLearnAIModel(AiModel, ABC):

    def __init__(self, config: BaseAIModelConfig, model) -> None:
        super().__init__(config.num_class)
        self.config = filter_dict(config.model_dump(), model.__init__)
        print(self.config)
        self.model = model()
    
    def train(self, df : pd.DataFrame) -> np.ndarray:
        x_matrix, y_vector = self.sample_data(df)
        random_search = RandomizedSearchCV(self.model, self.config, n_iter=2, cv=5)
        random_search.fit(x_matrix, y_vector)
        best_params = random_search.best_params_
        best_model = random_search.best_estimator_
        predicted = cross_val_predict(best_model, x_matrix, y_vector, cv=5)
        print(best_params)
        return confusion_matrix(y_vector, predicted)
    
    def evaluate(self, row: pd.DataFrame) -> int:
        return self.model.predict(row)[0]
    