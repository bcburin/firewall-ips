from sklearn.model_selection import train_test_split
from lightgbm import LGBMClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier

from src.ai_module.utils.new_dataset import read_data
from src.ai_module.ai_module import AiModule
from src.ai_module.ai_model import PytorchAIModel, Firewall_NN
from src.common.config import AIModelsTrainingConfig


def create_model_tuple(df):
    pytorch_model = Firewall_NN(df.shape[1] - 1)
    nn_model = PytorchAIModel(pytorch_model)
    gbdt_model = GradientBoostingClassifier()
    lgbm_model = LGBMClassifier(objective='multiclass', num_class=7)
    lr_model = LogisticRegression()
    rf_model = RandomForestClassifier()
    SVC_model = SVC(probability=True)
    mlp_classifier = MLPClassifier()
    knn_model = KNeighborsClassifier()
    dt_model = DecisionTreeClassifier(max_depth=3, random_state=42)
    estimators = [('lightgbm',lgbm_model)]
    return estimators

if __name__ == "__main__":
    data_path = "data/final_data"
    model_training_config: AIModelsTrainingConfig = AIModelsTrainingConfig.get()
    df = read_data(data_path)
    train_df, test_df = train_test_split(df, test_size=0.2, random_state=2, shuffle=True)
    estimator = create_model_tuple(df)
    ai_module = AiModule(estimator, model_training_config, train_df)
    ai_module.train(train_df)
    ai_module.evaluate(test_df)
