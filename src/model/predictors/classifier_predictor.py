import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.multiclass import OneVsRestClassifier
from sklearn.multioutput import MultiOutputClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import LinearSVC

from src.model.predictors.base_predictor import BasePredictor


def generate_features(df):
    df = df.copy()

    df.drop(columns=["Date", "Time"], inplace=True)
    return df


class ForrestClassifierPredictor(BasePredictor):
    def __init__(self):
        self.forest = RandomForestClassifier(random_state=1)
        self.team_encoder = LabelEncoder()

    def predict(self, data: pd.DataFrame):
        data = generate_features(data)
        data[["HomeTeam", "AwayTeam"]] = data[["HomeTeam", "AwayTeam"]].replace(
            {"St Pauli": "FC Koln", "Holstein Kiel": "Darmstadt"}
        )
        data["HomeTeam"] = self.team_encoder.transform(data["HomeTeam"])
        data["AwayTeam"] = self.team_encoder.transform(data["AwayTeam"])
        prediction = self.forest.predict(data)
        prediction = [[int(x) for x in p.split(":")] for p in prediction]
        return np.round(prediction)

    def fit(self, data, labels):
        data = generate_features(data)
        data["HomeTeam"] = self.team_encoder.fit_transform(data["HomeTeam"])
        data["AwayTeam"] = self.team_encoder.transform(data["AwayTeam"])
        labels = [f"{h}:{a}" for h, a in labels]
        self.forest.fit(data, labels)


class MultiOutputClassifierPredictor(BasePredictor):
    def __init__(self):
        self.forest = RandomForestClassifier(random_state=1)
        self.multi_output_regressor = MultiOutputClassifier(self.forest, n_jobs=2)
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


class MultiClassifierPredictor(BasePredictor):
    def __init__(self):
        self.classifier = OneVsRestClassifier(LinearSVC(random_state=0))
        self.team_encoder = LabelEncoder()

    def predict(self, data: pd.DataFrame):
        data = generate_features(data)
        data[["HomeTeam", "AwayTeam"]] = data[["HomeTeam", "AwayTeam"]].replace(
            {"St Pauli": "FC Koln", "Holstein Kiel": "Darmstadt"}
        )
        data["HomeTeam"] = self.team_encoder.transform(data["HomeTeam"])
        data["AwayTeam"] = self.team_encoder.transform(data["AwayTeam"])
        prediction = self.classifier.predict(data)
        return np.round(prediction)

    def fit(self, data, labels):
        data = generate_features(data)
        data["HomeTeam"] = self.team_encoder.fit_transform(data["HomeTeam"])
        data["AwayTeam"] = self.team_encoder.transform(data["AwayTeam"])
        self.classifier.fit(data, labels)
