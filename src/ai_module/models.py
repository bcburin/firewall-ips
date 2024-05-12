from lightgbm import LGBMClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier

from src.ai_module.ai_model import ScikitLearnAIModel
from src.common.config import LightgbmConfig, GradientBoostConfig, LogisticRegressionConfig, MultiLayerPerceptronConfig, RandomForestConfig, SVMConfig


class LightgbmModel(ScikitLearnAIModel):
    def __init__(self, config: LightgbmConfig) -> None:
        super().__init__(config, LGBMClassifier)


class GradientBoostModel(ScikitLearnAIModel):
    def __init__(self, config: GradientBoostConfig) -> None:
        super().__init__(config, GradientBoostingClassifier)


class LogisticRegressionModel(ScikitLearnAIModel):
    def __init__(self, config: LogisticRegressionConfig) -> None:
        super().__init__(config, LogisticRegression)


class MultiPerceptronModel(ScikitLearnAIModel):
    def __init__(self, config: MultiLayerPerceptronConfig) -> None:
        super().__init__(config, MLPClassifier)


class RandomForestModel(ScikitLearnAIModel):
    def __init__(self, config: RandomForestConfig) -> None:
        super().__init__(config, RandomForestClassifier)

class SVMModel(ScikitLearnAIModel):
    def __init__(self, config: SVMConfig) -> None:
        super().__init__(config, SVC)