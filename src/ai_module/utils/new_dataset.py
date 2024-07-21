import pandas as pd
import numpy as np
import os
import warnings
import json

from scipy import stats
from sklearn.preprocessing import MinMaxScaler


def prepare_data(df: pd.DataFrame, n_class : int = 2, k : int = 5000) -> pd.DataFrame:
    df = fix_data_type(df)
    df = drop_infinate_null(df)
    df = generate_multi_label(df)
    df = drop_unnecessary_column(df)
    df = stratified_sample(df, k, n_class)
    return df

def read_data(folder_path: str, num_class: int) -> pd.DataFrame:
    warnings.filterwarnings("ignore")
    final_data: pd.DataFrame = pd.DataFrame()
    for filename in os.listdir(folder_path):
        print(f"Iniciando a leitura do arquivo {filename}")
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            data = pd.read_csv(file_path, low_memory=False)
            data = prepare_data(data, num_class)
            if len(final_data) == 0:
                final_data = data
            else:
                final_data = pd.concat([final_data, data], ignore_index=True)

    final_data  = filter_outliers_zscore(final_data, num_class)
    final_data = normalize(final_data)
    return final_data


def stratified_sample(df: pd.DataFrame, k: int, n_classes: int) -> pd.DataFrame:
    df_sampled = pd.DataFrame()
    for i in range(n_classes):
        df_aux = df[df["Label"] == i]
        sample_size = min(k, len(df_aux))
        df_aux = df_aux.sample(n = sample_size)
        df_sampled = pd.concat([df_sampled, df_aux])
    return df_sampled

def drop_infinate_null(df: pd.DataFrame) -> pd.DataFrame:
    df = df.replace(["Infinity", "infinity"], np.inf)
    df = df.replace([np.inf, -np.inf], np.nan)
    df.dropna(inplace=True)
    return df

def drop_unnecessary_column(df: pd.DataFrame) -> pd.DataFrame:
    df.drop(columns="Timestamp", inplace=True)
    return df

def generate_binary_label(df: pd.DataFrame) -> pd.DataFrame:
    df["Label"] = df['Label'].apply(lambda x: 1 if x == 'Benign' else 0)
    return df

def generate_multi_label(df: pd.DataFrame) -> pd.DataFrame:
    with open('config/dataset.json', 'r') as file:
        config = json.load(file)
    mapping = config['mapping']
    df['Label'] = df['Label'].map(mapping) 
    return df

def fix_data_type(df: pd.DataFrame) -> pd.DataFrame:
    with open('config/dataset.json', 'r') as file:
        config = json.load(file)
    int_var = config['variables_type']['int']
    float_var = config['variables_type']['float']
    df = df[df['Dst Port'] != 'Dst Port']
    for var in int_var:
        df[var] = df[var].astype(int)
    for var in float_var:
        df[var] = df[var].astype(float)
    return df

def drop_constant_col(df: pd.DataFrame) -> pd.DataFrame:
    exclude_columns = ['Dst Port', 'Protocol', 'Flow Duration', 'Tot Fwd Pkts', 'Tot Bwd Pkts']
    variances = df.var(numeric_only=True)
    constant_columns = variances[variances == 0].index
    columns_to_drop = [col for col in constant_columns if col not in exclude_columns]
    df = df.drop(columns_to_drop, axis=1)
    return df

def drop_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    exclude_columns = ['Dst Port', 'Protocol', 'Flow Duration', 'Tot Fwd Pkts', 'Tot Bwd Pkts']
    duplicates = set()
    for i in range(0, len(df.columns)):
        col1 = df.columns[i]
        for j in range(i+1, len(df.columns)):
            col2 = df.columns[j]
            if(df[col1].equals(df[col2])):
                duplicates.add(col2)

    print (f"As colunas duplicadas são: {duplicates}")
    columns_to_drop = [col for col in duplicates if col not in exclude_columns]
    df = df.drop(columns_to_drop, axis=1)
    return df

def drop_correlated_col(df: pd.DataFrame) -> pd.DataFrame:
    exclude_columns = ['Dst Port', 'Protocol', 'Flow Duration', 'Tot Fwd Pkts', 'Tot Bwd Pkts']
    corr = df.corr(numeric_only=True)
    correlated_col = set()
    is_correlated = [True] * len(corr.columns)
    threshold = 0.90
    for i in range (len(corr.columns)):
        if(is_correlated[i]):
            for j in range(i):
                if (corr.iloc[i, j] >= threshold) and (is_correlated[j]):
                    colname = corr.columns[j]
                    is_correlated[j]=False
                    correlated_col.add(colname)
    
    columns_to_drop = [col for col in correlated_col if col not in exclude_columns]
    df = df.drop(columns_to_drop, axis=1)
    print (f"o tamanho do dataframe é {df.shape}")
    return df

def filter_outliers_zscore(data : pd.DataFrame, threshold: int) -> pd.DataFrame:
    z_scores = np.abs(stats.zscore(data))
    outlier_mask = (z_scores > threshold).any(axis=1)
    return data[~outlier_mask]

def normalize(df: pd.DataFrame) -> pd.DataFrame:
    columns = [col for col in df.columns if col != 'Label']
    min_max_scaler = MinMaxScaler().fit(df[columns])
    df[columns] = min_max_scaler.transform(df[columns])
    return df

def filter_col(df: pd.DataFrame, col: list[str]) -> pd.DataFrame:
    return df[col]