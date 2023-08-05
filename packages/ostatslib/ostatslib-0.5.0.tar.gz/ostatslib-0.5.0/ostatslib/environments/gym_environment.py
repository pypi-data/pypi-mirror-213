"""
GymEnvironment module
"""

from typing import Any
from numpy import ndarray
from pandas import DataFrame
from gymnasium import Env
from gymnasium.spaces import Dict
from ostatslib import config
from ostatslib.actions import ActionsSpace
from ostatslib.actions.action import ActionInfo
from ostatslib.actions.actions_space import _invalid_action_step
from ostatslib.states import State
from .utils import generate_training_dataset

ObsType = Dict


class GymEnvironment(Env):
    """
    Statistical environment implemented as Gymnasium environment
    """

    __state: State
    __data: DataFrame

    def __init__(self) -> None:
        self.__init_state_and_data()
        self.observation_space = State().as_gymnasium_space
        self.action_space: ActionsSpace = ActionsSpace()
        self.reward_range = config.REWARD_RANGE
        self.__steps_taken = 0

    def render(self) -> None:
        print("Render has no effect yet")

    def reset(self,
              *,
              seed: int | None = None,
              options: dict[str, Any] | None = None) -> tuple[dict, dict]:
        self.__init_state_and_data()
        self.__steps_taken = 0
        super().reset(seed=seed, options=options)
        return self.__state.features_dict, ActionInfo(action_name='Invalid Action',
                                                      action_fn=_invalid_action_step,
                                                      model=None,
                                                      raised_exception=False)

    def step(self, action: ndarray) -> tuple[dict, float, bool, bool, dict]:
        action_fn = self.action_space.get_action_by_encoding(action)
        state, reward, info = action_fn(self.__state.copy(), self.__data)

        self.__steps_taken += 1
        info["state_delta"] = state - self.__state
        self.__state = state
        observation = state.features_dict
        terminated = self.__is_done(state, reward)

        return observation, reward, terminated, False, info

    def set_data(self, data: DataFrame) -> None:
        """
        Set dataset to be used until next reset

        Args:
            data (DataFrame): dataset
        """
        self.__data = data

    def set_state(self, state: State) -> None:
        """
        Set analysis state

        Args:
            state (State): State
        """
        self.__state = state

    def __is_done(self, state: State, reward: float) -> bool:
        return (state.get("score") > config.MIN_ACCEPTED_SCORE and reward > config.MAX_REWARD/2)\
            or self.__steps_taken >= config.MAX_STEPS

    def __init_state_and_data(self):
        self.__data, self.__state = generate_training_dataset()
