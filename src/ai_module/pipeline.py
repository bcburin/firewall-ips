import json

from sklearn.model_selection import train_test_split

from src.ai_module.utils.new_dataset import read_and_prepare_data, select_col, normalize, filter_col, \
    filter_outliers_zscore
from src.ai_module.ensamble_manager import EnsembleManager
from src.ai_module.models import create_estimator, create_models
from src.common.config import ConfigurationManager
from src.models.critical_rule import CriticalRuleBaseModel


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
    em.evaluate_loaded_ensemble(df_test=test_df)


def create_rules_pipeline(data_path: str, model_path: str, dataset_config_path: str) -> list[CriticalRuleBaseModel]:
    with open(dataset_config_path, 'r') as file:
        config = json.load(file)
    model_training_config = ConfigurationManager().get_ai_models_training_config()
    df = read_and_prepare_data(data_path)
    estimator = None
    ai_module = EnsembleManager(estimator, model_training_config, df)
    ai_module.change_model(model_path)
    df = select_col(df, ai_module.columns)
    if 'Label' in df.columns:
        df = df.drop(['Label'], axis=1)
    rules = ai_module.evaluate_package(df, config)
    print(rules)
    return rules

