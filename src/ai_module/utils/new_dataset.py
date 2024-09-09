from pathlib import Path
from typing import Iterable

import pandas as pd
import numpy as np
import os
import warnings
from collections import Counter

from scipy import stats
from sklearn.preprocessing import MinMaxScaler
from sklearn.utils import class_weight
from sqlalchemy.testing.plugin.plugin_base import logging

from src.common.config import ConfigurationManager, DatasetConfig, ColumnType


def prepare_data(df: pd.DataFrame) -> pd.DataFrame:
    config = ConfigurationManager().get_dataset_config()
    df = fix_data_type(df, config)
    df = drop_infinate_null(df)
    df = generate_multi_label(df, config)
    df = drop_unnecessary_column(df)
    df = stratified_sample(df, config.sample_size, config.num_classes)
    return df


def read_and_prepare_data(data_path: Path) -> pd.DataFrame:
    warnings.filterwarnings("ignore")
    final_data: pd.DataFrame = pd.DataFrame()
    if data_path.is_dir():
        for file_path in data_path.iterdir():
            #logging.info(f"Reading file at {file_path}")
            if not file_path.is_file():
                continue
            data = pd.read_csv(file_path, low_memory=False)
            data = prepare_data(data)
            if len(final_data) == 0:
                final_data = data
            else:
                final_data = pd.concat([final_data, data], ignore_index=True)
    else:
        data = pd.read_csv(data_path, low_memory=False)
        final_data = prepare_data(data)
    return final_data


def stratified_sample(df: pd.DataFrame, k: int, n_classes: int) -> pd.DataFrame:
    df_sampled = pd.DataFrame()
    for i in range(n_classes):
        df_aux = df[df["Label"] == i]
        sample_size = min(k, len(df_aux))
        if i == 0:
            sample_size = int(sample_size/5)
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
    df["Label"] = df['Label'].apply(lambda x: 0 if x == 'Benign' else 1)
    return df


def generate_multi_label(df: pd.DataFrame, config: DatasetConfig) -> pd.DataFrame:
    mapping = { mapping.label: mapping.value for mapping in config.mapping }
    df['Label'] = df['Label'].map(mapping) 
    return df


def fix_data_type(df: pd.DataFrame, config : DatasetConfig) -> pd.DataFrame:
    columns = config.columns
    for col in columns:
        col_name = col.name
        col_type = col.type
        if col_type == ColumnType.FLOAT:
            df[col_name] = pd.to_numeric(df[col_name], errors='coerce')
        elif col_type == ColumnType.INT:
            df[col_name] = pd.to_numeric(df[col_name], errors='coerce', downcast='integer')
    return df


def remove_columns(df: pd.DataFrame, col_names: Iterable[str]):
    not_excluded_columns = ConfigurationManager().get_dataset_config().columns_not_to_remove
    columns_to_drop = [col for col in col_names if col not in not_excluded_columns]
    df = df.drop(columns_to_drop, axis=1)
    return df


def drop_constant_col(df: pd.DataFrame) -> pd.DataFrame:
    variances = df.var(numeric_only=True)
    constant_columns = variances[variances == 0].index
    return remove_columns(df, constant_columns)


def drop_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    duplicates = set()
    for i in range(0, len(df.columns)):
        col1 = df.columns[i]
        for j in range(i+1, len(df.columns)):
            col2 = df.columns[j]
            if df[col1].equals(df[col2]):
                duplicates.add(col2)
    #logging.info(f"Duplicate columns: {duplicates}")
    return remove_columns(df, duplicates)


def drop_correlated_col(df: pd.DataFrame) -> pd.DataFrame:
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
    return remove_columns(df, correlated_col)


def filter_outliers_zscore(data : pd.DataFrame) -> pd.DataFrame:
    threshold = ConfigurationManager().get_dataset_config().num_classes
    z_scores = np.abs(stats.zscore(data))
    outlier_mask = (z_scores > threshold).any(axis=1)
    return data[~outlier_mask]


def normalize(df: pd.DataFrame) -> pd.DataFrame:
    columns = [col for col in df.columns if col != 'Label']
    min_max_scaler = MinMaxScaler().fit(df[columns])
    df[columns] = min_max_scaler.transform(df[columns])
    return df


def select_col(df: pd.DataFrame, col: list[str]) -> pd.DataFrame:
    return df[col]


def filter_col(df: pd.DataFrame) -> pd.DataFrame:
    df = drop_constant_col(df)
    df = drop_duplicates(df)
    df = drop_correlated_col(df)
    return df


def calculate_weights(df: pd.DataFrame):
    order_label_list = np.unique(df['Label'])
    class_weights = class_weight.compute_class_weight(
        'balanced', classes=order_label_list, y=df['Label'].values)
    class_weights = { k: v for k,v in enumerate(class_weights) }
    return class_weights
