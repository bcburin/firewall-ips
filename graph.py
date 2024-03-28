import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

class Net:
    def __init__(self, df: pd.DataFrame, col1: str, col2: str) -> None:
        self.df = df
        self.graph = nx.Graph()
        self.col_source_node = col1
        self.col_destination_node = col2

    def get_nodes(self, col) -> list:
        port = []
        for node in self.df[col].unique():
            port.append(int(node))
        return port

    def add_nodes(self) -> None:
        node_set = set(self.get_nodes(self.col_source_node)) | set(self.get_nodes(self.col_destination_node))
        node_list = list(node_set)
        for node in node_list:
            self.graph.add_node(node)

    def add_edges(self) -> None:
        for index, row in self.df.iterrows():
            self.graph.add_edge(row[self.col_source_node], row[self.col_destination_node])

    def create_graph(self) -> None:
       self.add_nodes()
       self.add_edges()

    def draw(self) -> None:
        nx.draw(self.graph, with_labels=True, node_color='skyblue', font_weight='bold')
        plt.show()
