import pandas as pd
from sklearn.model_selection import GridSearchCV
from sklearn.base import BaseEstimator
from lightgbm import LGBMClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier

from src.ai_module.ai_model import PytorchAIModel, Firewall_NN
from src.ai_module.utils.new_dataset import calculate_weights


def select_hyperparameter(model: BaseEstimator, param_grid: dict, df: pd.DataFrame) -> BaseEstimator:
    x_train = df.drop('Label', axis=1)
    y_train = df['Label']
    grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=5, scoring='accuracy', verbose=2, n_jobs=-1)
    grid_search.fit(x_train, y_train)
    return grid_search.best_estimator_

def create_estimator(df):
    weights = calculate_weights(df)
    pytorch_model = Firewall_NN(df.shape[1] - 1)
    nn_model = PytorchAIModel(pytorch_model)
    gbdt_model = GradientBoostingClassifier()
    lgbm_model = LGBMClassifier(class_weight=weights)
    lr_model = LogisticRegression(class_weight=weights)
    rf_model = RandomForestClassifier(class_weight=weights)
    mlp_classifier = MLPClassifier()
    knn_model = KNeighborsClassifier()
    estimators = [('lightgbm',lgbm_model),('gradientboost',gbdt_model),('logisticregression',lr_model),('randomforest',rf_model),
                  ('multilayerperceptron',mlp_classifier), ('knn',knn_model), ('nn',nn_model)]
    estimators = [('lightgbm',lgbm_model)]
    return estimators

def create_models(df):
    weights = calculate_weights(df)
    pytorch_model = Firewall_NN(df.shape[1] - 1)
    nn_model = PytorchAIModel(pytorch_model)
    gbdt_model = GradientBoostingClassifier()
    lgbm_model = LGBMClassifier(class_weight=weights)
    lr_model = LogisticRegression(class_weight=weights)
    rf_model = RandomForestClassifier(class_weight=weights)
    mlp_classifier = MLPClassifier()
    knn_model = KNeighborsClassifier()
    return lr_model