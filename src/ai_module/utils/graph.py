import networkx as nx
import pandas as pd
import numpy as np


def add_nodes(df: pd.DataFrame, col : str, graph : nx.DiGraph) -> None:
    for node in df[col].unique():
        if np.isnan(node):
            continue
        graph.add_node(node)


def add_edges(graph : nx.DiGraph, df : pd.DataFrame, col_source_node : str, col_destination_node : str) -> None:
    for _, row in df.iterrows():
        graph.add_edge(row[col_source_node], row[col_destination_node])


def create_graph(df: pd.DataFrame, col_source_node : str, col_destination_node : str) -> nx.DiGraph:
    graph = nx.DiGraph()
    add_nodes(df, col_source_node, graph)
    add_nodes(df, col_destination_node, graph)
    add_edges(graph, df, col_source_node, col_destination_node)
    return graph


def get_common_neighbors_size(graph : nx.DiGraph, node1: int, node2: int) -> int:
    neighbor1 = graph.neighbors(node1)
    neighbor2 = graph.neighbors(node2)
    if not neighbor1 or not neighbor2:
        return 0
    neighbor1 = sorted(list(neighbor1))
    neighbor2 = sorted(list(neighbor2))
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


def get_union_neighbors_size(graph : nx.DiGraph, node1: int, node2: int) -> int:
    neighbor1 = sorted(list(graph.neighbors(node1)))
    neighbor2 = sorted(list(graph.neighbors(node2)))
    set1 = set(neighbor1)
    set2 = set(neighbor2)
    union_neigbors =  list(set1.union(set2))
    return len(union_neigbors)


def get_neighbors_size(graph : nx.DiGraph, node1: int) -> int:
    return len(list(graph.neighbors(node1)))     