import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm
import math


def get_nodes(df: pd.DataFrame, col : str) -> list:
    port = []
    for node in df[col].unique():
        port.append(int(node))
    return port

def add_nodes(graph : nx.Graph, df : pd.DataFrame, col_source_node : str, col_destination_node : str) -> None:
    node_set = set(get_nodes(df, col_source_node)) | set(get_nodes(df, col_destination_node))
    node_list = list(node_set)
    for node in node_list:
        graph.add_node(node)

def add_edges(graph : nx.Graph, df : pd.DataFrame, col_source_node : str, col_destination_node : str) -> None:
    for index, row in df.iterrows():
        graph.add_edge(row[col_source_node], row[col_destination_node])

def create_graph(df: pd.DataFrame, col_source_node : str, col_destination_node : str) -> nx.Graph:
    graph = nx.Graph()
    add_nodes(graph, df, col_source_node, col_destination_node)
    add_edges(graph, df, col_source_node, col_destination_node)
    return graph


def get_common_neighbors(graph : nx.Graph, node1: int, node2: int) -> int:
    neighbor1 = sorted(list(graph.neighbors(node1)))
    neighbor2 = sorted(list(graph.neighbors(node2)))
    common_neighbor = []
    p1 = 0
    p2 = 0
    while p1 < len(neighbor1) and p2 <len(neighbor2):
        if neighbor1[p1] == neighbor2[p2]:
            common_neighbor.append(neighbor1[p1])
            p1 += 1
            p2 += 1
        elif neighbor1[p1] > neighbor2[p2]:
            p2 += 1
        else:
            p1 += 1
    return len(common_neighbor)

def get_union_neigbors(graph : nx.Graph, node1: int, node2: int) -> int:
    neighbor1 = sorted(list(graph.neighbors(node1)))
    neighbor2 = sorted(list(graph.neighbors(node2)))
    set1 = set(neighbor1)
    set2 = set(neighbor2)
    union_neigbors =  list(set1.union(set2))
    return len(union_neigbors)

def get_neigbors(graph : nx.Graph, node1: int) -> int:
    return len(list(graph.neighbors(node1)))     

def add_metrics(df : pd.DataFrame, graph: nx.Graph) -> pd.DataFrame:
    new_dataframe = []
    with tqdm(total= len(df)) as pbar:
        for index, row in df.iterrows():
            n_common = get_common_neighbors(graph, row['Source Port'], row['Destination Port'])
            n_union = get_union_neigbors(graph, row['Source Port'], row['Destination Port'])
            n_neigbors_source = get_neigbors(graph, row['Source Port'])
            n_neigbors_dest = get_neigbors(graph, row['Destination Port'])
            jaccard_index = n_common/n_union
            salton_index = n_common/math.sqrt(n_neigbors_dest * n_neigbors_source)
            sorosen_index = n_common/(n_neigbors_source + n_neigbors_dest)
            new_dataframe.append([n_common, jaccard_index, salton_index, sorosen_index])
            pbar.update(1)
    extra_df = pd.DataFrame(new_dataframe, columns=['common neighbors', 'jaccard index', 'salton index', 'sorosen index'])
    df = pd.concat([df, extra_df], axis=1)
    return df

