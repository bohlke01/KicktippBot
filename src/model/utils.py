def sign(num: int) -> int:
    """Return the sign of a number."""
    return 1 if num > 0 else -1 if num < 0 else 0


def compute_score(x_home, x_away, y_home, y_away, default_scoring: bool = False) -> int:
    """Compute kicktipp score based on the outcome of a football match.

    Args:
        x_home (int): Predicted number of goals scored by the home team.
        x_away (int): Predicted number of goals scored by the away team.
        y_home (int): Actual number of goals scored by the home team.
        y_away (int): Actual number of goals scored by the away team.
        default_scoring (bool): If True, use the default kicktipp scoring system
            (4 points for correct result, 3 for correct goal difference, 2 for correct tendency).
            If False, use the modified scoring system (3-1-1).
    Returns:
        int: Kicktipp score for the match.
    """
    if x_home == y_home and x_away == y_away:
        return 4 if default_scoring else 3
    if x_home - x_away == y_home - y_away and y_home != y_away:
        return 3 if default_scoring else 1
    if sign(x_home - x_away) == sign(y_home - y_away):
        return 2 if default_scoring else 1
    else:
        return 0


def compute_scores(
    y_pred: list[list[int]], y_target: list[list[int]], default_scoring: bool = False
) -> list[int]:
    """Compute the total score based on the predicted and target outcomes of football matches.

    Args:
        y_pred (list[list[int]]): List of predicted outcomes for each match.
        y_target (list[list[int]]): List of target outcomes for each match.
        default_scoring (bool): If True, use the default kicktipp scoring system (4-3-2).
                                 If False, use the modified scoring system (3-1-1).

    Returns:
        list[int]: List of scores for each match.
    """
    scores = [
        compute_score(pred[0], pred[1], target[0], target[1], default_scoring)
        for pred, target in zip(y_pred, y_target)
    ]
    return scores
