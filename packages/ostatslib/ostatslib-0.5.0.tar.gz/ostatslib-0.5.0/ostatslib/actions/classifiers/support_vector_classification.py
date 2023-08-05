"""
Support Vector Classification module
"""

import operator
from pandas import DataFrame
from sklearn.svm import SVC
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

_ACTION_NAME = "Support Vector Classification"
_VALIDATIONS = [('response_variable_label', operator.truth, None),
                ('is_response_discrete', operator.gt, 0),
                ('log_rows_count', operator.gt, 0),
                ('log_rows_count', operator.lt, 0.71),
                ('support_vector_classification_score_reward', operator.eq, 0)]


@validate_state(action_name=_ACTION_NAME, validator_fns=_VALIDATIONS)
@reward_cap
@opaque_model
def _support_vector_classification(state: State, data: DataFrame) -> ActionResult[SVC]:
    """
    Fits data to a SVC model

    Args:
        state (State): current environment state
        data (DataFrame): data under analysis

    Returns:
        ActionResult[SVC]: action result
    """
    y_values, x_values = split_response_from_explanatory_variables(state, data)
    classifier: SVC = SVC()
    param_grid = {'C': [1, 10, 100],
                  'kernel': ['poly', 'rbf']}

    try:
        classifier, score = model_selection(classifier,
                                            param_grid,
                                            x_values,
                                            y_values)
    except ValueError:
        state.set('support_vector_classification_score_reward',
                  config.MIN_REWARD)
        return state, config.MIN_REWARD, ActionInfo(action_name=_ACTION_NAME,
                                                    action_fn=_support_vector_classification,
                                                    model=None,
                                                    raised_exception=True)

    update_state_score(state, score)
    reward = calculate_score_reward(score)
    state.set('support_vector_classification_score_reward', reward)
    return state, reward, ActionInfo(action_name=_ACTION_NAME,
                                     action_fn=_support_vector_classification,
                                     model=classifier,
                                     raised_exception=False)


support_vector_classification: Action[SVC] = _support_vector_classification
