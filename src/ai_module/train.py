from src.ai_module.pipeline import train_pipeline


if __name__ == "__main__":
    data_path = "data/final_data"
    model_path = "src/ai_module/models/model.bin"
    columns_path = "src/ai_module/models/model.json"
    train_pipeline(data_path, model_path, columns_path)
