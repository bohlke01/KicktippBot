import os

import pandas as pd


def get_train_test_dfs():
    # Get the absolute path of the current script
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Define the relative paths to the data directories and files
    train_dir = os.path.join(current_dir, '../../data/football-data.co.uk')
    test_file = os.path.join(current_dir, '../../data/football-data.co.uk/BL24.csv')

    files = os.listdir(train_dir)

    train_df = pd.DataFrame()
    for file in files[1:]:
        train_df = pd.concat([train_df, pd.read_csv(f'{train_dir}/{file}')], axis=0)

    test_df = pd.read_csv(f'{test_file}')

    return get_features(train_df), get_targets(train_df), get_features(test_df), get_targets(test_df)

def get_features(df):
    features = ['Date', 'Time', 'HomeTeam', 'AwayTeam', 'B365H', 'B365D', 'B365A', 'B365<2.5', 'B365>2.5']
    df_return = df.loc[:, features]
    df_return.rename(columns={'B365<2.5': 'B365U', 'B365>2.5': 'B365O'}, inplace=True)
    return df_return

def get_targets(df):
    return df.loc[:, ['FTHG', 'FTAG']].values.tolist()