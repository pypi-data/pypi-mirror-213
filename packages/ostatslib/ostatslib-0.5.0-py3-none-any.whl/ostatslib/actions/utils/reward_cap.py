"""
reward_cap function module
"""

from functools import wraps
from pandas import DataFrame
from ostatslib import config
from ostatslib.states import State
from ..action import Action, TModel


def reward_cap(action_function: Action[TModel]) -> Action[TModel]:
    """
    Limits rewards from an action within lower and upper limits

    Args:
        action_function (Action[TModel]): action

    Returns:
        Action[TModel]: action
    """
    wraps(action_function)

    def function_wrapper(state: State, data: DataFrame):
        state, reward, info = action_function(state, data)
        reward = min(max(config.MIN_REWARD, reward), config.MAX_REWARD)
        return state, reward, info

    return function_wrapper
