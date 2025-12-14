import numpy as np
import pandas as pd
import xgboost
from sklearn.multioutput import MultiOutputRegressor
from sklearn.preprocessing import LabelEncoder

from src.model.predictors.base_predictor import BasePredictor
from src.model.data_loader import get_train_test_dfs
from src.model.utils import compute_scores


def generate_features(df):
    df = df.copy()

    df.drop(columns=["Date", "Time"], inplace=True)
    return df


class XGBoostPredictor(BasePredictor):
    def __init__(self):
        self.regressor = xgboost.XGBRegressor(objective="reg:squarederror")
        self.multi_output_regressor = MultiOutputRegressor(self.regressor)
        self.team_encoder = LabelEncoder()

    def predict(self, data: pd.DataFrame):
        data = generate_features(data)
        data[["HomeTeam", "AwayTeam"]] = data[["HomeTeam", "AwayTeam"]].replace(
            {"St Pauli": "FC Koln", "Holstein Kiel": "Darmstadt"}
        )
        data["HomeTeam"] = self.team_encoder.transform(data["HomeTeam"])
        data["AwayTeam"] = self.team_encoder.transform(data["AwayTeam"])
        prediction = self.multi_output_regressor.predict(data)
        return np.round(prediction)

    def fit(self, data, labels):
        data = generate_features(data)
        data["HomeTeam"] = self.team_encoder.fit_transform(data["HomeTeam"])
        data["AwayTeam"] = self.team_encoder.transform(data["AwayTeam"])
        self.multi_output_regressor.fit(data, labels)


if __name__ == "__main__":
    X_train, y_train, X_test, y_test = get_train_test_dfs()

    predictor = XGBoostPredictor()
    predictor.fit(X_train, y_train)
    pred = predictor.predict(X_test)
    compute_scores(y_test, pred)
