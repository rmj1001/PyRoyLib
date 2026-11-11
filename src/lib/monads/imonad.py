from abc import ABC, abstractmethod
from typing import Callable

class IMonad[T](ABC):
    value: T

    @abstractmethod
    def expect[E](self, message: E) -> T:
        """Return value if possible, or raise an exception with custom message."""

    @abstractmethod
    def unwrap(self) -> T:
        """Return value if possible, or raise an exception."""

    @abstractmethod
    def unwrap_or(self, default: T) -> T:
        """Return value if possible, or a default value."""

    @abstractmethod
    def unwrap_or_else(self, fn: Callable, *args, **kwargs) -> T:
        """Return value if possible, or a value returned from passed Callable."""

    @abstractmethod
    def or_else(self, fn: Callable, *args, **kwargs) -> IMonad[T]:
        """Return self or another IMonad created from fn"""
