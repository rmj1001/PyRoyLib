from abc import ABC, abstractmethod
from collections.abc import Iterator


class ICollection[T](ABC):
    @abstractmethod
    def __len__(self) -> int:
        """Length of collection"""

    @abstractmethod
    def __iter__(self) -> Iterator:
        """Iterate over collection"""

    @abstractmethod
    def __getitem__(self, item) -> T:
        """Get item from collection"""

    @abstractmethod
    def __setitem__(self, key, value) -> None:
        """Set item to collection"""

    @abstractmethod
    def __delitem__(self, key) -> None:
        """Delete item from collection"""

    @abstractmethod
    def __contains__(self, item) -> bool:
        """Check if collection contains item"""

    @abstractmethod
    def __reversed__(self) -> Iterator:
        """Reverse collection"""
