"""
Get exploratory reward module
"""

from ostatslib import config
from ostatslib.states import State


def get_exploratory_reward(state: State, state_copy: State) -> float:
    """
    Get exploratory action reward default method.
    If state is unchanged, action should penalized.

    Args:
        state (State): updated state
        state_copy (State): state copy before exploratory updates

    Returns:
        float: reward
    """
    if state == state_copy:
        return config.MIN_REWARD

    return config.MAX_EXPLORATORY_REWARD
