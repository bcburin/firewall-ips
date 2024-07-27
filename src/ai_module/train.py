from src.ai_module.pipeline import train_pipeline, test_pipeline


if __name__ == "__main__":
    data_path = "data/final_data"
    model_path = "src/ai_module/models/model.bin"
    dataset_config_path = 'config/dataset.json'
    train_pipeline(data_path, model_path, dataset_config_path)