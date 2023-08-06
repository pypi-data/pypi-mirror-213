from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class KNumber(ABC):
    value: int

#   @abstractmethod
    def __add__(self, other):
        if isinstance(other, KNumber):
            return KNumber(self.value + other.value)
        elif isinstance(other, int) or isinstance(other, float):
            return KNumber(self.value + other)
        else:
            raise TypeError(
                'Unsupported operand type(s) for +: {} and {}'
                .format(type(self), type(other))
            )

#   @abstractmethod
    def __sub__(self, other):
        if isinstance(other, KNumber):
            return KNumber(self.value - other.value)
        elif isinstance(other, int) or isinstance(other, float):
            return KNumber(self.value - other)
        else:
            raise TypeError(
                'Unsupported operand type(s) for -: {} and {}'
                .format(type(self), type(other))
            )

#   @abstractmethod
    def __mul__(self, other):
        if isinstance(other, KNumber):
            return KNumber(self.value * other.value)
        elif isinstance(other, int) or isinstance(other, float):
            return KNumber(self.value * other)
        else:
            raise TypeError(
                'Unsupported operand type(s) for *: {} and {}'
                .format(type(self), type(other))
            )

#   @abstractmethod
    def __truediv__(self, other):
        if isinstance(other, KNumber):
            return KNumber(self.value / other.value)
        elif isinstance(other, int) or isinstance(other, float):
            return KNumber(self.value / other)
        else:
            raise TypeError(
                'Unsupported operand type(s) for /: {} and {}'
                .format(type(self), type(other))
            )

#   @abstractmethod
    def __floordiv__(self, other):
        if isinstance(other, KNumber):
            return KNumber(self.value // other.value)
        elif isinstance(other, int) or isinstance(other, float):
            return KNumber(self.value // other)
        else:
            raise TypeError(
                'Unsupported operand type(s) for //: {} and {}'
                .format(type(self), type(other))
            )

#   @abstractmethod
    def __mod__(self, other):
        if isinstance(other, KNumber):
            return KNumber(self.value % other.value)
        elif isinstance(other, int) or isinstance(other, float):
            return KNumber(self.value % other)
        else:
            raise TypeError(
                'Unsupported operand type(s) for %: {} and {}'
                .format(type(self), type(other))
            )

#   @abstractmethod
    def __pow__(self, other):
        if isinstance(other, KNumber):
            return KNumber(self.value ** other.value)
        elif isinstance(other, int) or isinstance(other, float):
            return KNumber(self.value ** other)
        else:
            raise TypeError(
                'Unsupported operand type(s) for **: {} and {}'
                .format(type(self), type(other))
            )

#   @abstractmethod
    def __lt__(self, other):
        if isinstance(other, KNumber):
            return self.value < other.value
        elif isinstance(other, int) or isinstance(other, float):
            return self.value < other
        else:
            raise TypeError(
                'Unsupported operand type(s) for <: {} and {}'
                .format(type(self), type(other))
            )

#   @abstractmethod
    def __gt__(self, other):
        if isinstance(other, KNumber):
            return self.value > other.value
        elif isinstance(other, int) or isinstance(other, float):
            return self.value > other
        else:
            raise TypeError(
                'Unsupported operand type(s) for >: {} and {}'
                .format(type(self), type(other))
            )

#   @abstractmethod
    def __le__(self, other):
        if isinstance(other, KNumber):
            return self.value <= other.value
        elif isinstance(other, int) or isinstance(other, float):
            return self.value <= other
        else:
            raise TypeError(
                'Unsupported operand type(s) for <=: {} and {}'
                .format(type(self), type(other))
            )

#   @abstractmethod
    def __ge__(self, other):
        if isinstance(other, KNumber):
            return self.value >= other.value
        elif isinstance(other, int) or isinstance(other, float):
            return self.value >= other
        else:
            raise TypeError(
                'Unsupported operand type(s) for >=: {} and {}'
                .format(type(self), type(other))
            )

#   @abstractmethod
    def __eq__(self, other):
        if isinstance(other, KNumber):
            return self.value == other.value
        elif isinstance(other, int) or isinstance(other, float):
            return self.value == other
        else:
            raise TypeError(
                'Unsupported operand type(s) for ==: {} and {}'
                .format(type(self), type(other))
            )

# CODE DUMP
