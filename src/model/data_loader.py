import os

import pandas as pd


def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(current_dir, "../../data/football-data.co.uk/")
    files = os.listdir(path)
    df_all = pd.DataFrame()

    for file in sorted(files):
        df = pd.read_csv(os.path.join(path, file))
        df.insert(1, "Season", file.split(".")[0])
        df.insert(2, "GameDay", df.index // 9 + 1)
        df_all = pd.concat([df_all, df], axis=0)

    df_all["BWCH"] = df_all["BWCH"].fillna(df_all["B365CH"])
    df_all["BWCD"] = df_all["BWCD"].fillna(df_all["B365CD"])
    df_all["BWCA"] = df_all["BWCA"].fillna(df_all["B365CA"])

    return df_all


def get_train_test_dfs():
    # Get the absolute path of the current script
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Define the relative paths to the data directories and files
    train_dir = os.path.join(current_dir, "../../data/football-data.co.uk")
    test_file = os.path.join(current_dir, "../../data/football-data.co.uk/BL24.csv")

    files = os.listdir(train_dir)

    train_df = pd.DataFrame()
    for file in files[1:]:
        train_df = pd.concat([train_df, pd.read_csv(f"{train_dir}/{file}")], axis=0)

    train_df["BWCH"] = train_df["BWCH"].fillna(train_df["B365CH"])
    train_df["BWCD"] = train_df["BWCD"].fillna(train_df["B365CD"])
    train_df["BWCA"] = train_df["BWCA"].fillna(train_df["B365CA"])

    test_df = pd.read_csv(f"{test_file}")
    test_df["BWCH"] = test_df["BWCH"].fillna(test_df["B365CH"])
    test_df["BWCD"] = test_df["BWCD"].fillna(test_df["B365CD"])
    test_df["BWCA"] = test_df["BWCA"].fillna(test_df["B365CA"])

    return (
        get_features(train_df),
        get_targets(train_df),
        get_features(test_df),
        get_targets(test_df),
    )


def get_features(df):
    features = ["Date", "Time", "HomeTeam", "AwayTeam", "BWCH", "BWCD", "BWCA"]
    return df.loc[:, features]


def get_targets(df):
    return df.loc[:, ["FTHG", "FTAG"]].values.tolist()
