#pylint: disable=too-few-public-methods
"""
State iterator module
"""


class StateIterator:
    """
    Iterator for State classes
    """

    def __init__(self, state) -> None:
        self.__state = state
        self.__features_keys_list = state.keys
        self.__index = 0

    def __next__(self) -> tuple[str, int | float | bool]:
        if self.__index < len(self.__features_keys_list):
            next_feature_key = self.__features_keys_list[self.__index]
            self.__index += 1
            return (next_feature_key, self.__state.get(next_feature_key))

        raise StopIteration()
