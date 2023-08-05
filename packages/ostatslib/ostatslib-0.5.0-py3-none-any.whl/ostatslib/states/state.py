"""
State module
"""

from collections import ChainMap
from copy import deepcopy
from dataclasses import fields
from functools import cached_property
from itertools import chain
from numpy import concatenate, ndarray, array
from gymnasium.spaces import Dict
from ostatslib.states.analysis_features_set import AnalysisFeaturesSet
from ostatslib.states.data_features_set import DataFeaturesSet
from ostatslib.states.models_features_set import ModelsFeaturesSet
from ostatslib.states.features_set import KnownFeaturesList
from ostatslib.states.state_iterator import StateIterator
from ostatslib.states.utils import init_features_set


class State:
    """
    State class
    """

    def __init__(self,
                 data_features: DataFeaturesSet | None = None,
                 analysis_features: AnalysisFeaturesSet | None = None,
                 models_features: ModelsFeaturesSet | None = None) -> None:
        self.__features_sets = (
            init_features_set(analysis_features, AnalysisFeaturesSet),
            init_features_set(data_features, DataFeaturesSet),
            init_features_set(models_features, ModelsFeaturesSet)
        )

    def copy(self) -> 'State':
        """
        Deep copies State instance

        Returns:
            State: state instance deep copy
        """
        return deepcopy(self)

    def get(self, feature_key: str) -> str | int | float | bool:
        """
        Gets feature value by passing feature key (feature name).
        If feature is not found, returns NaN.

        Args:
            feature_key (str): feature key (name)

        Raises:
            AttributeError: raises error if feature is not found

        Returns:
            str | int | float | bool: feature value
        """
        for features_set in self.__features_sets:
            if hasattr(features_set, feature_key):
                return getattr(features_set, feature_key)

        raise AttributeError()

    def set(self, feature_key: str, value: str | int | float | bool) -> None:
        """
        Sets value to feature

        Args:
            feature_key (str): feature key (name)
            value (str | int | float | bool): value

        Raises:
            AttributeError: If feature is not found
        """
        for features_set in self.__features_sets:
            if hasattr(features_set, feature_key):
                return setattr(features_set, feature_key, value)

        raise AttributeError()

    @cached_property
    def keys(self) -> tuple[str]:
        """
        Returns features keys (names)

        Returns:
            list[str]: list of features keys (names)
        """
        keys = []
        for features_set in self.__features_sets:
            keys += [field.name for field in fields(features_set)]

        return tuple(keys)

    @property
    def features_vector(self) -> ndarray[float]:
        """
        Returns features vector

        Returns:
            ndarray: array of values
        """
        features_set_list = [array(features_set)
                             for features_set in self.__features_sets]
        return concatenate(features_set_list).flatten()

    @property
    def features_dict(self) -> dict[str, float | int | bool]:
        """
        Returns features dictionary

        Returns:
            ndarray: array of values
        """
        features_dicts = [features_set.as_features_dict()
                          for features_set in self.__features_sets]
        return dict(ChainMap(*features_dicts))

    def list_known_features(self) -> KnownFeaturesList:
        """
        Lists fields that have values different from default (unkown state attribute)

        Returns:
            KnownFeaturesList: list of non-default values
        """
        known_features_list = [features_set.list_known_features()
                               for features_set in self.__features_sets]
        return list(chain(*known_features_list))

    @cached_property
    def as_gymnasium_space(self) -> Dict:
        """
        Returns Gymnasium space Dict
        https://gymnasium.farama.org/api/spaces/composite/#dict

        Returns:
            Dict: Gymnasium space Dict
        """
        gym_spaces = [features_set.as_gymnasium_space()
                      for features_set in self.__features_sets]
        return Dict(dict(ChainMap(*gym_spaces)))

    def __iter__(self):
        return StateIterator(self)

    def __eq__(self, other: 'State') -> bool:
        return self is other or self.__check_if_features_match(other)

    def __check_if_features_match(self, other: 'State') -> bool:
        for key, value in self:
            if value != other.get(key):
                return False

        return True

    def __sub__(self, other: 'State'):
        diff_state: State = State()
        for key, value in self:
            if value != other.get(key):
                diff_state.set(key, value)

        return diff_state

    def __len__(self) -> int:
        return len(self.features_vector)
