import pandas as pd
from dataset import add_metrics, prepare_label



if __name__ == "__main__":
    data_path = "data/log.xlsx"
    data = pd.read_excel(data_path)
    df = prepare_label(data)
    df = add_metrics(df, 'Source Port', 'Destination Port')


