import pandas as pd

from model.data_loader import get_targets, load_data
from model.predictors.dummy_predictor import DummyPredictor
from model.predictors.odd_predictor import OddPredictor, ValidOddPredictor
from model.utils import compute_scores


def evaluate_predictor(predictor, df):
    """Evaluate a predictor on a given DataFrame and return the total score."""
    pred = predictor.predict(df)
    targets = get_targets(df)
    scores = compute_scores(targets, pred, default_scoring=True)
    return sum(scores)


def simulate():
    """Simulate different predictors on football match data and summarize their scores for each season."""
    dfs = load_data()
    predictors = {
        "DummyPredictor21": DummyPredictor((2, 1)),
        "DummyPredictor10": DummyPredictor((1, 0)),
        "DummyPredictor11": DummyPredictor((1, 1)),
        "OddPredictor21": OddPredictor((2, 1)),
        "OddPredictor10": OddPredictor((1, 0)),
        "ValidOddPredictor21": ValidOddPredictor((2, 1)),
    }

    results = {}
    for predictor_name, predictor in predictors.items():
        results[predictor_name] = {}
        for season, df in dfs.items():
            score = 0
            for gameday in df["GameDay"].unique():
                df_subset = df[df["GameDay"] == gameday]
                score += evaluate_predictor(predictor, df_subset)
            results[predictor_name][season] = score

    df = pd.DataFrame(results)
    print(f"\nSummary of scores:\n{df.to_string()}")
    return df


if __name__ == "__main__":
    simulate()
