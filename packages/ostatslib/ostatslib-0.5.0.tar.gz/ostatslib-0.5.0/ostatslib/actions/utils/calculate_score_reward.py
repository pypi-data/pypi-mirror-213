"""
calculate score reward helper function module
"""

import math
from ostatslib import config


def calculate_score_reward(score: float) -> float:
    """
    Calculates reward based on standard score.

    Args:
        score (float): standard score

    Returns:
        float: reward
    """
    if math.isnan(score) or (not -1 <= score <= 1):
        return -1

    if score <= config.MIN_ACCEPTED_SCORE:
        return - (1 - score)

    return score
