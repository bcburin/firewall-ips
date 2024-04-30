import pickle

import pandas as pd
import numpy as np

from ai_model import AiModel


class AiModule():

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