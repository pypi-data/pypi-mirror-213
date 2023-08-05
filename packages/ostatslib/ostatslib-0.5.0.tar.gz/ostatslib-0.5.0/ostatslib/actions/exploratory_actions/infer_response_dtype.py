"""
infer_response_dtype module
"""

import operator
from pandas import DataFrame, Series
from pandas.api.types import infer_dtype
from ostatslib import config

from ostatslib.states import State
from ._get_exploratory_reward import get_exploratory_reward
from ..action import Action, ActionInfo, ActionResult
from ..utils import validate_state

_ACTION_NAME = "Infer Response DType"
_VALIDATIONS = [('response_variable_label', operator.truth, None)]


@validate_state(action_name=_ACTION_NAME, validator_fns=_VALIDATIONS)
def _infer_response_dtype(state: State, data: DataFrame) -> ActionResult[None]:
    """
    Infer response dtype

    Args:
        state (State): state
        data (DataFrame): data

    Returns:
        ActionResult[None]: action result
    """
    state_copy: State = state.copy()
    response_var_label: str = state.get("response_variable_label")

    try:
        response: Series = data[response_var_label]
    except KeyError:
        return state, config.MIN_REWARD, ActionInfo(action_name=_ACTION_NAME,
                                                    action_fn=_infer_response_dtype,
                                                    model=None,
                                                    raised_exception=True)

    inferred_dtype = infer_dtype(response)
    state.set('response_inferred_dtype', inferred_dtype)
    reward = get_exploratory_reward(state, state_copy)

    return state, reward, ActionInfo(action_name=_ACTION_NAME,
                                     action_fn=_infer_response_dtype,
                                     model=None,
                                     raised_exception=False)


infer_response_dtype: Action[None] = _infer_response_dtype
