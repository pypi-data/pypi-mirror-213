"""
Support Vector Regression module
"""

import operator
from pandas import DataFrame
from sklearn.svm import SVR
from ostatslib import config

from ostatslib.states import State
from ..action import Action, ActionInfo, ActionResult
from ..utils import (calculate_score_reward,
                     reward_cap,
                     opaque_model,
                     split_response_from_explanatory_variables,
                     update_state_score,
                     validate_state,
                     model_selection)

_ACTION_NAME = "Support Vector Regression"
_VALIDATIONS = [('is_response_quantitative', operator.gt, 0),
                ('response_variable_label', operator.truth, None),
                ('log_rows_count', operator.gt, 0),
                ('log_rows_count', operator.lt, 0.71),
                ('support_vector_regression_score_reward', operator.eq, 0)]


@validate_state(action_name=_ACTION_NAME, validator_fns=_VALIDATIONS)
@reward_cap
@opaque_model
def _support_vector_regression(state: State, data: DataFrame) -> ActionResult[SVR]:
    """
    Fits data to a SVR model

    Args:
        state (State): current environment state
        data (DataFrame): data under analysis

    Returns:
        ActionResult[SVR]: action result
    """
    y_values, x_values = split_response_from_explanatory_variables(state, data)
    regressor: SVR = SVR()
    param_grid = {'C': [1, 10, 100],
                  'kernel': ['poly', 'rbf']}

    try:
        regressor, score = model_selection(regressor,
                                           param_grid,
                                           x_values,
                                           y_values)
    except ValueError:
        state.set('support_vector_regression_score_reward', config.MIN_REWARD)
        return state, config.MIN_REWARD, ActionInfo(action_name=_ACTION_NAME,
                                                    action_fn=_support_vector_regression,
                                                    model=None,
                                                    raised_exception=True)

    update_state_score(state, score)
    reward = calculate_score_reward(score)
    state.set('support_vector_regression_score_reward', reward)
    return state, reward, ActionInfo(action_name=_ACTION_NAME,
                                     action_fn=_support_vector_regression,
                                     model=regressor,
                                     raised_exception=False)


support_vector_regression: Action[SVR] = _support_vector_regression
