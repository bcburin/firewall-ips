from __future__ import annotations
from pydantic import BaseModel


class ConfusionMatrixInfo(BaseModel):
    confusion_matrix: list[list[str]]
    precision: list[float]
    recall: list[float]
    f1_score: list[float]
    accuracy: float

class Time(BaseModel):
    hour: int
    minute: int