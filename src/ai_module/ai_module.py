import pickle

import pandas as pd
import numpy as np

from src.ai_module.ai_model import AiModel
from src.services.persistence import PersistableObject

class AiModule(PersistableObject):

    def __init__(self, model : AiModel) -> None:
        self.model : AiModel = model
    
    def _load(self, model_bytes: bytes) -> None:
        self.model = pickle.loads(model_bytes)
        
    def _dump(self) -> bytes:
        return pickle.dumps(self.model)     

    def train(self,  df : pd.DataFrame) -> np.ndarray:
        return self.model.train(df=df)
    
    def evaluate(self, row: pd.DataFrame) -> int:
        return self.model.evaluate(row)
    
    def change_model(self, model: AiModel) -> None:
        self.model = model