"""
split_response_from_explanatory_variables module
"""

from pandas import DataFrame, Series
from ostatslib.states import State


def split_response_from_explanatory_variables(state: State,
                                              data: DataFrame) -> tuple[Series, DataFrame]:
    """Split Dataframe in a response variable values Serie and 
    other potential explanatory variables values in another dataframe without response column

    Args:
        state (State): state
        data (DataFrame): dataframe

    Returns:
        tuple[Series, DataFrame]: response values serie and explanatory variables dataframe
    """
    response_var_label = state.get("response_variable_label")
    response_var = data[response_var_label]
    explanatory_vars = data.drop(response_var_label, axis=1)
    return response_var, explanatory_vars
