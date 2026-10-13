from enum import Enum
from typing import TypeVar, Callable

# Generic type
T = TypeVar("T")


class Option:
    """Rust-style option"""
    _value = None

    def __init__(self, value: T | None):
        self._value = value

    def __str__(self):
        """Return string representation of option"""
        if self.is_some():
            return f"Some({self.unwrap()})"

        return "None"

    def __bool__(self):
        """Return true if option is Some, false if None"""
        if self.is_some():
            return True
        return False

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

        return predicate(self._value)

    def is_none(self) -> bool:
        """Return true if variant is None"""
        return self._value is None

    def is_none_or(self, predicate: Callable[[T], bool]) -> bool:
        """Return true if variant is None or matches predicate"""
        if self.is_none() or predicate(self._value):
            return True

        return False

    def expect(self, error: T):
        """Get value if Some, else raise custom ValueError"""
        if self.is_none():
            raise ValueError(error)

        return self._value

    def unwrap(self) -> T:
        """Get the value if Some, else raise ValueError"""
        if self.is_none():
            raise ValueError("Cannot unwrap None")

        return self._value

    def unwrap_or(self, default: T) -> T:
        """Get value if variant is Some, else return default value"""
        if self.is_none():
            return default

        return self._value

    def unwrap_or_else(self, func: Callable) -> T:
        """Get value if Some, else get value from passed function"""
        if self.is_some():
            return self._value

        return func()

    def map(self, func: Callable) -> "Option":
        """Call a function on the option and return a new option"""
        if self._value is None:
            return Option.none()

        return Option.some(func(self._value))

    def flatten(self) -> "Option":
        """Recursively flatten nested options"""
        if isinstance(self._value, Option):
            return self._value.flatten()
        else:
            return self

    def flatmap(self, func: Callable) -> "Option":
        """Call a function on the option and return a flattened option"""
        return self.map(func).flatten()

    def ok_or(self, error: T) -> "Result":
        """Return a result"""
        if self.is_none():
            return Result.err(error)

        return Result.ok(self._value)

    def ok_or_else(self, error: Callable) -> "Result":
        """Return a result. If option is None, error will be the result of a function."""
        if self.is_none():
            return Result.err(error)

        return Result.ok(self._value)

    def filter(self, predicate: Callable[[T], bool]) -> "Option":
        """Return Option.some(self._value) if predicate returns True, else return Option.none()"""
        if self.is_none():
            return self

        if predicate(self._value):
            return Option.some(self._value)

        return Option.none()

    def both(self, other_option: Option) -> "Option":
        """Return None if option is None, otherwise return other_option"""
        if self.is_none():
            return self

        return other_option

    def either(self, other_option: Option) -> "Option":
        """Returns the option if it is Some, otherwise returns other_option"""
        if self.is_some():
            return self

        return other_option

    def or_else(self, func: Callable) -> "Option":
        """Returns option if it is Some, else calls func and returns result"""
        if self.is_some():
            return self

        result = func(self._value)

        if result is None:
            return Option.none()

        return Option.some(result)

    def take(self) -> T:
        """Return the value in the Option and set it to None"""
        value = self._value

        self._value = None

        return value

    def replace(self, value: T) -> None:
        """Replace the current value with another value"""
        self._value = value

    def zip(self, other_option: Option) -> Option:
        """Return tuple if both options are Some, else return None"""
        if self.is_some() and other_option.is_some():
            return Option.some((self._value, other_option._value))

        return Option.none()

    def unzip(self) -> tuple[Option, Option]:
        """Unzips an option containing a tuple of values. Returns (None, None) if tuple not present."""
        if not isinstance(self._value, tuple):
            return Option.none(), Option.none()

        first = self._value[0]
        second = self._value[1]
        first_opt = Option.none()
        second_opt = Option.none()

        if first is not None:
            first_opt = Option.some(first)

        if second is not None:
            second_opt = Option.some(second)

        return first_opt, second_opt


def something(value: T) -> Option:
    """Shorthand for Option.some(value)"""
    return Option.some(value)


def nothing() -> Option:
    """Shorthand for Option.none()"""
    return Option.none()


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
