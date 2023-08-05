"""
DataFeaturesSets module
"""

from functools import cache
from dataclasses import dataclass, field
from gymnasium.spaces import Box, MultiBinary
import numpy as np
from numpy.typing import NDArray

from ostatslib.states.features_set import FeaturesSet


MAX_INFERRED_DTYPE_INDEX = 10

INFERRABLE_DTYPES = {
    "string": 10,
    "bytes": 1,
    "floating": 2,
    "integer": 3,
    "mixed-integer": 4,
    "mixed-integer-float": 5,
    "decimal": 2,
    "complex": 2,
    "categorical": 6,
    "boolean": 7,
    "datetime64": 8,
    "datetime": 8,
    "date": 8,
    "timedelta64": 8,
    "timedelta": 8,
    "time": 8,
    "period": 8,
    "mixed": 9,
    "unknown-array": 0,
}


@cache
def _map_inferred_dtype_to_binary_array(inferred_dtype: str) -> NDArray[np.float64]:
    feature_vector = np.zeros(10)
    dtype_index = INFERRABLE_DTYPES[inferred_dtype]
    feature_vector[dtype_index] = 1
    return feature_vector


@dataclass(init=False)
class DataFeaturesSet(FeaturesSet):
    """
    Class to hold features extracted from a dataset.
    """
    log_rows_count: float = field(
        default=0,
        metadata={
            'gym_space': Box(0, 1),
            'get_value_fn': None
        })

    response_unique_values_ratio: float = field(
        default=0,
        metadata={
            'gym_space': Box(0, 1),
            'get_value_fn': None
        })

    response_inferred_dtype: str = field(
        default="unknown-array",
        metadata={
            'gym_space': MultiBinary(MAX_INFERRED_DTYPE_INDEX),
            'get_value_fn': _map_inferred_dtype_to_binary_array
        })

    is_response_dichotomous: int = field(
        default=0,
        metadata={
            'gym_space': Box(-1, 1),
            'get_value_fn': None
        })

    is_response_quantitative: int = field(
        default=0,
        metadata={
            'gym_space': Box(-1, 1),
            'get_value_fn': None
        })

    is_response_discrete: int = field(
        default=0,
        metadata={
            'gym_space': Box(-1, 1),
            'get_value_fn': None
        })

    is_response_positive_values_only: int = field(
        default=0,
        metadata={
            'gym_space': Box(-1, 1),
            'get_value_fn': None
        })
