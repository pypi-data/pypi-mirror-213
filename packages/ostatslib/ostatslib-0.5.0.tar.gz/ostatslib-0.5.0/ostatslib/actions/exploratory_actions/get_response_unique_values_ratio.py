"""
response_unique_values_ratio module
"""

import operator
from pandas import DataFrame, Series
from ostatslib import config
from ostatslib.states import State

from ..action import Action, ActionInfo, ActionResult
from ..utils import validate_state

_ACTION_NAME = "Get Response Unique Values Ratio"
_VALIDATIONS = [('response_variable_label', operator.truth, None)]


@validate_state(action_name=_ACTION_NAME, validator_fns=_VALIDATIONS)
def _get_response_unique_values_ratio(state: State,
                                      data: DataFrame) -> ActionResult[None]:
    """
    Gets response unique values ratio to total rows

    Args:
        state (State): state
        data (DataFrame): data

    Returns:
        ActionResult[None]: action result
    """
    response_unique_values_ratio = __calculate_response_unique_values_ratio(state,
                                                                            data)
    reward = __calculate_reward(state, response_unique_values_ratio)
    state = __update_state(state, response_unique_values_ratio)
    return state, reward, ActionInfo(action_name=_ACTION_NAME,
                                     action_fn=_get_response_unique_values_ratio,
                                     model=None,
                                     raised_exception=False)


def __calculate_response_unique_values_ratio(state: State, data: DataFrame) -> float:
    response_var_label = state.get("response_variable_label")
    response_values: Series = data[response_var_label]

    return response_values.nunique()/len(response_values)


def __calculate_reward(state: State, response_unique_values_ratio: float) -> float:
    if state.get("response_unique_values_ratio") == response_unique_values_ratio:
        return config.MIN_REWARD

    return config.MAX_EXPLORATORY_REWARD


def __update_state(state: State, response_unique_values_ratio: float) -> State:
    state.set("response_unique_values_ratio", response_unique_values_ratio)
    return state


get_response_unique_values_ratio: Action[None] = _get_response_unique_values_ratio
