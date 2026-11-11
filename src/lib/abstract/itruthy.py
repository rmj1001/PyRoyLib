from abc import ABC, abstractmethod


class ITruthy(ABC):
    @abstractmethod
    def __bool__(self) -> bool:
        """Return boolean representation"""

    @abstractmethod
    def __and__(self, other) -> bool:
        """Check if self and other are True"""

    @abstractmethod
    def __or__(self, other) -> bool:
        """Check if self or other True"""

    @abstractmethod
    def __xor__(self, other) -> bool:
        """Check self XOR other"""
