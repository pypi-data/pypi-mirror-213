"""
Time series using Auto Arima module

ref: https://www.machinelearningplus.com/time-series/arima-model-time-series-forecasting-python/
"""

import operator
from pandas import DataFrame, Series, to_datetime
from pmdarima import auto_arima, ARIMA as AUTOARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAXResults
import numpy as np
from ostatslib import config

from ostatslib.states import State
from ..action import Action, ActionInfo, ActionResult
from ..utils import (calculate_score_reward,
                     reward_cap,
                     interpretable_model,
                     split_response_from_explanatory_variables,
                     validate_state)

TRAINING_FRACTION: float = 0.9

_ACTION_NAME = "Time Series - SARIMAX"
_VALIDATIONS = [('response_variable_label', operator.truth, None),
                ('is_response_quantitative', operator.gt, 0),
                ('time_series_auto_arima_score_reward', operator.eq, 0)]


@validate_state(action_name=_ACTION_NAME, validator_fns=_VALIDATIONS)
@reward_cap
@interpretable_model
def _time_series_auto_arima(state: State,
                            data: DataFrame) -> ActionResult[SARIMAXResults]:
    """
    Fits data to an ARIMA model

    Args:
        state (State): current environment state
        data (DataFrame): data under analysis

    Returns:
        ActionResult[SARIMAXResults]: action result
    """
    if not __is_valid_state(state):
        return state, config.MIN_REWARD, ActionInfo(action_name=_ACTION_NAME,
                                                    action_fn=_time_series_auto_arima,
                                                    model=None,
                                                    raised_exception=False)

    y_data, x_data = __build_time_index_dataframes_for_y_and_x(state, data)
    data_length = len(y_data)
    training_split_index = int(data_length * TRAINING_FRACTION)
    y_training, y_testing = (y_data.iloc[:training_split_index],
                             y_data.iloc[training_split_index:])
    if x_data is None:
        x_training, x_testing = (None, None)
    else:
        x_training, x_testing = (x_data.iloc[:training_split_index],
                                 x_data.iloc[training_split_index:])

    auto_arima_model: AUTOARIMA = auto_arima(y_training, x_training)
    model: SARIMAXResults = auto_arima_model.arima_res_

    forecast: Series = model.forecast(data_length - training_split_index,
                                      exog=x_testing)
    score: float = 1 - \
        __calculate_mean_abs_percentage_error(forecast, y_testing)

    reward: float = __calculate_reward(state, model, score)
    return state, reward, ActionInfo(action_name=_ACTION_NAME,
                                     action_fn=_time_series_auto_arima,
                                     model=model,
                                     raised_exception=False)


def __is_valid_state(state: State) -> bool:
    if bool(state.get("time_convertible_variable")) and \
        state.get("is_response_quantitative") > 0 and \
            bool(state.get("response_variable_label")):
        return True

    return False


def __calculate_mean_abs_percentage_error(forecast: Series, y_testing: DataFrame) -> float:
    forecast_values = forecast.values.flatten()
    y_testing_values = y_testing.values.flatten()
    return np.mean(np.abs(forecast_values - y_testing_values)/np.abs(y_testing_values))


def __calculate_reward(state: State, model: SARIMAXResults, correlation_coef: float) -> float:
    reward = calculate_score_reward(correlation_coef)
    state.set('time_series_auto_arima_score_reward', reward)

    reward += __penalty_for_correlated_residuals(model)
    reward += __penalty_for_heteroskedasticity_residuals(model)
    reward += __penalty_for_non_normal_residuals(model)

    return reward


def __penalty_for_correlated_residuals(model: SARIMAXResults) -> float:
    lag_correlations = model.test_serial_correlation(method='ljungbox')[:, 1]
    max_corr = np.max(lag_correlations)

    if max_corr > 0.25:
        return -0.25

    return 0


def __penalty_for_heteroskedasticity_residuals(model) -> float:
    prob_h = model.test_heteroskedasticity(method='breakvar')[:, 1][0]

    if prob_h <= 0.1:
        return -0.1

    return 0


def __penalty_for_non_normal_residuals(model) -> float:
    prob_jb = model.test_normality(method='jarquebera')[:, 1][0]

    if prob_jb <= 0.1:
        return -0.25

    return 0


def __build_time_index_dataframes_for_y_and_x(
    state: State,
    data: DataFrame
) -> tuple[DataFrame, DataFrame | None]:
    y_values, x_data = split_response_from_explanatory_variables(state, data)
    time = to_datetime(x_data[state.get("time_convertible_variable")])

    if len(x_data.columns) == 1:
        x_data = None
    else:
        x_data = x_data.set_index(state.get("time_convertible_variable"))

    y_data = DataFrame({y_values.name: y_values.values}, index=time)

    return y_data, x_data


time_series_auto_arima: Action[SARIMAXResults] = _time_series_auto_arima
