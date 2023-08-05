"""
DBSCAN module
"""

import operator
import numpy as np
from kneed import KneeLocator
from pandas import DataFrame
from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_score
from sklearn.neighbors import NearestNeighbors

from ostatslib.states import State
from ..action import Action, ActionInfo, ActionResult
from ..utils import (calculate_score_reward,
                     reward_cap,
                     update_state_score,
                     validate_state)

_ACTION_NAME = "DBSCAN"
_VALIDATIONS = [('response_variable_label', operator.eq, ''),
                ('clusters_count', operator.eq, 0)]


@validate_state(action_name=_ACTION_NAME, validator_fns=_VALIDATIONS)
@reward_cap
def _dbscan(state: State, data: DataFrame) -> ActionResult[DBSCAN]:
    """
    Fits data to a DBSCAN cluster

    Args:
        state (State): current environment state
        data (DataFrame): data under analysis

    Returns:
        ActionResult[DBSCAN]: action result
    """
    max_curvature_point = __get_max_curvature_point(data)
    db_scan = DBSCAN(eps=max_curvature_point)
    db_scan.fit(data)

    if np.all(db_scan.labels_ == -1) or np.all(db_scan.labels_ == 0):
        score = 0
    else:
        score = silhouette_score(data, db_scan.labels_)

    reward: float = calculate_score_reward(score)
    update_state_score(state, score)
    return state, reward, ActionInfo(action_name=_ACTION_NAME,
                                     action_fn=_dbscan,
                                     model=db_scan,
                                     raised_exception=False)


def __get_max_curvature_point(data: DataFrame) -> float:
    n_rows, n_columns = data.shape
    if n_rows < 2 * n_columns:
        min_points = 5
    elif n_rows < 10 * n_columns:
        min_points = n_columns
    else:
        min_points = 2* n_columns

    neighbors_fit = NearestNeighbors(
        n_neighbors=min_points, metric='euclidean').fit(data)
    distances, _ = neighbors_fit.kneighbors(data)
    distances = np.sort(distances.sum(axis=1), axis=0)
    elbow_locator = KneeLocator(
        range(0, len(distances)),
        distances,
        curve="convex",
        direction="increasing",
        interp_method='polynomial')

    if elbow_locator.elbow_y is None:
        return 0.5

    return elbow_locator.elbow_y


dbscan: Action[DBSCAN] = _dbscan
