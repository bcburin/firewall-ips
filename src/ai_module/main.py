import sys
import os


import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np


from src.ai_module.utils.dataset import prepare_data
from src.ai_module.models.lightgbm_model import LightgbmModel
from src.ai_module.models.randomForest_model import RandomForestModel
from src.ai_module.models.gradient_boost_model import Xgbbost
from src.ai_module.models.svm_model import SVM
from src.ai_module.models.logistic_regression_model import LogisticRegressionClassifier
from src.ai_module.models.multilayer_perceptron_model import MultiLayerPerceptron
from src.ai_module.ai_module import AiModule
from src.common.config import AIModelsTrainingConfig, ServerConfig


def print_results(cm: np.ndarray) -> None:
    print(cm)
    precision = np.zeros(3)
    recall = np.zeros(3)
    f1_score = np.zeros(3)
    for i in range(3):
        precision[i] = cm[i][i]/np.sum(cm[i])
        recall[i] = cm[i][i]/np.sum(cm[:,i])
        f1_score[i] = (2 * precision[i] * recall[i])/(precision[i] + recall[i])
    print(f1_score)
    print(recall)
    print(precision)


if __name__ == "__main__":
    server_config: ServerConfig = ServerConfig.get()
    data_path = server_config.ai_model.training.data.resolved_path
    data = pd.read_excel(data_path)
    df = prepare_data(data)
    model_training_config: AIModelsTrainingConfig = AIModelsTrainingConfig.get()
    ai_model = LightgbmModel(config=model_training_config.lightgbm[0])
    
    ai_module = AiModule(ai_model)
    cm = ai_module.train(df.copy())
    print_results(cm)
    ai_model = RandomForestModel(n_estimator=100,criterion="log_loss", min_sample_split=2, min_samples_leaf=1,
                                 bootstrap=True, verbose=0, n_class=3)
    ai_module.change_model(ai_model)
    cm = ai_module.train(df.copy())
    print_results(cm)
    ai_model = Xgbbost(n_class=3, loss="log_loss", learning_rate= 0.1, n_estimator=100,subsample=0.5, max_depth=10)
    ai_module.change_model(ai_model)
    cm = ai_module.train(df.copy())
    print_results(cm)
    ai_model = SVM(n_class=3, C = 1, kernel="linear", degree=3)
    ai_module.change_model(ai_model)
    cm = ai_module.train(df.copy())
    print_results(cm)
    ai_model = MultiLayerPerceptron(n_class=3, hidden_layer_size=100, activation='relu', solver='adam',
                                     learning_rate='adaptive', momentum=0.9, early_stop=True)
    ai_module.change_model(ai_model)
    cm = ai_module.train(df.copy())
    print_results(cm)