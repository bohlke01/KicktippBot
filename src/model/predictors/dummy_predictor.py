import pandas as pd

from src.model.predictors.base_predictor import BasePredictor


class DummyPredictor(BasePredictor):
    """A predictor that always predicts the same score."""

    def __init__(self, default=(2, 1)):
        self.default = default

    def predict(self, data: pd.DataFrame):
        return [self.default] * len(data)

    def fit(self, data, labels):
        pass
