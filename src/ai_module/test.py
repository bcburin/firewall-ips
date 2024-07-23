from src.ai_module.pipeline import test_pipeline


if __name__ == "__main__":
    data_path = "data/final_data"
    model_path = "src/ai_module/models/model.bin"
    columns_path = "src/ai_module/models/model.json"
    test_pipeline(data_path, model_path, columns_path)
