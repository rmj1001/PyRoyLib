from enum import StrEnum
from typing import Callable

from abstract.iequality import IEquality
from abstract.irepr import IRepr
from abstract.imonad import IMonad
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


class Result[T, E](IRepr, IMonad[T], IEquality):
    """Rust-style result"""
    __match_args__ = ('value',)

    def __init__(self, value: T | E, state: ResultVariant = ResultVariant.OK):
        self.value: T | E = value
        self.state: ResultVariant = state

    def __bool__(self) -> bool:
        """
        Convert Result to a truthy value

        Examples:

        - bool(Ok(10)) -> True

        - bool(Err(10)) -> False

        :return: True if state is Ok, else False
        """
        return self.is_ok()

    # -- IRepr Implementation

    def __repr__(self):
        """
        String representation for Result[T,E]

        Examples:

        - str(Ok(10)) -> 'Ok(10)'

        - str(Err(10)) -> 'Err(10)'

        :return: str(Result)
        """
        return f'{self.state.value}({self.value})'

    # -- IEquality Implementation

    def __eq__(self, other: object) -> bool:
        """
        Check if two Results are equal

        Examples:

        - Ok(10) == Ok(10) -> True

        - Ok(10) == Ok(15) -> False

        - Ok(10) == Err(10) -> False

        - Err(10) == Err(10) -> True

        :param other: Second Result to compare with
        :return: True if both Results have equal values and states, else False
        """
        if not isinstance(other, Result):
            return NotImplemented

        return self.value == other.value and self.state == other.state

    def __ne__(self, other: object) -> bool:
        """
        Check if two Results are not equal

        Examples:

        - Ok(1) != Ok(10) -> True

        - Ok(1) != Ok(1) -> False

        - Err(1) != Err(10) -> True

        - Err(10) != Err(10) -> False

        - Ok(1) != Err(1) -> True

        :param other: Second Result to compare with
        :return: True if either Result's value or state doesn't match the other, else False
        """
        if not isinstance(other, Result):
            return NotImplemented

        return self.value != other.value or self.state != other.state

    # -- IMonad Implementation

    def expect(self, message: E) -> T:
        """
        Get Result.value if Result.state if Ok, else raise ResultException with custom message

        Examples:

        - Ok(1).expect('Error') -> 1

        - Err(1).expect('Error') -> raise ResultException('Error')

        :param message: Custom error message
        :return: Result.value
        """
        if self.is_err():
            raise ResultException(message)

        return self.value

    def unwrap(self) -> T:
        """
        Get Result.value if Result.state is Ok, or raise a ResultException

        Examples:

        - Ok(1).unwrap() -> 1

        - Err('This is not OK.').unwrap() -> raise ResultException('This is not OK.')

        :return: Result.value
        """
        if self.is_err():
            raise ResultException(self.value)

        return self.value

    def unwrap_or(self, default: T) -> T:
        """
        Get Result.value if Result.state is Ok, or else a default value

        Examples:

        - Ok(1).unwrap_or(5) -> 1

        - Err('Error').unwrap_or(5) -> 5

        :param default: Default value
        :return: Result.value or default value
        """
        if self.is_err():
            return default

        return self.value

    def unwrap_or_else(self, fn: Callable, *args, **kwargs) -> T | Callable:
        """
        Get Result.value if Result.state is Ok, or else returned value of function

        Examples:

        - Ok(1).unwrap_or_else(lambda: 100 + 5) -> 1

        - Err('Error').unwrap_or_else(lambda: 100 + 5) -> 105

        :param fn: function to get a value from
        :param args: sequential arguments to pass to fn
        :param kwargs: keyword arguments to pass to fn
        :return: Result.value or function return
        """
        if self.is_ok():
            return self.value

        return fn(*args, **kwargs)

    def or_else(self, fn: Callable, *args, **kwargs) -> "Result[T, Callable]":
        """
        Returns Ok() with original value if Result is Ok, or else an Error with its
        value sourced from called function

        Example:

        - Ok(1).or_else(lambda 100 + 50) -> Ok(1)

        - Err(1).or_else(lambda 100 + 50) -> Err(150)

        :param fn: function to get a value from
        :param args: sequential arguments to pass to fn
        :param kwargs: keyword arguments to pass to fn
        :return: self or Err(fn(*args, **kwargs))
        """
        if self.is_ok():
            return self

        return Err(fn(*args, **kwargs))

    # -- IFunctor Implementation

    def flatten(self) -> "Result[T, E]":
        """
        Return innermost Result in nested Results

        Examples:

        - Ok(Ok(Ok(1))).flatten() -> Ok(1)

        - Ok(1).flatten() -> Ok(1)

        - Err(Err(Err(1))).flatten() -> Err(1)

        - Err(1).flatten() -> Err(1)

        - Err(Ok(1)).flatten() -> Ok(1)

        - Ok(Err(1)).flatten() -> Err(1)

        :return: Innermost Result
        """
        current = Result(self.value, self.state)

        while isinstance(current.value, Result):
            current.state = current.value.state
            current.value = current.value.value

        return current

    def map(self, fn: MapFn) -> "Result[T, E]":
        """
        Create a Result where Result.value = fn(Result.value) if Result.state is Ok

        Examples:

        - Ok(1).map(lambda x: x + 1) -> Ok(2)

        - Err(1).map(lambda x: x + 1) -> Err(1)

        :param fn: Function that takes one argument T and returns another T
        :return: Mapped Result
        """
        if self.is_err():
            return self

        return Ok(fn(self.value))

    def flatmap(self, fn: MapFn) -> "Result[T, E]":
        """
        Flatten a Result and map it with a function

        Examples:

        - Ok(Ok(1)).flatmap(lambda x: x + 1) -> Ok(2)

        - Ok(10).flatmap(lambda x: x + 1) -> Ok(11)

        - Err(Err('Error')).flatmap(lambda x: x + 1) -> Error('Error')

        :param fn: Function that takes one argument T and returns another T
        :return: Flattened and Mapped Result
        """
        return self.flatten().map(fn)

    # -- END Interface Implementations

    @classmethod
    def ok(cls, value: T) -> "Result[T,E]":
        """Create a result with OK variant"""
        return cls(value, ResultVariant.OK)

    @classmethod
    def err(cls, error: E) -> "Result[T,E]":
        """Create a result with ERR variant"""
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
            return Ok(default)

        return Ok(func(self.value))

    def map_or_else(self, success: MapFn, default: Callable, *args, **kwargs) -> "Result[MapFn,MapErr]":
        """Maps function if variant is Ok, else creates new Ok result with default function returned value"""
        if self.is_err():
            return Ok(default(*args, **kwargs))

        return Ok(success(self.value))

    def map_err(self, func: MapErr) -> "Result[T, E] | Result[T,MapErr]":
        """Maps an Err value, leaving Ok untouched"""
        if self.is_ok():
            return self

        return Err(func(self.value))

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
        return Ok(self.value)

    def into_err(self) -> "Result[T, E]":
        """Returns the contained Err, never raises exception"""
        return Err(self.value)

    def other_if_ok(self, res: "Result[T, E]") -> "Result[T, E]":
        """Result res if result is Ok, otherwise return Err of self"""
        if self.is_ok():
            return res

        return self

    def and_then(self, func: Callable, *args, **kwargs) -> "Result[T, E] | Result[Callable, E]":
        """Calls func if result is Ok, otherwise returns Err of self"""
        if self.is_err():
            return self

        return Ok(func(*args, **kwargs))

    def other_if_err(self, res: "Result[T, E]") -> "Result[T, E]":
        """Returns res if result is Err, otherwise returns Ok value of self"""
        if self.is_ok():
            return self

        return res


class Ok[T, E](Result[T, E]):
    """Create a Result[T, E] with an Ok variant"""

    def __init__(self, value: T) -> None:
        super().__init__(value, ResultVariant.OK)


class Err[T, E](Result[T, E]):
    """Create a Result[T, E] with an Err variant"""

    def __init__(self, error: E) -> None:
        super().__init__(error, ResultVariant.ERR)
