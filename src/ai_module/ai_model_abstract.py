import pandas as pd
import numpy as np
from abc import ABC, abstractmethod


class AiModelInterface(ABC):

    def __init__(self) -> None:
        pass
    
    @abstractmethod
    def train(self, df : pd.DataFrame) -> np.ndarray:
        pass
    
    @abstractmethod
    def evaluate(self, row: pd.DataFrame) -> int:
        pass
    
