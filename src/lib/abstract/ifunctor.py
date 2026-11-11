from abc import ABC, abstractmethod
from typing import Callable


class IFunctor[T](ABC):
    value: T

    @abstractmethod
    def flatten(self) -> IFunctor[T]:
        """Flatten the contained value so that self.value is of type T, not nested Functors"""

    @abstractmethod
    def map(self, fn: Callable[[T], T]) -> T:
        """Apply fn to the contained value, changing it to fn's returned value"""

    @abstractmethod
    def flatmap(self, fn: Callable[[T], T]) -> T:
        """Flatten self.value, then map fn to it"""
