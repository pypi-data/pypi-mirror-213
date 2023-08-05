"""
Action type definitions module
"""

from typing import Callable, Generic, TypeVar, TypedDict

from pandas import DataFrame
from sklearn.base import BaseEstimator
from statsmodels.base.model import LikelihoodModelResults, Results
from statsmodels.tsa.base.tsa_model import TimeSeriesModelResults
from ostatslib.states import State

TModel = TypeVar('TModel', # pylint: disable=invalid-name
                 None,
                 BaseEstimator,
                 LikelihoodModelResults,
                 Results,
                 TimeSeriesModelResults)


class ActionInfo(TypedDict, Generic[TModel], total=False):
    """
    Action results information
    """
    action_name: str
    action_fn: 'Action[TModel]'
    model: None | TModel
    raised_exception: bool
    state_delta: State


ActionResult = tuple[State, float, ActionInfo[TModel]]

Action = Callable[[State, DataFrame], ActionResult[TModel]]
