import pandas as pd

from typing import TypeVar, Generic
from dataclasses import dataclass

T = TypeVar('T', int, str, bool, float)


@dataclass
class KTimeSeries(Generic[T]):
    '''
    [ DESCRIPTION ]: Wrapper over pandas.DataFrame that supports four different
        types of indices: integers, floats, booleans and strings. The
        implementation also includes type hints for clarity.

    [ NOTE ]: This implementation makes use of the generic type T to specify
        that the indices of the TimeSeries can be either int or str.

        The __init__ method takes in a dictionary with keys of type T and values
        of type float, which is then used to create a pandas.Series object.

        The __getitem__ and __setitem__ methods allow for getting and setting
        values using the TimeSeries object's keys, while the __repr__, __len__,
        keys, values, and items methods provide some additional convenience
        methods for working with the TimeSeries object.
    '''

    def __init__(self, data: dict[T, float]):
        self._data = pd.Series(data)

    def __getitem__(self, key: T) -> float:
        return self._data[key]

    def __setitem__(self, key: T, value: float) -> None:
        self._data[key] = value

    def __repr__(self) -> str:
        return self._data.__repr__()

    def __len__(self) -> int:
        return len(self._data)

    def keys(self):
        return self._data.keys()

    def values(self):
        return self._data.values()

    def items(self):
        return self._data.items()
