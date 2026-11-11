from abc import ABC, abstractmethod, abstractproperty
from collections.abc import Iterable


class ContainerException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class IContainer[T](ABC):
    value: T

    def __init__(self, value: T):
        self.value: T = value

    @abstractmethod
    def __str__(self) -> str:
        """String representation of the object"""

    @abstractmethod
    def __add__(self, other) -> IContainer[T]:
        """Add the contents of two containers together for a new container"""

    @abstractmethod
    def __sub__(self, other) -> IContainer[T]:
        """Subtract the contents of two containers together for a new container"""

    @abstractmethod
    def __mul__(self, other) -> IContainer[T]:
        """Multiply the contents of two containers together for a new container"""

    @abstractmethod
    def __truediv__(self, other) -> IContainer[T]:
        """Divide the contents of two containers together for a new container"""

    @abstractmethod
    def __floordiv__(self, other) -> IContainer[T]:
        """Divide and floor the contents of two containers together for a new container"""

    @abstractmethod
    def __mod__(self, other) -> IContainer[T]:
        """Modulo the contents of two containers together for a new container"""

    @abstractmethod
    def __pow__(self, other) -> IContainer[T]:
        """Create a new container with the contents of the first container raised to the second container's contents"""

    @abstractmethod
    def __bool__(self) -> bool:
        """Return boolean representation of Box contents"""

    @abstractmethod
    def __ge__(self, other) -> bool:
        """Compare two containers for greater or equal contents"""

    @abstractmethod
    def __gt__(self, other) -> bool:
        """Compare two containers for greater contents"""

    @abstractmethod
    def __le__(self, other) -> bool:
        """Compare two containers for less or equal contents"""

    @abstractmethod
    def __lt__(self, other) -> bool:
        """Compare two containers for lesser contents"""

    @abstractmethod
    def __eq__(self, other) -> bool:
        """Check if contents of two containers are equal"""

    @abstractmethod
    def __ne__(self, value: object, /) -> bool:
        """Check if contents of two containers are not equal"""

    @abstractmethod
    def __and__(self, other) -> bool:
        """Check if contents from both containers are True"""

    @abstractmethod
    def __or__(self, other) -> bool:
        """Check if contents of either container are True"""

    @abstractmethod
    def __xor__(self, other) -> bool:
        """Check XOR on contents of both containers"""

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
    def replace(self, new_value: T) -> IContainer[T]:
        """Replace the contents and return self"""
    
    @abstractmethod
    def peek(self) -> T:
        """Return the contents without removing it"""