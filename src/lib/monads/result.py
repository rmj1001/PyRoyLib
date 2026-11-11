from enum import StrEnum
from typing import Callable

from abstract.iequality import IEquality
from abstract.ifunctor import IFunctor
from abstract.irepr import IRepr
from .imonad import IMonad
from monads.exceptions.result_exception import ResultException

# Used for functions that pass an error to function and return another error
type MapFn[T] = Callable[[T], T]
type MapErr[E] = Callable[[E], E]

# Used for search functions where contained value is checked against condition to return True/False
type Predicate[T] = Callable[[T], bool]


class ResultVariant(StrEnum):
    """State variants for Result monad"""
    OK = 'Ok'
    ERR = 'Err'


class Result[T, E](IRepr, IFunctor[T | E], IMonad[T], IEquality):
    """Rust-style result"""

    def __init__(self, value: T | E, state: ResultVariant = ResultVariant.OK):
        super().__init__(value)
        self.state: ResultVariant = state

    def __bool__(self) -> bool:
        """Return True if Result[T,E] is Ok, else return False"""
        return self.is_ok()

    # -- IRepr Implementation

    def __repr__(self):
        """String representation for Result[T,E]"""
        return f'{self.state}({self.value})'

    # -- IEquality Implementation

    def __eq__(self, other: object) -> bool:
        """Compare Result objects for equality"""
        if not isinstance(other, Result):
            return NotImplemented

        return self.value == other.value and self.state == other.state

    def __ne__(self, other: object) -> bool:
        if not isinstance(other, Result):
            return NotImplemented

        return self.value != other.value or self.state != other.state

    # -- IMonad Implementation

    def expect(self, message: E) -> T:
        """Returns Ok value or throws exception with custom error message"""
        if self.is_err():
            raise ResultException(message)

        return self.value

    def unwrap(self) -> T:
        """Returns Ok value or throws exception with Err value"""
        if self.is_err():
            raise ResultException(self.value)

        return self.value

    def unwrap_or[V](self, default: V) -> T | V:
        """Returns contained Ok value or default if Err"""
        if self.is_err():
            return default

        return self.value

    def unwrap_or_else[R](self, fn: Callable, *args, **kwargs) -> T | R:
        """Returns contained Ok value or value from func if Err"""
        if self.is_ok():
            return self.value

        return fn(*args, **kwargs)

    def or_else(self, fn: Callable, *args, **kwargs) -> "Result[T, E] | Result[T, Callable]":
        """Calls func if result is Err, otherwise returns Ok of self"""
        if self.is_ok():
            return self

        return err(fn(*args, **kwargs))

    # -- IFunctor Implementation

    def flatten(self) -> "Result[T, E]":
        """
        Flatten nested Results until self.value is of type T or E
        :return: self flattened
        """
        while isinstance(self.value, Result):
            self.state = self.value.state
            self.value = self.value.value

        return self

    def map(self, fn: MapFn) -> "Result[T, E]":
        """
        Apply function to contained Ok value, leaving Err value untouched.
        :param fn: Function to apply to contained Ok value
        :return: self with value changed by applied function
        """
        if self.is_err():
            return self

        self.value = fn(self.value)
        return self

    def flatmap(self, fn: MapFn) -> "Result[T, E]":
        """
        Flatten self, then apply function to internal value
        :param fn: Function to apply to internal value
        :return: self, flattened and function applied
        """
        return self.flatten().map(fn)

    # -- END Interface Implementations

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
        return self.state == ResultVariant.OK

    def is_ok_and(self, predicate: Predicate) -> bool:
        """Return True if variant is OK and predicate returns True"""
        return self.is_ok() and predicate(self.value)

    def is_err(self) -> bool:
        """Return True if variant is ERR"""
        return self.state == ResultVariant.ERR

    def is_err_and(self, predicate: Predicate) -> bool:
        """Return True if variant is ERR and predicate returns True"""
        return self.is_err() and predicate(self.value)

    def map_or[V](self, func: MapFn, default: V) -> "Result[MapFn|V,E]":
        """Returns the provided default if Err or applies func to value"""
        if self.is_err():
            return ok(default)

        return ok(func(self.value))

    def map_or_else(self, success: MapFn, default: Callable, *args, **kwargs) -> "Result[MapFn,MapErr]":
        """Maps function if variant is Ok, else creates new Ok result with default function returned value"""
        if self.is_err():
            return ok(default(*args, **kwargs))

        return ok(success(self.value))

    def map_err(self, func: MapErr) -> "Result[T, E] | Result[T,MapErr]":
        """Maps an Err value, leaving Ok untouched"""
        if self.is_ok():
            return self

        return err(func(self.value))

    def expect_err(self, message: E) -> T:
        """Returns contained Err, or else raises exception if Ok"""
        if self.is_err():
            return self.value

        raise ResultException(message)

    def unwrap_err(self) -> T:
        """Returns contained Err, or else raises exception with Ok value"""
        if self.is_err():
            return self.value

        raise ResultException(self.value)

    def into_ok(self) -> "Result[T, E]":
        """Returns the contained Ok, never raises exception"""
        return ok(self.value)

    def into_err(self) -> "Result[T, E]":
        """Returns the contained Err, never raises exception"""
        return err(self.value)

    def other_if_ok(self, res: "Result[T, E]") -> "Result[T, E]":
        """Result res if result is Ok, otherwise return Err of self"""
        if self.is_ok():
            return res

        return self

    def and_then(self, func: Callable, *args, **kwargs) -> "Result[T, E] | Result[Callable, E]":
        """Calls func if result is Ok, otherwise returns Err of self"""
        if self.is_err():
            return self

        return ok(func(*args, **kwargs))

    def other_if_err(self, res: "Result[T, E]") -> "Result[T, E]":
        """Returns res if result is Err, otherwise returns Ok value of self"""
        if self.is_ok():
            return self

        return res


def ok[T, E](value: T, *args, **kwargs) -> Result[T, E]:
    """Shorthand for Result.ok(), useful for pattern matching"""
    return Result.ok(value, *args, **kwargs)


def err[T, E](value: E, *args, **kwargs) -> Result[T, E]:
    """Shorthand for Result.err(), useful for pattern matching"""
    return Result.err(value, *args, **kwargs)
