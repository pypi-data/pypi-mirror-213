from abc import ABC, abstractmethod
from dataclasses import dataclass
from ._k_number import KNumber


@dataclass
class KInt(KNumber):
    value: int

