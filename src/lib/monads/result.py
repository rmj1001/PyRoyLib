from enum import StrEnum
from typing import Callable

lazy from src.lib.abstract.iequality import IEquality
lazy from src.lib.abstract.imonad import IMonad
lazy from src.lib.abstract.irepr import IRepr
lazy from src.lib.monads.exceptions.result_exception import ResultException
lazy from src.lib.monads.option import Option, Some, Nada


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

    def map(self, fn: Callable[[T], T]) -> "Result[T, E]":
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

    def flatmap(self, fn: Callable[[T], T]) -> "Result[T, E]":
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
        """
        Create a Result with Ok variant

        Example: Result.ok(val) -> Result(val, ResultVariant.OK)

        :param value: The value for Result to contain
        :return: Result(value, ResultVariant.OK)
        """
        return cls(value, ResultVariant.OK)

    @classmethod
    def err(cls, value: E) -> "Result[T,E]":
        """
        Create a Result with Err variant

        Example: Result.err(val) -> Result(val, ResultVariant.ERR)

        :param value: The error for Result to contain
        :return: Result(value, ResultVariant.ERR)
        """
        return cls(value, ResultVariant.ERR)

    def is_ok(self) -> bool:
        """
        Check that Result.state is Ok

        Example:

        - Ok(1).is_ok() -> True

        - Err(1).is_ok() -> False

        :return: True if Result.state is Ok, else False
        """
        return self.state == ResultVariant.OK

    def is_ok_and(self, predicate: Callable[[T], bool]) -> bool:
        """
        Check that Result.state is Ok, and predicate function
        returns True.

        Examples

        - Ok(2).is_ok_and(lambda x: x % 2 == 0) -> True

        - Ok(5).is_ok_and(lambda x: x % 2 == 0) -> False

        - Err().is_err_and(lambda x: x % 2 == 0) -> False

        :param predicate: Function taking Result.value as only argument, returns bool
        :return: True if Result.state is Ok and predicate returns True, else False
        """
        return self.is_ok() and predicate(self.value)

    def is_err(self) -> bool:
        """
        Check that Result.state is Err

        Example:

        - Ok(1).is_err() -> False

        - Err(1).is_err() -> True

        :return: True if Result.state is Err, else False
        """
        return self.state == ResultVariant.ERR

    def is_err_and(self, predicate: Callable[[T], bool]) -> bool:
        """
        Check that Result.state is Err, and predicate function
        returns True.

        Examples

        - Ok(2).is_err_and(lambda x: x % 2 == 0) -> False

        - Ok(5).is_err_and(lambda x: x % 2 == 0) -> False

        - Err('Error').is_err_and(lambda x: x == 'Error') -> True

        :param predicate: Function taking Result.value as only argument, returns bool
        :return: True if Result.state is Err and predicate returns True, else False
        """
        return self.is_err() and predicate(self.value)

    def into_option(self) -> Option[T]:
        """
        Create an Option from Result. Ok Results convert to Some Options,
        Err Results convert to Nada Options

        Examples:

        - Ok(1).into_option() -> Some(1)

        - Err(1).into_option() -> Nada()

        :return: Option
        """
        match self:
            case Ok(value):
                return Some(value)
            case Err(_):
                return Nada()
            case _:
                raise ResultException('Unreachable')


    def map_ok_or(self, fn: Callable[[T], T], default: T) -> "Result[T | Callable[[T], T],E]":
        """
        Convert Result to Ok(default) if Err, else map function to Result

        Examples:

        - Ok(1).map_or(lambda x: x + 1, 10) -> Ok(2)

        - Err(1).map_or(lambda x: x + 1, 10) -> Ok(10)

        :param fn: Function that takes one argument T and returns another T
        :param default: Default value
        :return: Ok(default) or mapped Ok Result
        """
        if self.is_err():
            return Ok(default)

        return Ok(fn(self.value))

    def map_ok_or_else(self, fn: Callable[[T], T], default: Callable, *args,
                       **kwargs) -> "Result[Callable[[T], T],Callable[[E], E]]":
        """
        Convert Result to Ok(default(*args, **kwargs)) if Err, else map function to Result

        Examples:

        - Ok(1).map_or(lambda x: x + 1, lambda x: x + 5, 10) -> Ok(2)

        - Err(1).map_or(lambda x: x + 1, lambda x: x + 5, 10) -> Ok(15)

        :param fn: Function that takes one argument T and returns another T
        :param default: Default function with *args and **kwargs passed in
        :return: Ok(default(*args, **kwargs)) or mapped Ok Result
        """
        if self.is_err():
            return Ok(default(*args, **kwargs))

        return Ok(fn(self.value))

    def map_err(self, fn: Callable[[E], E]) -> "Result[T, E | Callable[[E], E]]":
        """
        Return self if Ok(), else map Result to Err(fn(Result.value))

        Examples:

        - Ok(1).map_err(lambda x: x + 1) -> Ok(1)

        - Err(1).map_err(lambda x: x + 1) -> Err(2)

        :param fn: Function that takes one argument E and returns another E
        :return: self or mapped Err Result
        """
        if self.is_ok():
            return self

        return Err(fn(self.value))

    def expect_err(self, message: E) -> E:
        """
        Return contained error if Err, else raises exception with message

        Examples:

        - Ok(1).expect_err('Not an error') -> raise ResultException('Not an error')

        - Err(1).expect_err('Not an error') -> 1

        :param message: Exception message
        :return: Error value
        """
        if self.is_err():
            return self.value

        raise ResultException(message)

    def unwrap_err(self) -> T:
        """
        Return contained error if Err, else raises exception

        Examples:

        - Ok(1).unwrap_err() -> raise ResultException('Result is not an error.')

        - Err(1).unwrap_err() -> 1

        :return: Error value
        """
        if self.is_err():
            return self.value

        raise ResultException('Result is not an error.')

    def into_ok(self) -> "Result[T, E]":
        """
        Convert a Result to an Ok variant, regardless of its previous state.

        Examples:

        - Ok(1).into_ok() -> Ok(1)

        - Err(1).into_ok() -> Ok(1)

        :return: Ok()
        """
        return Ok(self.value)

    def into_err(self) -> "Result[T, E]":
        """
        Convert a Result to an Err variant, regardless of its previous state.

        Examples:

        - Ok(1).into_err() -> Err(1)

        - Err(1).into_err() -> Err(1)

        :return: Ok()
        """
        return Err(self.value)

    def other_if_ok(self, other: "Result[T, E]") -> "Result[T, E]":
        """
        Return another Result if current Result is Ok, else return self

        Examples:

        - Ok(1).other_if_ok(Err(1)) -> Err(1)

        - Err(1).other_if_ok(Ok(1)) -> Err(1)

        :param other: Other Result
        :return: other if self is Ok, else self
        """
        if self.is_ok():
            return other

        return self

    def and_then(self, fn: Callable, *args, **kwargs) -> "Result[T | Callable, E]":
        """
        Return a new Result created from fn return if Result is Ok, else return self

        Examples:

        - Ok(1).and_then(lambda: 10) -> Ok(10)

        - Err(1).and_then(lambda: 10) -> Err(1)

        :param fn: function to create new Result from
        :param args: Sequential arguments passed to fn
        :param kwargs: Keyword arguments passed to fn
        :return: self if self is Err, else Ok(fn(*args, **kwargs))
        """
        if self.is_err():
            return self

        return Ok(fn(*args, **kwargs))

    def other_if_err(self, other: "Result[T, E]") -> "Result[T, E]":
        """
        Return another Result if current Result is Err, else return self

        Examples:

        - Ok(1).other_if_err(Err(1)) -> Ok(1)

        - Err(1).other_if_err(Ok(1)) -> Ok(1)

        :param other: Other Result
        :return: other if self is Err, else self
        """
        if self.is_ok():
            return self

        return other


class Ok[T, E](Result[T, E]):
    """Create a Result[T, E] with an Ok variant"""

    def __init__(self, value: T) -> None:
        super().__init__(value, ResultVariant.OK)


class Err[T, E](Result[T, E]):
    """Create a Result[T, E] with an Err variant"""

    def __init__(self, error: E) -> None:
        super().__init__(error, ResultVariant.ERR)
