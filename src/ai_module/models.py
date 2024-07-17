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


def select_hyperparameter(model: BaseEstimator, param_grid: dict, df: pd.DataFrame) -> BaseEstimator:
    x_train = df.drop('Label', axis=1)
    y_train = df['Label']
    grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=5, scoring='accuracy', verbose=2, n_jobs=-1)
    grid_search.fit(x_train, y_train)
    return grid_search.best_estimator_

def create_estimator(df):
    pytorch_model = Firewall_NN(df.shape[1] - 1)
    nn_model = PytorchAIModel(pytorch_model)
    gbdt_model = GradientBoostingClassifier()
    lgbm_model = LGBMClassifier()
    lr_model = LogisticRegression()
    rf_model = RandomForestClassifier()
    mlp_classifier = MLPClassifier()
    knn_model = KNeighborsClassifier()
    dt_model = DecisionTreeClassifier(max_depth=3, random_state=42)
    estimators = [('lightgbm',lgbm_model),('gradientboost',gbdt_model),('logisticregression',lr_model),('multilayerperceptron',mlp_classifier),
                  ('randomforest',rf_model),('nn',nn_model),('knn',knn_model)]
    return estimators