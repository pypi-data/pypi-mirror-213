"""
time_convertible_variable_search module
"""

from pandas import DataFrame
from pandas.api.types import infer_dtype

from ostatslib import config
from ostatslib.actions.utils import split_response_from_explanatory_variables
from ostatslib.states import State
from ..action import Action, ActionInfo, ActionResult

_ACTION_NAME = "Time Convertible Variable Search"


ORDERED_LIST_OF_POSSIBLE_TIME_DTYPES = [
    "datetime64", "datetime", "date",
    "period",
    "time",
    "timedelta64", "timedelta",
]


def _time_convertible_variable_search(state: State, data: DataFrame) -> ActionResult[None]:
    """
    Gets log rows count: log(#rows)/c, where c is a compression constant

    Args:
        state (State): state
        data (DataFrame): data

    Returns:
        ActionResult[None]: action result
    """
    if bool(state.get("response_variable_label")):
        variables_dataframe: DataFrame = split_response_from_explanatory_variables(state,
                                                                                   data)[1]
    else:
        variables_dataframe = data

    date_convertible_variable = __date_variable_search(variables_dataframe)

    reward: float = __calculate_reward(state, date_convertible_variable)
    __update_state(state, date_convertible_variable)
    return state, reward, ActionInfo(action_name=_ACTION_NAME,
                                     action_fn=_time_convertible_variable_search,
                                     model=None,
                                     raised_exception=False)


def __date_variable_search(variables_dataframe: DataFrame) -> str | None:
    time_related_variables: list[tuple[str, str]] = []

    for var_name, values in variables_dataframe.items():
        inferred_dtype_name: str = infer_dtype(values)
        if inferred_dtype_name in ORDERED_LIST_OF_POSSIBLE_TIME_DTYPES:
            time_related_variables.append((var_name, inferred_dtype_name))

    if not time_related_variables:
        return None

    if len(time_related_variables) == 1:
        return time_related_variables[0][0]

    return __select_best_time_related_variable(time_related_variables)


def __select_best_time_related_variable(time_related_variables) -> str:
    for time_dtype in ORDERED_LIST_OF_POSSIBLE_TIME_DTYPES:
        for var_name, inferred_dtype_name in time_related_variables:
            if time_dtype == inferred_dtype_name:
                return var_name

    return time_related_variables[0]


def __calculate_reward(state: State, date_convertible_variable: str | None) -> float:
    if state.get("time_convertible_variable") == date_convertible_variable:
        return config.MIN_REWARD

    if date_convertible_variable == "":
        return config.MAX_EXPLORATORY_REWARD * 0.5

    return config.MAX_EXPLORATORY_REWARD


def __update_state(state: State, date_convertible_variable: str | None) -> State:
    state.set("time_convertible_variable", date_convertible_variable)
    return state


time_convertible_variable_search: Action[None] = _time_convertible_variable_search
