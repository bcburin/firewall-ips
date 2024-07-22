from sklearn.model_selection import train_test_split
from tqdm import tqdm
import pandas as pd

from src.ai_module.utils.new_dataset import read_data, select_col,normalize
from src.ai_module.ai_module import AiModule
from src.ai_module.models import create_estimator
from src.common.config import AIModelsTrainingConfig




if __name__ == "__main__":
    data_path = "data/final_data"
    file_path = "src/ai_module/models/model.bin"
    col_path = "src/ai_module/models/model.json"
    model_training_config: AIModelsTrainingConfig = AIModelsTrainingConfig.read_file()
    df = read_data(data_path, 6)
    estimator = create_estimator(df)
    ai_module = AiModule(estimator, model_training_config, df)
    ai_module.change_model(file_path, col_path)
    df = select_col(df, ai_module.col)
    df = df.drop(['Label'],axis=1)
    normalized_df = normalize(df.copy())
    set_rules = set()
    rules = []
    rules.append(['Dst Port', 'Protocol', 'Flow Duration', 'Tot Fwd Pkts', 'Tot Bwd Pkts'])
    with tqdm(total= len(normalized_df)) as pbar:
        for index, row in normalized_df.iterrows():
            original_row : pd.Series = df.loc[index]
            label = ai_module.predict(row.to_frame().T)
            if label != 0:
                set_rules.add(tuple(original_row[['Dst Port', 'Protocol', 'Flow Duration', 'Tot Fwd Pkts', 'Tot Bwd Pkts']].tolist()))
            pbar.update(1)
    for rule in set_rules:
        rules.append(list(rule))
print(rules)