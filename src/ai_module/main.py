from sklearn.model_selection import train_test_split


from src.ai_module.utils.new_dataset import read_data, filter_col,normalize
from src.ai_module.ai_module import AiModule
from src.ai_module.models import create_estimator
from src.common.config import AIModelsTrainingConfig




if __name__ == "__main__":
    data_path = "data/final_data"
    file_path = "src/ai_module/models/model.bin"
    col_path = "src/ai_module/models/model.json"
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
    ai_module.save_model(file_path, col_path)
