from dataclasses import dataclass


@dataclass
class KString(str):
    value: str = ''

    def __lt__(self, other):
        return len(self.value) < len(other.value)

    def __gt__(self, other):
        return len(self.value) > len(other.value)

    def __le__(self, other):
        return len(self.value) <= len(other.value)

    def __ge__(self, other):
        return len(self.value) >= len(other.value)

    def __eq__(self, other):
        return len(self.value) == len(other.value)

