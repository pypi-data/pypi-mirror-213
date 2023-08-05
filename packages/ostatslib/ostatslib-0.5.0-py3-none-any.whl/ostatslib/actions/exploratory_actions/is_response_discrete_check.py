"""
is_response_discrete_check module
"""

import operator
from pandas import DataFrame, Series
import numpy as np

from ostatslib.states import State
from ._get_exploratory_reward import get_exploratory_reward
from ..action import Action, ActionInfo, ActionResult
from ..utils import validate_state

_ACTION_NAME = "Is Response Discrete Check"
_VALIDATIONS = [('response_variable_label', operator.truth, None)]

@validate_state(action_name=_ACTION_NAME, validator_fns=_VALIDATIONS)
def _is_response_discrete_check(state: State, data: DataFrame) -> ActionResult[None]:
    """
    Check if response variable is discrete

    Args:
        state (State): state
        data (DataFrame): data

    Returns:
        ActionResult[None]: action result
    """
    state_copy: State = state.copy()
    response_var_label: str = state.get("response_variable_label")
    response: Series = data[response_var_label]

    is_discrete: bool = __is_discrete_check(response)
    if is_discrete:
        state.set("is_response_discrete", 1)
    else:
        state.set("is_response_discrete", -1)

    reward = get_exploratory_reward(state, state_copy)
    return state, reward, ActionInfo(action_name=_ACTION_NAME,
                                     action_fn=_is_response_discrete_check,
                                     model=None,
                                     raised_exception=False)


def __is_discrete_check(values: Series) -> bool:
    unique_values = values.unique()

    is_numeric = np.issubdtype(unique_values.dtype, np.number)
    if not is_numeric:
        return False

    is_inexact = np.issubdtype(unique_values.dtype, np.inexact)
    if is_inexact:
        for value in unique_values:
            is_whole = float(value).is_integer()
            if not is_whole:
                return False

    return True


is_response_discrete_check: Action[None] = _is_response_discrete_check
