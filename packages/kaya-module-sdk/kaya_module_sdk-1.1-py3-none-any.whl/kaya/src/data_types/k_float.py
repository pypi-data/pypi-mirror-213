from dataclasses import dataclass
from ._k_number import KNumber


@dataclass
class KFloat(KNumber):
    value: int


