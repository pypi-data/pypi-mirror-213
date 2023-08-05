"""
AnalysisFeaturesSet module
"""

from dataclasses import dataclass, field
from typing import Literal
from gymnasium.spaces import Discrete, Box

from ostatslib.states.features_set import FeaturesSet


def time_convertible_variable_to_feature(time_convertible_variable: str) -> bool | Literal[-1]:
    """
    Returns -1 if field is set to None, else returns boolean from string.
    Empty string = False and any valid string = True

    Args:
        time_convertible_variable (str): analysis features set field

    Returns:
        bool: time_convertible_variable feature value
    """
    if time_convertible_variable is None:
        return -1

    return bool(time_convertible_variable)


@dataclass(init=False)
class AnalysisFeaturesSet(FeaturesSet):
    """
    Class to hold analysis features.
    """
    response_variable_label: str = field(
        default="result",
        metadata={
            'gym_space': Discrete(2),
            'get_value_fn': bool
        })

    score: float = field(
        default=0,
        metadata={
            'gym_space': Box(0, 1),
            'get_value_fn': None
        })

    clusters_count: int = field(
        default=0,
        metadata={
            'gym_space': Box(0, 10),
            'get_value_fn': None
        })

    time_convertible_variable: str = field(
        default="",
        metadata={
            'gym_space': Box(-1, 1),
            'get_value_fn': time_convertible_variable_to_feature
        })
