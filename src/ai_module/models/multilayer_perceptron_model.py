from sklearn.neural_network import MLPClassifier
import pandas as pd
from sklearn.metrics import confusion_matrix
import numpy as np
from sklearn.model_selection import cross_val_predict

from src.ai_module.ai_model import AiModel


class MultiLayerPerceptron(AiModel):
    def __init__(self, n_class: int, hidden_layer_size : int, activation: str, solver: str,
                 learning_rate: str, momentum: int, early_stop: bool) -> None:
        super().__init__(n_class)
        self.model = MLPClassifier(
            hidden_layer_sizes=hidden_layer_size,
            activation= activation, 
            solver= solver,
            learning_rate=learning_rate,
            momentum=momentum, 
            early_stopping= early_stop
        )

    def train(self, df : pd.DataFrame) -> np.ndarray:
        X, y = self.sample_data(df)
        predicted = cross_val_predict(self.model, X, y, cv=5)
        return confusion_matrix(y, predicted)


    def evaluate(self, row: pd.DataFrame) -> int:
        return self.model.predict(row)[0]