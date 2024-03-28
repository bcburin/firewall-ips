import pandas as pd
import numpy as np
from graph import Net
from sklearn.model_selection import train_test_split
from typing import Tuple

class Dataset:
    def __init__(self, data_path) -> None:
        data = pd.read_excel(data_path)
        self.data = data[data['Action'] != "reset-both"]
        self.df = self.data.copy()
        self.one_hot_variables = ['Source Port', 'Destination Port',	'NAT Source Port',	'NAT Destination Port']
        self.net = Net(data, 'Source Port', 'Destination Port')
    
    def draw_net(self) -> None:
        self.net.draw()

    def process_data(self) -> None:
        self.df['label'] = self.df['Action'].apply(lambda x: 1 if x == 'allow' else 0)
        self.df = self.df.drop('Action', axis=1)
        self.net.create_graph()

    def split_data(self) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
        X = self.df.drop('label', axis=1) 
        y = self.df['label']
        return train_test_split(X, y, test_size=0.2, random_state=42)

    def add_common_neighbors(self):
        pass

    def add_jaccard_index(self):
        pass

    def add_salton_index():
        pass

    def add_sorensen_Index(self):
        pass

    def adar_index():
        pass

    def normalize_columns(self):
        pass





