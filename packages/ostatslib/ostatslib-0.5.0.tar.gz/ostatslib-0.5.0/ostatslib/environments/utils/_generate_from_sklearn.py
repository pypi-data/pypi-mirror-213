"""
Generate datasets from SciKit Learn for agent training module

https://scikit-learn.org/stable/datasets.html

The following sklearn generated datasets functions may be applied later
as the agent states and actions evolves:

# "make_biclusters",
# "make_circles",
# "make_checkerboard",
# "make_friedman1",
# "make_friedman2",
# "make_friedman3",
# "make_gaussian_quantiles",
# "make_hastie_10_2",
# "make_low_rank_matrix",
# "make_moons",
# "make_multilabel_classification",
# "make_s_curve",
# "make_sparse_coded_signal",
# "make_sparse_spd_matrix",
# "make_sparse_uncorrelated",
# "make_spd_matrix",
# "make_swiss_roll",
"""

from random import choice, getrandbits
from pandas import DataFrame
import sklearn.datasets as sklearn_dts
import numpy as np

from ostatslib.states import State


def generate_from_sklearn() -> tuple[DataFrame, State]:
    """
    Generates a dataset from sklearn's toy datasets or generated
    https://scikit-learn.org/stable/datasets.html

    Returns:
        tuple[DataFrame, State]: dataset and initial state
    """
    sklearn_gen_fn = choice([_from_toy, __from_generated, __from_cluster])
    return sklearn_gen_fn()


_TOY_FUNCTIONS = (
    sklearn_dts.load_iris,
    sklearn_dts.load_diabetes,
    sklearn_dts.load_digits,
    sklearn_dts.load_wine,
    sklearn_dts.load_breast_cancer
)


def _from_toy(toy_fns=_TOY_FUNCTIONS) -> tuple[DataFrame, State]:
    sample_toy_fn = choice(toy_fns)
    x_dataframe, y_series = sample_toy_fn(return_X_y=True, as_frame=True)
    data = x_dataframe.join(y_series)
    state = State()
    state.set('response_variable_label', y_series.name)
    return data, state


def __from_generated() -> tuple[DataFrame, State]:
    sample_gen_fn = choice([
        __make_classification,
        __make_regression
    ])
    x_values, y_values = sample_gen_fn()

    data = DataFrame(x_values)
    data['target'] = y_values

    state = State()
    state.set('response_variable_label', 'target')

    return data, state


def __from_cluster() -> tuple[DataFrame, State]:
    n_centers, xy_tuple = __make_blobs()
    data = DataFrame(xy_tuple[0])
    state = State()
    state.set('response_variable_label', '')

    if bool(getrandbits(1)):
        state.set('clusters_count', n_centers)

    return data, state


def __get_n_samples_and_features() -> tuple[int, int]:
    n_samples = np.random.randint(20, 1000)
    n_features = np.random.randint(5, 50)
    return n_samples, n_features


def __make_regression():
    n_samples, n_features = __get_n_samples_and_features()
    noise = np.random.random() + 0.001
    return sklearn_dts.make_regression(
        n_samples=n_samples,
        n_features=n_features,
        noise=noise
    )


def __make_classification():
    n_informative = np.random.randint(3, 20)
    n_redundant = np.random.randint(2, 20)
    n_repeated = np.random.randint(2, 20)
    n_samples = np.random.randint(20, 1000)
    sum_features = n_informative + n_redundant + n_repeated
    n_features = np.random.randint(sum_features, sum_features * 2)
    n_classes = np.random.randint(n_informative, 2**(n_informative - 1))
    return sklearn_dts.make_classification(
        n_samples=n_samples,
        n_features=n_features,
        n_informative=n_informative,
        n_redundant=n_redundant,
        n_repeated=n_repeated,
        n_classes=n_classes
    )


def __make_blobs():
    n_samples, n_features = __get_n_samples_and_features()
    n_centers = np.random.randint(2, 20)
    return n_centers, sklearn_dts.make_blobs(
        n_samples=n_samples,
        n_features=n_features,
        centers=n_centers,
        cluster_std=0.5
    )
