from abc import ABC, abstractmethod

class IEquality(ABC):
    @abstractmethod
    def __eq__(self, other) -> bool:
        """Check self == other"""

    @abstractmethod
    def __ne__(self, other) -> bool:
        """Check self != other"""
