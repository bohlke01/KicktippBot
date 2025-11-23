import pandas as pd

from src.model.predictors.base_predictor import BasePredictor
from src.model.data_loader import get_train_test_dfs
from src.model.utils import compute_scores


class DummyPredictor(BasePredictor):
    def predict(self, data: pd.DataFrame):
        return [[2, 1]] * len(data)

    def fit(self, data, labels):
        pass



if __name__ == '__main__':
    X_train, y_train, X_test, y_test = get_train_test_dfs()

    predictor = DummyPredictor()
    pred = predictor.predict(X_test)
    compute_scores(y_test, pred)
