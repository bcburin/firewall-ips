import pandas as pd

from dataset import prepare_data
from models.lightgbm_module import LightgbmModule


if __name__ == "__main__":
    data_path = "C:/Users/jpcar/OneDrive/Documentos/Área de Trabalho/IME/Profissional/Nono periodo/PFC/code/Firewall-Rules-Predictions/data/log.xlsx"
    data = pd.read_excel(data_path)
    df =  prepare_data(data)
    ai_module = LightgbmModule(num_leaves=31, learning_rate=0.05, n_estimators=100, max_depth=-1,
                                feature_fraction=0.9, bagging_fraction=0.8, bagging_freq=5)
    cm = ai_module.train(df)
    print(cm)