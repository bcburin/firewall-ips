import pandas as pd

from dataset import prepare_data



if __name__ == "__main__":
    data_path = "C:/Users/jpcar/OneDrive/Documentos/Área de Trabalho/IME/Profissional/Nono periodo/PFC/code/Firewall-Rules-Predictions/data/log.xlsx"
    data = pd.read_excel(data_path)
    df =  prepare_data(data)