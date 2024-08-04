import json

from sklearn.model_selection import train_test_split

from src.ai_module.utils.new_dataset import read_data, select_col,normalize, filter_col
from src.ai_module.ai_module import AiModule
from src.ai_module.models import create_estimator, create_models
from src.common.config import ConfigurationManager
from src.models.critical_rule import CriticalRuleBaseModel


def train_pipeline(data_path: str, model_path: str, dataset_config_path: str) -> None:
    with open(dataset_config_path, 'r') as file:
        config = json.load(file)
    model_training_config = ConfigurationManager().get_ai_models_training_config()
    df = read_data(data_path, config)
    df = normalize(df)
    df = filter_col(df, config)
    train_df, test_df = train_test_split(df, test_size=0.95, random_state=2, shuffle=True)
    estimator = create_estimator(df)
    ai_module = AiModule(estimator, model_training_config, train_df)
    ai_module.create_ensemble(train_df)
    ai_module.train(train_df)
    ai_module.evaluate(test_df)
    ai_module.save_model(model_path) 
    return ai_module.ensemble_model

def test_pipeline(data_path: str, model_path: str, dataset_config_path: str) -> None:
    with open(dataset_config_path, 'r') as file:
        config = json.load(file)
    model_training_config = ConfigurationManager().get_ai_models_training_config()
    df = read_data(data_path, config)
    df = normalize(df)
    estimator = None
    ai_module = AiModule(estimator, model_training_config, df)
    ai_module.change_model(model_path)
    df = select_col(df, ai_module.columns)
    ai_module.evaluate(df)

def create_rules_pipeline(data_path: str, model_path: str, dataset_config_path: str) -> list[CriticalRuleBaseModel]:
    with open(dataset_config_path, 'r') as file:
        config = json.load(file)
    model_training_config = ConfigurationManager().get_ai_models_training_config()
    df = read_data(data_path, config)
    estimator = None
    ai_module = AiModule(estimator, model_training_config, df)
    ai_module.change_model(model_path)
    df = select_col(df, ai_module.columns)
    if 'Label' in df.columns:
        df = df.drop(['Label'], axis=1)
    rules = ai_module.evaluate_package(df, config)
    print(rules)
    return rules

def train_and_get_metrics_pipeline(data_path: str, model_path: str, dataset_config_path: str) -> None:
    with open(dataset_config_path, 'r') as file:
        config = json.load(file)
    model_training_config = ConfigurationManager().get_ai_models_training_config()
    df = read_data(data_path, config)
    df = normalize(df)
    df = filter_col(df, config)
    train_df, test_df = train_test_split(df, test_size=0.95, random_state=2, shuffle=True)
    estimator = create_models(df)
    ai_module = AiModule(estimator, model_training_config, train_df)
    ai_module.ensemble_model = estimator
    ai_module.train(train_df)
    ai_module.evaluate(test_df)
    ai_module.shap_metrics(train_df, test_df, "logisticregression")
