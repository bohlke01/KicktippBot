import numpy as np
import pandas as pd

from src.model.predictors.base_predictor import BasePredictor


class OddPredictor(BasePredictor):
    """A predictor that predicts the score based on betting odds."""

    def __init__(self, default=(2, 1)):
        self.default = default

    def predict(self, data: pd.DataFrame):
        def predict_outcome(odds_home, odds_away):
            if odds_home < odds_away:
                return self.default
            elif odds_home > odds_away:
                return self.default[::-1]
            else:
                return 0, 0

        return data.apply(lambda x: predict_outcome(x["BWCH"], x["BWCA"]), axis=1)

    def fit(self, data, labels):
        pass


class ValidOddPredictor(BasePredictor):
    """A predictor that predicts the score based on betting odds with three guaranteed draws."""

    def __init__(self, default=(2, 1)):
        self.default = default

    def predict(self, data: pd.DataFrame):
        odds: np.ndarray = data[["BWCH", "BWCD", "BWCA"]].values
        predictions = [self.default] * len(data)

        for index, row in enumerate(odds):
            if row[0] > row[2]:
                predictions[index] = (0, 1)

        # predict three draws with the best odds
        for index in np.argsort(odds[:, 1])[:3]:
            predictions[index] = (1, 1)
        return predictions

    def fit(self, data, labels):
        pass
