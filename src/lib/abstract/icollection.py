from abc import ABC, abstractmethod
from collections.abc import Iterable

from abstract.irepr import IRepr


class ContainerException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class ICollection[T](ABC, IRepr[T]):
    value: T

    def __init__(self, value: T):
        self.value: T = value

    @abstractmethod
    def __iter__(self) -> Iterable[T]:
        """Iterate over contents"""

    @abstractmethod
    def __len__(self) -> int:
        """Length of contents, or 1 if contents aren't a Sized iterable, or 0 if contents are None."""

    @abstractmethod
    def __contains__(self, item) -> bool:
        """Check if contents equal item, or if the contents contain the item"""

    @abstractmethod
    def take(self) -> T:
        """Remove the contents and return it"""

    @abstractmethod
    def replace(self, new_value: T) -> ICollection[T]:
        """Replace the contents and return self"""

    @abstractmethod
    def peek(self) -> T:
        """Return the contents without removing it"""
