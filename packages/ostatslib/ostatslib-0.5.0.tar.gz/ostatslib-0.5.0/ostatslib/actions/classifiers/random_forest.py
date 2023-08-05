"""
Random Forest module
"""

import operator
from pandas import DataFrame
from sklearn.ensemble import RandomForestClassifier
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

_ACTION_NAME = "Random Forest"
_VALIDATIONS = [('response_variable_label', operator.truth, None),
                ('is_response_discrete', operator.gt, 0),
                ('response_unique_values_ratio', operator.ne, 0),
                ('response_unique_values_ratio', operator.lt, 0.1),
                ('random_forest_score_reward', operator.eq, 0)]


@validate_state(action_name=_ACTION_NAME, validator_fns=_VALIDATIONS)
@reward_cap
@opaque_model
def _random_forest(state: State, data: DataFrame) -> ActionResult[RandomForestClassifier]:
    """
    Fits data to a random forest classifier

    Args:
        state (State): current environment state
        data (DataFrame): data under analysis

    Returns:
        ActionResult[RandomForestClassifier]: action result
    """
    y_values, x_values = split_response_from_explanatory_variables(state, data)
    classifier: RandomForestClassifier = RandomForestClassifier()
    param_grid = {'criterion': ['gini', 'entropy', 'log_loss'],
                  'max_features': ['sqrt', 'log2'],
                  'max_depth': [x_values.shape[1], 20]}

    try:
        classifier, score = model_selection(classifier,
                                            param_grid,
                                            x_values,
                                            y_values)
    except ValueError:
        state.set('random_forest_score_reward', config.MIN_REWARD)
        return state, config.MIN_REWARD, ActionInfo(action_name=_ACTION_NAME,
                                                    action_fn=_random_forest,
                                                    model=None,
                                                    raised_exception=True)

    update_state_score(state, score)
    reward = calculate_score_reward(score)
    state.set('random_forest_score_reward', reward)
    return state, reward, ActionInfo(action_name=_ACTION_NAME,
                                     action_fn=_random_forest,
                                     model=classifier,
                                     raised_exception=False)


random_forest: Action[RandomForestClassifier] = _random_forest
