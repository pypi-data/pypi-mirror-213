"""
Linear Support Vector Classification module
"""

import operator
from pandas import DataFrame
from sklearn.svm import LinearSVC
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

_ACTION_NAME = "Linear Support Vector Classification"
_VALIDATIONS = [('response_variable_label', operator.truth, None),
                ('is_response_discrete', operator.gt, 0),
                ('log_rows_count', operator.gt, 0),
                ('log_rows_count', operator.lt, 0.81),
                ('linear_support_vector_classification_score_reward', operator.eq, 0)]


@validate_state(action_name=_ACTION_NAME, validator_fns=_VALIDATIONS)
@reward_cap
@opaque_model
def _linear_support_vector_classification(state: State, data: DataFrame) -> ActionResult[LinearSVC]:
    """
    Fits data to a LinearSVC model

    Args:
        state (State): current environment state
        data (DataFrame): data under analysis

    Returns:
        ActionResult[LinearSVC]: action result
    """
    y_values, x_values = split_response_from_explanatory_variables(state, data)
    classifier: LinearSVC = LinearSVC()
    param_grid = {'penalty': ['l1', 'l2'],
                  'loss': ['squared_hinge', 'hinge']}

    try:
        classifier, score = model_selection(classifier,
                                            param_grid,
                                            x_values,
                                            y_values)
    except ValueError:
        state.set('linear_support_vector_classification_score_reward',
                  config.MIN_REWARD)
        return state, config.MIN_REWARD, ActionInfo(action_name=_ACTION_NAME,
                                                    action_fn=_linear_support_vector_classification,
                                                    model=None,
                                                    raised_exception=True)

    update_state_score(state, score)
    reward = calculate_score_reward(score)
    state.set('linear_support_vector_classification_score_reward', reward)
    return state, reward, ActionInfo(action_name=_ACTION_NAME,
                                     action_fn=_linear_support_vector_classification,
                                     model=classifier,
                                     raised_exception=False)


linear_support_vector_classification: Action[LinearSVC] = _linear_support_vector_classification
