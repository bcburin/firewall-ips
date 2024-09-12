from lightgbm import LGBMClassifier
from pandas import DataFrame
from sklearn.base import BaseEstimator
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier, VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier

from src.ai_module.utils.new_dataset import calculate_weights
from src.common.config import AIModelsTrainingConfig


def create_estimators(df: DataFrame):
    weights = calculate_weights(df)
    gbdt_model = GradientBoostingClassifier()
    lgbm_model = LGBMClassifier(class_weight=weights)
    lr_model = LogisticRegression(class_weight=weights)
    rf_model = RandomForestClassifier(class_weight=weights)
    mlp_classifier = MLPClassifier()
    knn_model = KNeighborsClassifier()
    estimators = {
        'lightgbm': lgbm_model,
        'gradientboost': gbdt_model,
        'logisticregression': lr_model,
        'randomforest': rf_model,
        'multilayerperceptron': mlp_classifier,
        'knn': knn_model
    }
    estimators = {
        'lightgbm': lgbm_model
    }
    return estimators


def select_best_estimator_from_hyperparams(estimator: BaseEstimator, param_grid: dict, df: DataFrame) \
        -> BaseEstimator:
    x_train = df.drop('Label', axis=1)
    y_train = df['Label']
    grid_search = GridSearchCV(
        estimator=estimator, param_grid=param_grid, cv=5, scoring='accuracy', verbose=2, n_jobs=-1)
    grid_search.fit(x_train, y_train)
    return grid_search.best_estimator_


def create_ensamble(models_config: AIModelsTrainingConfig, df: DataFrame):
    estimators = create_estimators(df=df)
    models_config_dict = models_config.model_dump()
    num_class = df['Label'].nunique()
    estimators_tuple_list = []
    for name, estimator in estimators.items():
        model_config_dict = models_config_dict[name]
        if model_config_dict["num_class"]:
            model_config_dict["num_class"] = num_class
        del model_config_dict["num_class"]
        estimators_tuple_list.append((
            name,
            select_best_estimator_from_hyperparams(
                estimator=estimator,
                param_grid=models_config_dict[name],
                df=df
        )))
    return VotingClassifier(estimators=estimators_tuple_list, voting='soft')
