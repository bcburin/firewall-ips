import sys
import os


import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np


from src.ai_module.utils.dataset import prepare_data
from src.ai_module.models.lightgbm_model import LightgbmModel
from src.ai_module.models.randomForest_model import RandomForestModel
from src.ai_module.ai_module import AiModule
 

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
    data_path = "C:/Users/jpcar/OneDrive/Documentos/Área de Trabalho/IME/Profissional/Nono periodo/PFC/code/Firewall-Rules-Predictions/data/log.xlsx"
    data = pd.read_excel(data_path)
    df =  prepare_data(data)
    ai_model = LightgbmModel(num_class=3, boosting_type='gbdt',objective='multiclass',num_leaves=31,
                                learning_rate=0.05, n_estimators=100, max_depth=-1, verbose=-1)
    
    ai_module = AiModule(ai_model)
    cm = ai_module.train(df.copy())
    print_results(cm)
    ai_model = RandomForestModel(n_estimator=100,criterion="log_loss", min_sample_split=2, min_samples_leaf=1,
                                 bootstrap=True, verbose=0, n_class=3)
    ai_module.change_model(ai_model)
    cm = ai_module.train(df.copy())
    print_results(cm)