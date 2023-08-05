"""
Penn ML Benchmarks datasets module
"""

from random import choice
from pandas import DataFrame
import pmlb

from ostatslib.states import State

PMLB_CACHE_FOLDER = './.pmlb_cache'
SKIP_DATASETS = ['poker', '1595_poker',
                 '1191_BNG_pbc', '1196_BNG_pharynx', 'kddcup']


def generate_from_pmlb() -> tuple[DataFrame, State]:
    """
    Randomly selects a dataset from Penn Machine Learning Benchmarks

    Returns:
        tuple[DataFrame, State]: dataset and initial state
    """
    pmlb_gen_fn = choice([
        __from_classification_datasets,
        __from_regression_datasets
    ])
    return pmlb_gen_fn()


def __from_classification_datasets() -> tuple[DataFrame, State]:
    dataset_name: str = SKIP_DATASETS[0]
    while dataset_name in SKIP_DATASETS:
        dataset_name = choice(pmlb.classification_dataset_names)
    return __fetch(dataset_name)


def __from_regression_datasets() -> tuple[DataFrame, State]:
    dataset_name: str = SKIP_DATASETS[0]
    while dataset_name in SKIP_DATASETS:
        dataset_name = choice(pmlb.regression_dataset_names)
    return __fetch(dataset_name)


def __fetch(dataset_name: str) -> tuple[DataFrame, State]:
    dataset = pmlb.fetch_data(dataset_name, local_cache_dir=PMLB_CACHE_FOLDER)
    if isinstance(dataset, DataFrame):
        state = State()
        state.set('response_variable_label', 'target')
        return dataset, state

    raise ValueError(f'Could not fetch {dataset_name} from PMLB')
