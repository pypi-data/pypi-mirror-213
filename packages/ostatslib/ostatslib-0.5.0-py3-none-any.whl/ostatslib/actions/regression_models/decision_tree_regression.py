"""
Decision Tree Regression module
"""

import operator
from pandas import DataFrame
from sklearn.tree import DecisionTreeRegressor

from ostatslib import config
from ostatslib.states import State
from ..action import Action, ActionInfo, ActionResult
from ..utils import (calculate_score_reward,
                     reward_cap,
                     comprehensible_model,
                     split_response_from_explanatory_variables,
                     update_state_score,
                     validate_state,
                     model_selection)

_ACTION_NAME = "Decision Tree Regression"
_VALIDATIONS = [('is_response_quantitative', operator.gt, 0),
                ('is_response_dichotomous', operator.lt, 0),
                ('response_variable_label', operator.truth, None),
                ('decision_tree_regression_score_reward', operator.eq, 0)]


@validate_state(action_name=_ACTION_NAME, validator_fns=_VALIDATIONS)
@reward_cap
@comprehensible_model
def _decision_tree_regression(state: State,
                              data: DataFrame) -> ActionResult[DecisionTreeRegressor]:
    """
    Fits data to a decision tree regressor

    Args:
        state (State): current environment state
        data (DataFrame): data under analysis

    Returns:
        ActionResult[DecisionTreeRegressor]: action result
    """
    y_values, x_values = split_response_from_explanatory_variables(state, data)
    regressor: DecisionTreeRegressor = DecisionTreeRegressor()
    param_grid = {'criterion': ['squared_error', 'friedman_mse', 'absolute_error'],
                  'max_features': ['sqrt', 'log2', None]}

    try:
        regressor, score = model_selection(regressor,
                                           param_grid,
                                           x_values,
                                           y_values)
    except ValueError:
        state.set('decision_tree_regression_score_reward', config.MIN_REWARD)
        return state, config.MIN_REWARD, ActionInfo(action_name=_ACTION_NAME,
                                                    action_fn=_decision_tree_regression,
                                                    model=None,
                                                    raised_exception=True)

    update_state_score(state, score)
    reward = calculate_score_reward(score)
    state.set('decision_tree_regression_score_reward', reward)
    return state, reward, ActionInfo(action_name=_ACTION_NAME,
                                     action_fn=_decision_tree_regression,
                                     model=regressor,
                                     raised_exception=False)


decision_tree_regression: Action[DecisionTreeRegressor] = _decision_tree_regression
