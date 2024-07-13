import numpy as np


from src.ai_module.utils.new_dataset import read_data
from src.ai_module.models import LightgbmModel
from src.ai_module.ai_module import AiModule
from src.common.config import AIModelsTrainingConfig, ConfigurationManager


def print_results(cm: np.ndarray) -> None:
    print(cm)
    precision = np.zeros(len(cm))
    recall = np.zeros(len(cm))
    f1_score = np.zeros(len(cm))
    for i in range(len(cm)):
        precision[i] = cm[i][i]/np.sum(cm[i])
        recall[i] = cm[i][i]/np.sum(cm[:, i])
        f1_score[i] = (2 * precision[i] * recall[i])/(precision[i] + recall[i])
    print(f1_score)
    print(recall)
    print(precision)


def main():
    data_path = "data/final_data"
    df = read_data(data_path)
    model_training_config: AIModelsTrainingConfig = ConfigurationManager().get_ai_models_training_config()
    ai_model = LightgbmModel(config=model_training_config.lightgbm[0])
    ai_module = AiModule(ai_model)
    cm = ai_module.train(df.copy())
    print_results(cm)


if __name__ == "__main__":
    main()
