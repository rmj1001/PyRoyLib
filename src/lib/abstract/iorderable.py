from abc import ABC, abstractmethod


class IOrderable(ABC):
    @abstractmethod
    def __ge__(self, other) -> bool:
        """Compare self >= other"""

    @abstractmethod
    def __gt__(self, other) -> bool:
        """Compare self > other"""

    @abstractmethod
    def __le__(self, other) -> bool:
        """Compare self <= other"""

    @abstractmethod
    def __lt__(self, other) -> bool:
        """Compare self < other"""
