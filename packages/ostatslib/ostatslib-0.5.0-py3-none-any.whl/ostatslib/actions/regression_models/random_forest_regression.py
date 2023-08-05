"""
Random Forest Regression module
"""

import operator
from pandas import DataFrame
from sklearn.ensemble import RandomForestRegressor

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

_ACTION_NAME = "Random Forest Regression"
_VALIDATIONS = [('is_response_quantitative', operator.gt, 0),
                ('is_response_dichotomous', operator.lt, 0),
                ('response_variable_label', operator.truth, None),
                ('random_forest_regression_score_reward', operator.eq, 0),
                ('response_unique_values_ratio', operator.gt, 0.5)]


@validate_state(action_name=_ACTION_NAME, validator_fns=_VALIDATIONS)
@reward_cap
@opaque_model
def _random_forest_regression(state: State,
                              data: DataFrame) -> ActionResult[RandomForestRegressor]:
    """
    Fits data to a random forest regressor

    Args:
        state (State): current environment state
        data (DataFrame): data under analysis

    Returns:
        ActionResult[RandomForestRegressor]: action result
    """
    y_values, x_values = split_response_from_explanatory_variables(state, data)
    regressor: RandomForestRegressor = RandomForestRegressor()
    param_grid = {'criterion': ['squared_error', 'friedman_mse'],
                  'max_features': ['sqrt', 'log2'],
                  'max_depth': [x_values.shape[1], 20]}

    try:
        regressor, score = model_selection(regressor,
                                           param_grid,
                                           x_values,
                                           y_values)
    except ValueError:
        state.set('random_forest_regression_score_reward', config.MIN_REWARD)
        return state, config.MIN_REWARD, ActionInfo(action_name=_ACTION_NAME,
                                                    action_fn=_random_forest_regression,
                                                    model=None,
                                                    raised_exception=True)

    update_state_score(state, score)
    reward = calculate_score_reward(score)
    state.set('random_forest_regression_score_reward', reward)
    return state, reward, ActionInfo(action_name=_ACTION_NAME,
                                     action_fn=_random_forest_regression,
                                     model=regressor,
                                     raised_exception=False)


random_forest_regression: Action[RandomForestRegressor] = _random_forest_regression
