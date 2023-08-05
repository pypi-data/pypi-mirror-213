"""
FeaturesSet abstract class module
"""

from abc import ABC
from dataclasses import Field, fields
import numpy as np
from numpy.typing import NDArray

KnownFeaturesList = list[tuple[str, float | int | str]]


class FeaturesSet(ABC):
    """
    Abstract base class for FeaturesSets
    """

    def list_known_features(self) -> KnownFeaturesList:
        """
        Lists fields that have values different from default (unknown state attribute)

        Returns:
            KnownFeaturesList: list of non-default values
        """
        known_features = []
        for field in fields(self):
            value = getattr(self, field.name)
            if field.default != value:
                known_features.append((field.name, value))

        return known_features

    def as_gymnasium_space(self) -> dict:
        """
        Features as Gymnasium space

        Returns:
            dict: dictionary of features and their Gymnasium spaces
        """
        return {field.name: field.metadata['gym_space'] for field in fields(self)}

    def as_features_dict(self) -> dict:
        """
        Features values as dictionary

        Returns:
            dict: dictionary with features values
        """
        return {field.name: self.__get_feature_value(field) for field in fields(self)}

    def __array__(self):
        return np.concatenate([self.__get_feature_value(field) for field in fields(self)])

    def __get_feature_value(self, _field: Field) -> NDArray[np.float64]:
        get_value_fn = _field.metadata['get_value_fn']
        field_value = getattr(self, _field.name)
        if get_value_fn is None:
            return np.array(field_value).reshape((1,))

        feature_value = get_value_fn(field_value)
        if isinstance(feature_value, np.ndarray):
            return feature_value

        return np.array(feature_value).reshape((1,))
