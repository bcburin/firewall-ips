import pandas as pd
from sklearn.model_selection import train_test_split
from dataset import prepare_data
from models.lightgbm_module import LightgbmModule
import numpy as np


if __name__ == "__main__":
    data_path = "C:/Users/jpcar/OneDrive/Documentos/Área de Trabalho/IME/Profissional/Nono periodo/PFC/code/Firewall-Rules-Predictions/data/log.xlsx"
    data = pd.read_excel(data_path)
    df =  prepare_data(data)
    train_df, test_df = train_test_split(df, test_size=0.05, random_state=42)
    ai_module = LightgbmModule(num_class=3, boosting_type='gbdt',objective='multiclass',num_leaves=31, metric='multi_error',
                                learning_rate=0.05, n_estimators=100, max_depth=-1, feature_fraction=0.9, bagging_fraction=0.8, bagging_freq=5, verbose=-1)
    cm = ai_module.train(train_df)
    print(cm)
    ground_truth = test_df['label']
    test_df = test_df.drop('label', axis=1) 
    predictions = ai_module.evaluate(test_df.iloc[[0]])
    print(predictions, ground_truth.iloc[0])
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