import json

from sklearn.model_selection import train_test_split

from src.ai_module.utils.new_dataset import read_data, select_col,normalize, filter_col
from src.ai_module.ai_module import AiModule
from src.ai_module.models import create_estimator
from src.common.config import AIModelsTrainingConfig
from src.models.critical_rule import CriticalRuleBaseModel


def train_pipeline(data_path: str, model_path: str, columns_path: str) -> None:
    model_training_config: AIModelsTrainingConfig = AIModelsTrainingConfig.read_file()
    df = read_data(data_path, 6)
    df = normalize(df)
    df = filter_col(df)
    train_df, test_df = train_test_split(df, test_size=0.2, random_state=2, shuffle=True)
    estimator = create_estimator(df)
    ai_module = AiModule(estimator, model_training_config, train_df)
    ai_module.create_ensemble(train_df)
    ai_module.train(train_df)
    ai_module.evaluate(test_df)
    ai_module.save_model(model_path, columns_path)

def test_pipeline(data_path: str, model_path: str, columns_path: str) -> None:
    model_training_config: AIModelsTrainingConfig = AIModelsTrainingConfig.read_file()
    df = read_data(data_path, 6)
    df = normalize(df)
    estimator = create_estimator(df)
    ai_module = AiModule(estimator, model_training_config, df)
    ai_module.change_model(model_path, columns_path)
    df = select_col(df, ai_module.col)
    ai_module.evaluate(df)

def create_rules_pipeline(data_path: str, model_path: str, columns_path: str, dataset_config_path: str) -> list[CriticalRuleBaseModel]:
    with open(dataset_config_path, 'r', encoding='utf-8') as file:
        config = json.load(file)
    model_training_config: AIModelsTrainingConfig = AIModelsTrainingConfig.read_file()
    df = read_data(data_path, 6)
    estimator = create_estimator(df)
    ai_module = AiModule(estimator, model_training_config, df)
    ai_module.change_model(model_path, columns_path)
    df = select_col(df, ai_module.col)
    if 'Label' in df.columns:
        df = df.drop(['Label'], axis=1)
    rules = ai_module.create_rules(df, config)
    return rules