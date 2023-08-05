"""
Actions validators module
"""

from functools import wraps
from inspect import signature
from typing import Any, Callable
from pandas import DataFrame
from ostatslib import config
from ostatslib.states import State
from ..action import Action, ActionInfo, ActionResult, TModel


def validate_state(action_name: str, validator_fns: list[tuple[str, Callable[..., bool], Any]]):
    """
    Validate state before executing action

    Args:
        action_name (str): action name
        validator_fns (list[tuple[str, Callable[..., bool], Any]]): list of validation tuples
    """

    def actual_validator(action_function: Action[TModel]) -> Action[TModel]:

        wraps(action_function)

        def function_wrapper(state: State, data: DataFrame) -> ActionResult[TModel]:
            for (feature_key, operator_fn, value) in validator_fns:
                if not _is_valid(state, feature_key, operator_fn, value):
                    return _default_invalid_state_return(state, action_name, action_function)
            return action_function(state, data)

        return function_wrapper

    return actual_validator


def _is_valid(state: State,
              feature_key: str,
              operator_fn: Callable[..., bool], value: Any) -> bool:
    if value is None:
        operator_fn_signature = signature(operator_fn)
        if len(operator_fn_signature.parameters) == 1:
            return operator_fn(state.get(feature_key))

    return operator_fn(state.get(feature_key), value)


def _default_invalid_state_return(state: State,
                                  action_name: str,
                                  action_function: Action[TModel]) -> ActionResult[TModel]:
    return state, config.MIN_REWARD, ActionInfo(action_name=action_name,
                                                action_fn=action_function,
                                                model=None,
                                                raised_exception=False)
