"""
ModelsFeaturesSet module
"""

from dataclasses import dataclass, field
from gymnasium.spaces import Box

from ostatslib.states.features_set import FeaturesSet


@dataclass(init=False)
class ModelsFeaturesSet(FeaturesSet):
    """
    Class to hold features extracted from models fitting attempts.
    """
    are_linear_model_regression_residuals_correlated: int = field(
        default=0,
        metadata={
            'gym_space': Box(-1, 1),
            'get_value_fn': None
        })

    are_linear_model_regression_residuals_heteroscedastic: float = field(
        default=0,
        metadata={
            'gym_space': Box(-1, 1),
            'get_value_fn': None
        })

    are_linear_model_regression_residuals_normally_distributed: float = field(
        default=0,
        metadata={
            'gym_space': Box(-1, 1),
            'get_value_fn': None
        })

    is_linear_model_regression_recursive_residuals_mean_zero: float = field(
        default=0,
        metadata={
            'gym_space': Box(-1, 1),
            'get_value_fn': None
        })

    does_poisson_regression_raises_perfect_separation_error: float = field(
        default=0,
        metadata={
            'gym_space': Box(-1, 1),
            'get_value_fn': None
        })

    decision_tree_regression_score_reward: float = field(
        default=0,
        metadata={
            'gym_space': Box(-1, 1),
            'get_value_fn': None
        })

    random_forest_regression_score_reward: float = field(
        default=0,
        metadata={
            'gym_space': Box(-1, 1),
            'get_value_fn': None
        })

    linear_regression_score_reward: float = field(
        default=0,
        metadata={
            'gym_space': Box(-1, 1),
            'get_value_fn': None
        })

    poisson_regression_score_reward: float = field(
        default=0,
        metadata={
            'gym_space': Box(-1, 1),
            'get_value_fn': None
        })

    support_vector_regression_score_reward: float = field(
        default=0,
        metadata={
            'gym_space': Box(-1, 1),
            'get_value_fn': None
        })

    linear_support_vector_regression_score_reward: float = field(
        default=0,
        metadata={
            'gym_space': Box(-1, 1),
            'get_value_fn': None
        })

    time_series_auto_arima_score_reward: float = field(
        default=0,
        metadata={
            'gym_space': Box(-1, 1),
            'get_value_fn': None
        })

    decision_tree_score_reward: float = field(
        default=0,
        metadata={
            'gym_space': Box(-1, 1),
            'get_value_fn': None
        })

    logistic_regression_score_reward: float = field(
        default=0,
        metadata={
            'gym_space': Box(-1, 1),
            'get_value_fn': None
        })

    support_vector_classification_score_reward: float = field(
        default=0,
        metadata={
            'gym_space': Box(-1, 1),
            'get_value_fn': None
        })

    linear_support_vector_classification_score_reward: float = field(
        default=0,
        metadata={
            'gym_space': Box(-1, 1),
            'get_value_fn': None
        })

    random_forest_score_reward: float = field(
        default=0,
        metadata={
            'gym_space': Box(-1, 1),
            'get_value_fn': None
        })
