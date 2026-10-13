from enum import Enum
from typing import TypeVar, Callable

# Generic type
T = TypeVar("T")


class Option:
    """Rust-style option"""
    _value = None

    def __init__(self, value: T | None):
        self._value = value

    @classmethod
    def some(cls, value: T) -> "Option":
        """Create an option with Some variant"""
        return cls(value)

    @classmethod
    def none(cls) -> "Option":
        """Create an option with None variant"""
        return cls(None)

    def is_some(self) -> bool:
        """Return true if variant is Some"""
        return self._value is not None

    def is_some_and(self, predicate: Callable[[T], bool]) -> bool:
        """Return true if variant is Some and matches predicate"""
        if self.is_none():
            return False

        if not predicate(self._value):
            return False

        return True

    def is_none(self) -> bool:
        """Return true if variant is None"""
        return self._value is None

    def is_none_or(self, predicate: Callable[[T], bool]) -> bool:
        """Return true if variant is None or matches predicate"""
        if self.is_none() or predicate(self._value):
            return True

        return False

    def expect(self, default: T) -> T:
        """Get value if variant is Some, else return default value"""
        if self._value is None:
            return default

        return self._value

    def unwrap(self):
        """Get the value if Some, else raise ValueError"""
        if self._value is None:
            raise ValueError("Cannot unwrap None")

        return self._value

    def map(self, func: Callable) -> "Option":
        """Call a function on the option and return a new option"""
        if self._value is None:
            return Option.none()

        return Option.some(func(self._value))

    def flatten(self) -> "Option":
        """Flatten nested options"""
        if isinstance(self._value, Option):
            return self._value
        else:
            return self

    def flatmap(self, func: Callable) -> "Option":
        """Call a function on the option and return a flattened option"""
        return self.map(func).flatten()


class ResultVariant(Enum):
    """State variants for Result monad"""
    OK = 0
    ERR = 1


class Result:
    """Rust-style result"""

    _value = None
    _state: ResultVariant = ResultVariant.ERR

    def __init__(self, value: T, state: ResultVariant = ResultVariant.OK):
        self._value = value
        self._state = state

    @classmethod
    def ok(cls, value: T) -> "Result":
        """Create a result with OK variant"""
        return cls(value, ResultVariant.OK)

    @classmethod
    def err(cls, value: T) -> "Result":
        """Create a result with ERR variant"""
        return cls(value, ResultVariant.ERR)

    def is_ok(self) -> bool:
        """Return true if variant is OK"""
        return self._state == ResultVariant.OK

    def is_err(self) -> bool:
        """Return true if variant is ERR"""
        return self._state == ResultVariant.ERR

    def get_value(self) -> T:
        """Get the value of the Result regardless of state"""
        return self._value

    def get_unsafe(self) -> T:
        """Convert error value to exception, or else return value"""
        if self._state == ResultVariant.ERR:
            raise Exception(self._value)
        else:
            return self._value

    def map(self, func: Callable) -> "Result":
        """Call a function on the result if variant is OK, else return self"""
        if self._state == ResultVariant.ERR:
            return self

        return Result.ok(func(self._value))

    def flatten(self):
        """Return value if it is a Result, else return self"""
        if isinstance(self._value, Result):
            return self._value
        else:
            return self

    def flatmap(self, func: Callable) -> "Result":
        """Map a function to the result and flatten it"""
        return self.map(func).flatten()
