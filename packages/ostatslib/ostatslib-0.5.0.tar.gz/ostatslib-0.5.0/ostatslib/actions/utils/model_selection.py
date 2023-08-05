"""
model_selection function module
"""

from typing import Mapping, Sequence
from pandas import DataFrame, Series
from sklearn.experimental import enable_halving_search_cv  # pylint: disable=unused-import
from sklearn.model_selection import HalvingGridSearchCV

from ..action import TModel


def model_selection(
        classifier: TModel,
        param_grid: Mapping | dict[str, list[int | float]] | Sequence[dict],
        X: DataFrame,
        y: Series
) -> tuple[TModel, float]:
    """
    Runs model selection strategy

    Args:
        classifier (TModel): classifier or regressor model
        param_grid (Mapping | dict[str, list[int  |  float]] | Sequence[dict]): hyper params
        X (DataFrame): variables values
        y (Series): response variable values

    Returns:
        tuple[TModel, float]: best model and its score
    """
    search = HalvingGridSearchCV(classifier,
                                 param_grid,
                                 cv=5,
                                 factor=2,
                                 n_jobs=None).fit(X, y)
    fitted_model: TModel = search.best_estimator_
    score = search.best_score_
    print(fitted_model, score)
    return fitted_model, score
