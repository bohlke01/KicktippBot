from model.utils import compute_scores, sign


def test_sign():
    assert sign(-5) == -1
    assert sign(0) == 0
    assert sign(7) == 1


def test_compute_scores():
    y_pred = [[2, 1], [3, 1], [1, 0], [1, 1], [3, 1]]
    y_target = [[2, 1], [2, 0], [4, 2], [0, 0], [1, 3]]
    # Default scoring
    scores_default = compute_scores(y_pred, y_target, True)
    assert scores_default == [4, 3, 2, 2, 0]
    # Modified scoring
    scores_mod = compute_scores(y_pred, y_target, False)
    assert scores_mod == [3, 1, 1, 1, 0]
