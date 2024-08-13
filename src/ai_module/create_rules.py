from src.ai_module.pipeline import create_rules_pipeline


if __name__ == "__main__":
    data_path = "data/final_data"
    model_path = "src/ai_module/models/model.bin"
    dataset_config_path = 'config/dataset.json'
    rules = create_rules_pipeline(data_path, model_path, dataset_config_path)