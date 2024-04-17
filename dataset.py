import pandas as pd
from sklearn.model_selection import train_test_split
import networkx as nx
from graph import create_graph, add_metrics

class Dataset:
    def __init__(self, data_path) -> None:
        data = pd.read_excel(data_path)
        self.data = data[data['Action'] != "reset-both"]
        self.df = self.data.copy()
        self.graph = nx.Graph()

    def get_data(self) -> pd.DataFrame:
        return self.df
    
    def get_graph(self) -> nx.Graph:
        return self.graph

    def process_data(self) -> None:
        self.df['label'] = self.df['Action'].apply(lambda x: 1 if x == 'allow' else 0)
        self.df = self.df.drop('Action', axis=1)
        self.graph = create_graph(self.df, 'Source Port', 'Destination Port')
        self.df = add_metrics(self.df, self.graph)


    def split_data(self) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
        X = self.df.drop('label', axis=1) 
        y = self.df['label']
        return train_test_split(X, y, test_size=0.2)
    
    







