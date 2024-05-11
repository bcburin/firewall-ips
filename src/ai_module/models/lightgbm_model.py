from lightgbm import LGBMClassifier

from src.ai_module.ai_model import ScikitLearnAIModel
from src.common.config import LightgbmConfig


class LightgbmModel(ScikitLearnAIModel):
    def __init__(self, config: LightgbmConfig) -> None:
        super().__init__(config, LGBMClassifier)
        self.model = LGBMClassifier(**config.model_dump())