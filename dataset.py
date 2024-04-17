import math

import pandas as pd
from tqdm import tqdm
from sklearn.model_selection import train_test_split

from graph import create_graph, get_common_neighbors, get_neigbors, get_union_neigbors


def prepare_label(data: pd.DataFrame) -> pd.DataFrame:
    df = data[data['Action'] != "reset-both"]
    df['label'] = df['Action'].apply(lambda x: 1 if x == 'allow' else 0)
    df = df.drop('Action', axis=1)
    return df


def add_metrics(df : pd.DataFrame, col1: int, col2: int) -> pd.DataFrame:
    graph = create_graph(df, col1, col2)
    new_dataframe = []
    with tqdm(total= len(df)) as pbar:
        for _, row in df.iterrows():
            n_common = get_common_neighbors(graph, row[col1], row[col2])
            n_union = get_union_neigbors(graph, row[col1], row[col2])
            n_neigbors_source = get_neigbors(graph, row[col1])
            n_neigbors_dest = get_neigbors(graph, row[col2])
            jaccard_index = n_common/n_union
            salton_index = n_common/math.sqrt(n_neigbors_dest * n_neigbors_source)
            sorosen_index = n_common/(n_neigbors_source + n_neigbors_dest)
            new_dataframe.append([n_common, jaccard_index, salton_index, sorosen_index])
            pbar.update(1)
    extra_df = pd.DataFrame(new_dataframe, columns=['common neighbors' + col1, 'jaccard index' + col1, 'salton index' + col1, 'sorosen index' + col1])
    df = pd.concat([df, extra_df], axis=1)
    return df.drop([col1, col2], axis = 1)


def normalize_data():
    pass


def split_data(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    X = df.drop('label', axis=1) 
    y = df['label']
    return train_test_split(X, y, test_size=0.2)









