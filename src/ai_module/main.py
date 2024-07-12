import pandas as pd
import numpy as np


from src.ai_module.utils.new_dataset import read_data
from src.ai_module.models import LightgbmModel, GradientBoostModel, LogisticRegressionModel, MultiPerceptronModel, RandomForestModel, SVMModel
from src.ai_module.ai_module import AiModule
from src.common.config import AIModelsTrainingConfig, ServerConfig


def print_results(cm: np.ndarray) -> None:
    print(cm)
    precision = np.zeros(len(cm))
    recall = np.zeros(len(cm))
    f1_score = np.zeros(len(cm))
    for i in range(len(cm)):
        precision[i] = cm[i][i]/np.sum(cm[i])
        recall[i] = cm[i][i]/np.sum(cm[:,i])
        f1_score[i] = (2 * precision[i] * recall[i])/(precision[i] + recall[i])
    print(f1_score)
    print(recall)
    print(precision)


if __name__ == "__main__":
    
    #server_config: ServerConfig = ServerConfig.get()
    #data_path = server_config.ai_module.training.data.resolved_path
    data_path = "data/final_data"
    df = read_data(data_path)
    model_training_config: AIModelsTrainingConfig = AIModelsTrainingConfig.get()
    ai_model = LightgbmModel(config=model_training_config.lightgbm[0])
    ai_module = AiModule(ai_model)
    cm = ai_module.train(df.copy())
    print_results(cm)