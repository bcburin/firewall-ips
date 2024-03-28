from AI import AI
from sklearn.ensemble import BaseEnsemble
import pandas as pd
from dataset import Dataset

class Firewall:
    def __init__(self, model: BaseEnsemble, data_path: str, n: int = 2) -> None:
        self.number_output = n
        self.df = Dataset(data_path)
        self.AI = AI(model)

    def print_results(self) -> None:
        accuracy, precision, recall, f1_score = self.AI.get_metrics()
        print(f"A acuracia é {accuracy}")
        for i in range(self.number_output):
            print(f"A precisão para a classe {i} é {precision[i]}")  
            print(f"A recall para a classe {i} é {recall[i]}")  
            print(f"O F1 Score para a classe {i} é {f1_score[i]}")  

    
    def get_importance(self) -> pd.DataFrame:
        feature_importance = self.AI.model.feature_importances_
        X = self.df.drop('Action', axis=1) 
        importance_df = pd.DataFrame({'Feature': X.columns, 'Importance': feature_importance})
        importance_df = importance_df.sort_values(by='Importance', ascending=False)
        return importance_df

    def draw_net(self) -> None:
        self.df.draw_net()

    def run(self) -> None:
        self.df.process_data()
        data = self.df.split_data()
        self.AI.add_train_test_dataset(data[0], data[1], data[2], data[3])
        self.AI.train()
        self.AI.evaluate()
        return self.AI.get_metrics()