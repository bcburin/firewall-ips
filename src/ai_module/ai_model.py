import pandas as pd
import numpy as np

from ai_model_abstract import AiModelInterface
from utils.dataset import stratified_sample


class AiModel(AiModelInterface):

    def __init__(self, num_class: int) -> None:
        self.n_class = num_class

    def train(self, df : pd.DataFrame) -> np.ndarray:
        pass
    
    def evaluate(self, row: pd.DataFrame) -> int:
        pass

    def sample_data(self, df: pd.DataFrame):
        df = stratified_sample(df, 10000, self.n_class)
        X = df.drop('label', axis=1) 
        y = df['label']
        return X,y
    
