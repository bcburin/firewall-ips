import pandas as pd

from sklearn.model_selection import train_test_split

import numpy as np
from sklearn.ensemble import BaseEnsemble
from typing import Tuple


class AI:
    def __init__(self, model:  BaseEnsemble, n: int = 2) -> None:
        self.x_train = NotImplemented
        self.x_test = NotImplemented
        self.y_train = NotImplemented
        self.y_test = NotImplemented
        self.y_pred = NotImplemented
        self.model = model
        self.number_output = n


    def add_train_test_dataset(self, x_train : pd.DataFrame, x_test : pd.DataFrame, y_train : pd.Series, y_test : pd.Series) -> None:
        self.x_train = x_train
        self.x_test = x_test
        self.y_train = y_train.to_list()
        self.y_test = y_test.to_list()
        self.y_pred = NotImplemented
        

    def get_metrics(self) -> Tuple[float, np.ndarray, np.ndarray, np.ndarray]:
        confusion_matrix = np.zeros((self.number_output, self.number_output))
        for i in range(len(self.y_pred)):
            confusion_matrix[self.y_test[i], self.y_pred[i]] += 1
        precision = np.zeros(self.number_output)
        recall = np.zeros(self.number_output)
        f1_score = np.zeros(self.number_output)
        for i in range(self.number_output):
            precision[i] = confusion_matrix[i][i]/np.sum(confusion_matrix[i])
            recall[i] = confusion_matrix[i][i]/np.sum(confusion_matrix[:,i])
            f1_score[i] = (2 * precision[i] * recall[i])/(precision[i] + recall[i])
        accuracy = np.trace(confusion_matrix)/np.sum(confusion_matrix)
        return accuracy, precision, recall, f1_score


    def train(self) -> None:
        self.model.fit(self.x_train, self.y_train)

    def evaluate(self) -> None:
        self.y_pred = self.model.predict(self.x_test)
        

