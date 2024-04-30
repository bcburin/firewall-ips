import math

import pandas as pd
from tqdm import tqdm
from sklearn.model_selection import train_test_split

from utils.graph import create_graph, get_common_neighbors_size, get_neighbors_size, get_union_neighbors_size


def prepare_label(df: pd.DataFrame) -> pd.DataFrame:
    df = df[df['Action'] != 'reset-both']
    df['label'] = df['Action'].apply(lambda x: 0 if x == 'allow' else (1 if x == 'deny' else 2))
    df = df.drop('Action', axis=1)
    return df.dropna()


def add_graph_metrics(df : pd.DataFrame, col1: int, col2: int) -> pd.DataFrame:
    graph = create_graph(df, col1, col2)
    new_dataframe = []
    with tqdm(total= len(df)) as pbar:
        for _, row in df.iterrows():
            n_common = get_common_neighbors_size(graph, row[col1], row[col2])
            n_union = get_union_neighbors_size(graph, row[col1], row[col2])
            n_neigbors_source = get_neighbors_size(graph, row[col1])
            n_neigbors_dest = get_neighbors_size(graph, row[col2])
            jaccard_index = n_common/max(n_union,1)
            salton_index = n_common/max(math.sqrt(n_neigbors_dest * n_neigbors_source),1)
            sorosen_index = n_common/max((n_neigbors_source + n_neigbors_dest),1)
            new_dataframe.append([n_common, jaccard_index, salton_index, sorosen_index])
            pbar.update(1)
    extra_df = pd.DataFrame(new_dataframe, columns=['common neighbors' + col1, 'jaccard index' + col1, 'salton index' + col1, 'sorosen index' + col1])
    df = pd.concat([df, extra_df.set_index(df.index)], axis=1)
    return df.drop([col1, col2], axis = 1)


def normalize_data(df : pd.DataFrame) -> pd.DataFrame:
    label = df['label']
    df = df.drop('label', axis=1)
    df = (df-df.mean())/df.std()
    df['label'] = label
    return df


def prepare_data(data : pd.DataFrame) -> pd.DataFrame:
    df = prepare_label(data)
    df['NAT translation source'] = df.apply(lambda row: row['Source Port'] == row['NAT Source Port'], axis=1)
    df['NAT translation destination'] = df.apply(lambda row:row['Destination Port'] == row['NAT Destination Port'], axis=1)
    df = add_graph_metrics(df, 'Source Port', 'Destination Port')
    df = add_graph_metrics(df, 'NAT Source Port', 'NAT Destination Port')
    df = normalize_data(df)
    return df


def split_data(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    X = df.drop('label', axis=1) 
    y = df['label']
    return train_test_split(X, y, test_size=0.2)


def stratified_sample(df: pd.DataFrame, k: int, n_classes: int) -> pd.DataFrame:
    df_sampled = pd.DataFrame()
    for i in range(n_classes):
        df_aux = df[df['label'] == i]
        df_aux = df_aux.sample(n = k)
        df_sampled = pd.concat([df_sampled, df_aux])
    return df_sampled

