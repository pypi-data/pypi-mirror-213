"""
Decision Tree module
"""

import operator
from pandas import DataFrame
from sklearn.tree import DecisionTreeClassifier
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

_ACTION_NAME = "Decision Tree"
_VALIDATIONS = [('response_variable_label', operator.truth, None),
                ('is_response_discrete', operator.gt, 0),
                ('decision_tree_score_reward', operator.eq, 0)]


@validate_state(action_name=_ACTION_NAME, validator_fns=_VALIDATIONS)
@reward_cap
@comprehensible_model
def _decision_tree(state: State, data: DataFrame) -> ActionResult[DecisionTreeClassifier]:
    """
    Fits data to a decision tree classifier

    Args:
        state (State): current environment state
        data (DataFrame): data under analysis

    Returns:
        ActionResult[DecisionTreeClassifier]: action result
    """
    y_values, x_values = split_response_from_explanatory_variables(state, data)
    classifier: DecisionTreeClassifier = DecisionTreeClassifier()
    param_grid = {'criterion': ['gini', 'entropy', 'log_loss'],
                  'max_features': ['sqrt', 'log2', None]}

    try:
        classifier, score = model_selection(classifier,
                                            param_grid,
                                            x_values,
                                            y_values)
    except ValueError:
        state.set('decision_tree_score_reward', config.MIN_REWARD)
        return state, config.MIN_REWARD, ActionInfo(action_name=_ACTION_NAME,
                                                    action_fn=_decision_tree,
                                                    model=None,
                                                    raised_exception=True)

    update_state_score(state, score)
    reward = calculate_score_reward(score)
    state.set('decision_tree_score_reward', reward)
    return state, reward, ActionInfo(action_name=_ACTION_NAME,
                                     action_fn=_decision_tree,
                                     model=classifier,
                                     raised_exception=False)


decision_tree: Action[DecisionTreeClassifier] = _decision_tree
