"""
Init features set helper function module
"""


from typing import Type
from ostatslib.states.analysis_features_set import AnalysisFeaturesSet
from ostatslib.states.data_features_set import DataFeaturesSet
from ostatslib.states.models_features_set import ModelsFeaturesSet


FeaturesSetInstance = (
    AnalysisFeaturesSet |
    DataFeaturesSet |
    ModelsFeaturesSet
)


def init_features_set(features_instance: FeaturesSetInstance | None,
                      features_set_class: Type[FeaturesSetInstance]) -> FeaturesSetInstance:
    """
    Helper function to initialize features sets dataclasses

    Args:
        features_instance (FeaturesSetInstance | None): feature set instance or none
        features_set_class (Type[FeaturesSetInstance]): feature set class

    Returns:
        FeaturesSetInstance: features set instance
    """
    return features_instance if features_instance is not None else features_set_class()
