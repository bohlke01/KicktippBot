def compute_score(x_home, x_away, y_home, y_away):
    """Compute kicktipp score based on the outcome of a football match.

    Args:
        x_home (int): Predicted number of goals scored by the home team.
        x_away (int): Predicted number of goals scored by the away team.
        y_home (int): Actual number of goals scored by the home team.
        y_away (int): Actual number of goals scored by the away team.
    Returns:
        int: Kicktipp score for the match.
            3: Correct outcome and correct score
            1: Correct outcome
        """
    if x_home == y_home and x_away == y_away:
        return 3
    elif (x_home > x_away and y_home > y_away) or (x_home < x_away and y_home < y_away) or (x_home == x_away and y_home == y_away):
        return 1
    else:
        return 0


def compute_scores(y_pred: list[list[int]], y_target: list[list[int]]) -> list[int]:
    """Compute the total score based on the predicted and target outcomes of football matches.

    Args:
        y_pred (list[list[int]]): List of predicted outcomes for each match.
        y_target (list[list[int]]): List of target outcomes for each match.

    Returns:
        list[int]: List of scores for each match.
    """
    scores = [compute_score(pred[0], pred[1], target[0], target[1]) for pred, target in zip(y_pred, y_target)]
    print("The total score is: ", sum(scores))
    return scores