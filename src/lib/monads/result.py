from enum import Enum
from typing import Callable, TypeAlias

from monads.exceptions.result_exception import ResultException
from types.predicate import Predicate
from types.map_function import MapFunc

# Used for functions that pass an error to function and return another error
ErrMapFunc: TypeAlias = MapFunc


class ResultVariant(Enum):
    """State variants for Result monad"""
    OK = 0
    ERR = 1


class Result[T, E]:
    """Rust-style result"""

    def __init__(self, value: T, state: ResultVariant = ResultVariant.OK):
        self._value: T = value
        self._state: ResultVariant = state

    def __str__(self):
        """String representation for Result[T,E]"""
        if self.is_ok():
            return f"ok({self._value})"
        else:
            return f"err({self._value})"

    def __bool__(self) -> bool:
        """Return True if Result[T,E] is Ok, else return False"""
        return self.is_ok()

    def __eq__(self, other: object) -> bool:
        """Compare Result objects for equality"""
        if not isinstance(other, Result):
            return NotImplemented

        if self._value != other._value:
            return False

        return self._state == other._state

    @classmethod
    def ok(cls, value: T, *args, **kwargs) -> "Result[T,E]":
        """Create a result with OK variant"""
        if isinstance(value, Callable):
            return cls(value(*args, **kwargs), ResultVariant.OK)

        return cls(value, ResultVariant.OK)

    @classmethod
    def err(cls, error: E, *args, **kwargs) -> "Result[T,E]":
        """Create a result with ERR variant"""
        if isinstance(error, Callable):
            return cls(error(*args, **kwargs), ResultVariant.ERR)

        # ignore reportArgumentType
        return cls(error, ResultVariant.ERR)

    def is_ok(self) -> bool:
        """Return True if variant is OK"""
        return self._state == ResultVariant.OK

    def is_ok_and(self, predicate: Predicate) -> bool:
        """Return True if variant is OK and predicate returns True"""
        return self.is_ok() and predicate(self._value)

    def is_err(self) -> bool:
        """Return True if variant is ERR"""
        return self._state == ResultVariant.ERR

    def is_err_and(self, predicate: Predicate) -> bool:
        """Return True if variant is ERR and predicate returns True"""
        return self.is_err() and predicate(self._value)

    def map(self, func: MapFunc) -> "Result[T,E]":
        """Create a new result with value mapped to func"""
        if self.is_err():
            return self

        return ok(func(self._value))

    def map_or[V](self, func: MapFunc, default: V) -> "Result[MapFunc|V,E]":
        """Returns the provided default if Err or applies func to value"""
        if self.is_err():
            return ok(default)

        return ok(func(self._value))

    def map_or_else(self, success: MapFunc, default: Callable, *args, **kwargs) -> "Result[MapFunc,ErrMapFunc]":
        """Maps function if variant is Ok, else creates new Ok result with default function returned value"""
        if self.is_err():
            return ok(default(*args, **kwargs))

        return ok(success(self._value))

    def map_err(self, func: ErrMapFunc) -> "Result[T, E] | Result[T,ErrMapFunc]":
        """Maps an Err value, leaving Ok untouched"""
        if self.is_ok():
            return self

        return err(func(self._value))

    def expect(self, message: E) -> T:
        """Returns Ok value or throws exception with custom error message"""
        if self.is_err():
            raise ResultException(message)

        return self._value

    def unwrap(self) -> T:
        """Returns Ok value or throws exception with Err value"""
        if self.is_err():
            raise ResultException(self._value)

        return self._value

    def expect_err(self, message: E) -> T:
        """Returns contained Err, or else raises exception if Ok"""
        if self.is_err():
            return self._value

        raise ResultException(message)

    def unwrap_err(self) -> T:
        """Returns contained Err, or else raises exception with Ok value"""
        if self.is_err():
            return self._value

        raise ResultException(self._value)

    def into_ok(self) -> "Result[T, E]":
        """Returns the contained Ok, never raises exception"""
        return ok(self._value)

    def into_err(self) -> "Result[T, E]":
        """Returns the contained Err, never raises exception"""
        return err(self._value)

    def other_if_ok[V](self, res: "Result[V, E]") -> "Result[T, E] | Result[V, E]":
        """Result res if result is Ok, otherwise return Err of self"""
        if self.is_ok():
            return res

        return self

    def and_then(self, func: Callable, *args, **kwargs) -> "Result[T, E] | Result[Callable, E]":
        """Calls func if result is Ok, otherwise returns Err of self"""
        if self.is_err():
            return self

        return ok(func(*args, **kwargs))

    def other_if_err[V](self, res: "Result[V, E]") -> "Result[T, E] | Result[V, E]":
        """Returns res if result is Err, otherwise returns Ok value of self"""
        if self.is_ok():
            return self

        return res

    def or_else(self, func: Callable, *args, **kwargs) -> "Result[T, E] | Result[T, Callable]":
        """Calls func if result is Err, otherwise returns Ok of self"""
        if self.is_ok():
            return self

        return err(func(*args, **kwargs))

    def unwrap_or[V](self, default: V) -> T | V:
        """Returns contained Ok value or default if Err"""
        if self.is_err():
            return default

        return self._value

    def unwrap_or_else[R](self, func: Callable, *args, **kwargs) -> T | R:
        """Returns contained Ok value or value from func if Err"""
        if self.is_ok():
            return self._value

        return func(*args, **kwargs)


def ok[T, E](value: T, *args, **kwargs) -> Result[T, E]:
    """Shorthand for Result.ok(), useful for pattern matching"""
    if isinstance(value, Callable):
        return Result.ok(value(*args, **kwargs))

    return Result.ok(value)


def err[T, E](value: E, *args, **kwargs) -> Result[T, E]:
    """Shorthand for Result.err(), useful for pattern matching"""
    if isinstance(value, Callable):
        return Result.err(value(*args, **kwargs))

    return Result.err(value)
