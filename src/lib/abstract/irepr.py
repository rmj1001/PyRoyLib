from abc import ABC, abstractmethod


class IRepr(ABC):
    @abstractmethod
    def __repr__(self) -> str:
        """String representation of the object."""
