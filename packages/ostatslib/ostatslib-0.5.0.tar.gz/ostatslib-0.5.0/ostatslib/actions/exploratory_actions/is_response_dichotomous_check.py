"""
is_response_dichotomous_check module
"""

import operator
from pandas import DataFrame, Series
from pandas.api.types import infer_dtype
import numpy as np

from ostatslib.states import State
from ._get_exploratory_reward import get_exploratory_reward
from ..action import Action, ActionInfo, ActionResult
from ..utils import validate_state

_ACTION_NAME = "Is Response Dichotomous Check"
_VALIDATIONS = [('response_variable_label', operator.truth, None)]

@validate_state(action_name=_ACTION_NAME, validator_fns=_VALIDATIONS)
def _is_response_dichotomous_check(state: State, data: DataFrame) -> ActionResult[None]:
    """
    Check if response variable is dichotomous

    Args:
        state (State): state
        data (DataFrame): data

    Returns:
        ActionResult[None]: action result
    """
    state_copy: State = state.copy()
    response_var_label: str = state.get("response_variable_label")
    response: Series = data[response_var_label]
    state.set("is_response_dichotomous", __get_is_dichotomous_feature_value(response))
    reward = get_exploratory_reward(state, state_copy)
    return state, reward, ActionInfo(action_name=_ACTION_NAME,
                                     action_fn=_is_response_dichotomous_check,
                                     model=None,
                                     raised_exception=False)


def __get_is_dichotomous_feature_value(values: Series) -> int:
    return 1 if __is_dichotomous_check(values) else -1


def __is_dichotomous_check(values: Series) -> bool:
    inferred_dtype: str = infer_dtype(values)
    if inferred_dtype == "boolean":
        return True

    unique_values = values.unique()
    if len(unique_values) > 2:
        return False

    match inferred_dtype:
        case "categorical" | "string" | "object" | "mixed-integer":
            return True
        case "integer":
            return bool(__is_within_possible_boolean_range_of_integers(unique_values))
        case "floating" | "decimal" | "mixed-integer-float":
            first, second = unique_values
            return bool(first.is_integer() and second.is_integer() and
                bool(__is_within_possible_boolean_range_of_integers(unique_values)))
        case _:
            return False


def __is_within_possible_boolean_range_of_integers(unique_values):
    return np.any((unique_values >= -1) | (unique_values <= 2))


is_response_dichotomous_check: Action[None] = _is_response_dichotomous_check
