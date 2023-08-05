"""
update state score helper function module
"""

import math

from ostatslib.states import State


def update_state_score(state: State, score: float) -> State:
    """
    Updates State score attribute

    Args:
        state (State): state
        score (float): action score

    Returns:
        State: state
    """
    if math.isnan(score) or (not 0 <= score <= 1):
        state.set('score', 0)
        return state

    state.set('score', score)
    return state
