from abc import ABC, abstractmethod


class IRepr(ABC):
    @abstractmethod
    def __str__(self) -> str:
        """String representation of the object."""

    @abstractmethod
    def __bool__(self) -> bool:
        """Boolean representation of the object."""
