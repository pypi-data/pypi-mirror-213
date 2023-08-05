"""
explainability rewards decorators module
"""

from functools import wraps

from pandas import DataFrame

from ostatslib.states import State
from ..action import Action, TModel

OPAQUE_PENALTY = -.1
INTERPRETABLE_REWARD = .1
COMPREHENSIBLE_REWARD = .075


def opaque_model(
        action_function: Action[TModel]) -> Action[TModel]:
    """
    Penalty for actions resulting in an opaque model

    Args:
        action_function (Action[TModel]): action

    Returns:
        Action[TModel]: action
    """
    wraps(action_function)

    def function_wrapper(state: State, data: DataFrame):
        state, reward, info = action_function(state, data)
        reward += OPAQUE_PENALTY
        return state, reward, info

    return function_wrapper


def interpretable_model(
        action_function: Action[TModel]) -> Action[TModel]:
    """
    Reward for actions resulting in an interpretable model

    Args:
        action_function (Action[TModel]): action

    Returns:
        Action[TModel]: action
    """
    wraps(action_function)

    def function_wrapper(state: State, data: DataFrame):
        state, reward, info = action_function(state, data)
        reward += INTERPRETABLE_REWARD
        return state, reward, info

    return function_wrapper


def comprehensible_model(
        action_function: Action[TModel]) -> Action[TModel]:
    """
    Reward for actions resulting in an comprehensible model

    Args:
        action_function (Action[TModel]): action

    Returns:
        Action[TModel]: action
    """
    wraps(action_function)

    def function_wrapper(state: State, data: DataFrame):
        state, reward, info = action_function(state, data)
        reward += COMPREHENSIBLE_REWARD
        return state, reward, info

    return function_wrapper
