import pandas as pd

from src.model.predictors.base_predictor import BasePredictor
from src.model.data_loader import get_train_test_dfs
from src.model.utils import compute_scores


class OddPredictor(BasePredictor):
    def predict(self, data: pd.DataFrame, default = (2,1)):
        def predict_outcome(odds_home, odds_away):
            if odds_home < odds_away:
                return default
            elif odds_home > odds_away:
                return default[1], default[0]
            else:
                return 0,0

        return data.apply(lambda x: predict_outcome(x['B365H'], x['B365A']), axis=1)

    def fit(self, data, labels):
        pass



if __name__ == '__main__':
    X_train, y_train, X_test, y_test = get_train_test_dfs()

    predictor = OddPredictor()
    pred = predictor.predict(X_test)
    compute_scores(y_test, pred)
