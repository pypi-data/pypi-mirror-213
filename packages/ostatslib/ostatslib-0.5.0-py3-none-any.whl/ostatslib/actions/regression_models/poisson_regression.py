"""
Poisson regression module
"""

import operator
from pandas import DataFrame
from statsmodels.api import GLM, families
from statsmodels.genmod.generalized_linear_model import GLMResults
from statsmodels.tools.sm_exceptions import PerfectSeparationError
from ostatslib import config

from ostatslib.states import State
from ..action import Action, ActionInfo, ActionResult
from ..utils import (calculate_score_reward,
                     reward_cap,
                     interpretable_model,
                     split_response_from_explanatory_variables,
                     update_state_score,
                     validate_state)

_ACTION_NAME = "Poisson Regression"
_VALIDATIONS = [('response_variable_label', operator.truth, None),
                ('is_response_positive_values_only', operator.gt, 0),
                ('is_response_discrete', operator.gt, 0),
                ('log_rows_count', operator.lt, 0.81),
                ('poisson_regression_score_reward', operator.eq, 0)]


@validate_state(action_name=_ACTION_NAME, validator_fns=_VALIDATIONS)
@reward_cap
@interpretable_model
def _poisson_regression(state: State, data: DataFrame) -> ActionResult[GLMResults]:
    """
    Fits data to a poisson regression model.

    Args:
        state (State): current environment state
        data (DataFrame): data under analysis

    Returns:
        ActionResult[GLMResults]: action result
    """
    response_var, explanatory_vars = split_response_from_explanatory_variables(state,
                                                                               data)
    try:
        poisson_family = families.Poisson()
        regression: GLMResults = GLM(response_var,
                                     explanatory_vars,
                                     poisson_family).fit()
    except ValueError:
        state.set('poisson_regression_score_reward', config.MIN_REWARD)
        return __raised_exception_action_result(state)
    except PerfectSeparationError:
        state.set('does_poisson_regression_raises_perfect_separation_error', 1)
        state.set('poisson_regression_score_reward', config.MIN_REWARD)
        return __raised_exception_action_result(state)

    state.set('does_poisson_regression_raises_perfect_separation_error', -1)
    score = regression.pseudo_rsquared()
    reward = calculate_score_reward(score)
    state = update_state_score(state, score)
    state.set('poisson_regression_score_reward', reward)
    return state, reward, ActionInfo(action_name=_ACTION_NAME,
                                     action_fn=_poisson_regression,
                                     model=regression,
                                     raised_exception=False)


def __raised_exception_action_result(state):
    return state, config.MIN_REWARD, ActionInfo(action_name=_ACTION_NAME,
                                                action_fn=_poisson_regression,
                                                model=None,
                                                raised_exception=True)


poisson_regression: Action[GLMResults] = _poisson_regression
