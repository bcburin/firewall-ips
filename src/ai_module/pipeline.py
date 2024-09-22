import pandas as pd
from sklearn.model_selection import train_test_split

from src.ai_module.utils.new_dataset import read_and_prepare_data, normalize, filter_col, \
    filter_outliers_zscore
from src.ai_module.ensamble_manager import EnsembleManager
from src.common.config import ConfigurationManager


def train_pipeline():
    # get configuration files
    server_config = ConfigurationManager().get_server_config()
    # read and preprocess data
    data_path = server_config.ai_module.training.data.resolved_path
    df = read_and_prepare_data(data_path)
    df = filter_outliers_zscore(df)
    df = normalize(df)
    df = filter_col(df)
    # train and evaluate models
    train_df, test_df = train_test_split(df, test_size=0.95, random_state=2, shuffle=True)
    em = EnsembleManager()
    em.train_new_ensemble(df_training=train_df)
    model_result_info = em.evaluate_loaded_ensemble(df_test=test_df)
    create_static_rules_pipeline()


def create_static_rules_pipeline():
    server_config = ConfigurationManager().get_server_config()
    data_path = server_config.ai_module.training.data.resolved_path
    dataset_config = ConfigurationManager().get_dataset_config()
    df = read_and_prepare_data(data_path)
    em = EnsembleManager()
    em.create_rules(df, dataset_config)

