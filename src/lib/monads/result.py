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

    def __repr__(self):
        """
        String representation for Result[T,E]

        Examples:

        - str(Ok(10)) -> 'Ok(10)'
        - str(Err(10)) -> 'Err(10)'

        :return: str(Result)
        """
        return f'{self.state.value}({self.value})'

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

    def and_then[U](self, fn: Callable[[T], Result[U, E]]) -> "Result[U,E]":
        """
        Return a new Result created from fn return if Result is Ok, else return self

        Examples:

        - Ok(1).and_then(lambda x: Ok(x + 1)) -> Ok(11)
        - Err(1).and_then(lambda x: Ok(x + 1)) -> Err(1)

        :param fn: function to create new Result from
        :return: self if self is Err, else fn(Result.value)
        """
        match self:
            case Ok(o):
                return fn(o)

            case Err(e):
                return Err(e)

            case _:
                raise ResultException('Unreachable')

    def err(self) -> Option[E]:
        """
        Convert from Result[T, E] to Option[E]

        Examples:


        - Ok(1).err() -> Nada()
        - Err(1).err() -> Some(1)

        :return:
        """
        match self:
            case Ok(_):
                return Nada()
            case Err(e):
                return Some(e)
            case _:
                raise ResultException('Unreachable')

    def expect(self, message: str) -> T:
        """
        Get Result.value if Result.state if Ok, else raise ResultException with custom message

        Examples:

        - Ok(1).expect('Error') -> 1
        - Err(1).expect('Error') -> ResultException('Error')

        :param message: Custom error message
        :return: Result.value
        """
        match self:
            case Ok(o):
                return o
            case Err(_):
                raise ResultException(message)
            case _:
                raise ResultException('Unreachable')

    def expect_err(self, message: E) -> E:
        """
        Returns contained Err value, or raises ResultException with custom message

        Examples:

        - Ok(1).expect_err('Error') -> raise ResultException('Error')
        - Err(1).expect_err('Error') -> 1

        :param message: Exception message
        :return: Error value
        """
        match self:
            case Ok(_):
                raise ResultException(message)

            case Err(e):
                return e

            case _:
                raise ResultException('Unreachable')

    def flatten(self, recurse: bool = False) -> "Result[T, E]":
        """
        Convert Result[Result[T,E],E] to Result[T,E].
        Only flattens one layer at a time unless recurse is True

        Examples:

        - Ok(Ok(Ok(1))).flatten() -> Ok(Ok(1))
        - Ok(Ok(Ok(1))).flatten(recurse=True) -> Ok(1)
        - Ok(1).flatten() -> Ok(1)
        - Err(Err(Err(1))).flatten() -> Err(Err(1))
        - Err(1).flatten() -> Err(1)
        - Err(Ok(1)).flatten() -> Ok(1)
        - Ok(Err(1)).flatten() -> Err(1)

        :return: Inner Result
        """

        match self:
            case Ok(o):
                if recurse and isinstance(o, Result):
                    return o.flatten(recurse)
                elif isinstance(o, Result):
                    return o
                else:
                    return Ok(o)

            case Err(e):
                if recurse and isinstance(e, Result):
                    return e.flatten(recurse)
                elif isinstance(e, Result):
                    return e
                else:
                    return Err(e)

            case _:
                raise ResultException('Unreachable')

    def flatmap(self, fn: Callable[[T], T], recurse: bool) -> "Result[T, E]":
        """
        Flatten a Result and map it with a function

        Ex. Function: add_one = lambda x: x + 1

        Examples:

        - Ok(Ok(1)).flatmap(add_one,True) -> Ok(2)
        - Ok(10).flatmap(add_one) -> Ok(11)
        - Err(Err('Error')).flatmap(add_one,True) -> Error('Error')

        :param fn: Function that takes one argument T and returns another T
        :param recurse: Recursively flatten or just flatten once
        :return: Flattened and Mapped Result
        """
        return self.flatten(recurse).map(fn)

    def inspect(self, fn: Callable[[T], None]) -> "Result[T, E]":
        """
        Calls fn with contained value if Ok. Always returns original Result.

        Examples:

        - Ok(1).inspect(lambda x: print(x)) -> prints 1 to STDOUT
        - Err(1).inspect(lambda x: print(x)) -> does nothing

        :param fn: function that takes one argument T and returns None
        :return: Original result
        """
        match self:
            case Ok(o):
                fn(o)
                return Ok(o)

            case Err(e):
                return Err(e)

            case _:
                raise ResultException('Unreachable')

    def inspect_err(self, fn: Callable[[E], None]) -> Result[T, E]:
        """
        Calls fn with contained value if Err. Always returns original Result.

        Examples:

        - Ok(1).inspect_err(lambda e: print(e)) -> Does nothing
        - Err(1).inspect_err(lambda e: print(e)) -> prints 1 to STDOUT

        :return: Original result
        """
        match self:
            case Ok(o):
                return Ok(o)

            case Err(e):
                fn(e)
                return Err(e)

            case _:
                raise ResultException('Unreachable')

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

    def is_err(self) -> bool:
        """
        Check that Result.state is Err

        Example:

        - Ok(1).is_err() -> False
        - Err(1).is_err() -> True

        :return: True if Result.state is Err, else False
        """
        match self:
            case Ok(_):
                return False

            case Err(_):
                return True

            case _:
                raise ResultException('Unreachable')

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

    def is_ok(self) -> bool:
        """
        Check that Result.state is Ok

        Example:

        - Ok(1).is_ok() -> True
        - Err(1).is_ok() -> False

        :return: True if Result.state is Ok, else False
        """
        match self:
            case Ok(_):
                return True

            case Err(_):
                return False

            case _:
                raise ResultException('Unreachable')

    def is_ok_and(self, predicate: Callable[[T], bool]) -> bool:
        """
        Check if Result is Ok and predicate function returns True

        Example Predicate: is_even = lambda x: x % 2 == 0

        Examples:

        - Ok(2).is_ok_and(is_even) -> True
        - Ok(1).is_ok_and(is_even) -> False
        - Err(1).is_ok_and(is_even) -> False

        :param predicate: function that takes Result.value as only argument, returns bool
        :return: True if Ok and predicate function returns True, else False
        """
        match self:
            case Ok(o):
                return predicate(o)
            case Err(_):
                return False
            case _:
                raise ResultException('Unreachable')

    def map[U](self, fn: Callable[[T], U]) -> "Result[U, E]":
        """
        Create a Result where Result.value = fn(Result.value) if Result.state is Ok

        Examples:

        - Ok(1).map(lambda x: x + 1) -> Ok(2)
        - Err(1).map(lambda x: x + 1) -> Err(1)

        :param fn: Function that takes one argument T and returns U
        :return: Mapped Result
        """
        match self:
            case Ok(o):
                return Ok(fn(o))

            case Err(e):
                return Err(e)

            case _:
                raise ResultException('Unreachable')

    def map_err[F](self, fn: Callable[[E], F]) -> "Result[T,F]":
        """
        Return self if Ok(), else map Result to Err(fn(Result.value))

        Examples:

        - Ok(1).map_err(lambda x: x + 1) -> 1
        - Err(1).map_err(lambda x: x + 1) -> 2

        :param fn: Function that takes one argument E and returns F
        :return: self or mapped Err Result
        """
        match self:
            case Ok(o):
                return Ok(o)

            case Err(e):
                return Err(fn(e))

            case _:
                raise ResultException('Unreachable')

    def map_or[U](self, fn: Callable[[T], U], default: U) -> U:
        """
        Convert Result to fn(T) if Ok, else convert to default

        Examples:

        - Ok(1).map_or(lambda x: x + 1, 3) -> 2
        - Err(1).map_or(lambda x: x + 1, 3) -> 3

        :param fn: Function that takes one argument T and returns U
        :param default: Default value
        :return: default or fn(Result.value)
        """
        match self:
            case Ok(o):
                return fn(o)

            case Err(_):
                return default

            case _:
                raise ResultException('Unreachable')

    def map_or_else[U](self, fn: Callable[[T], U], default: Callable[[E], U]) -> U:
        """
        Convert Result to default(Result.error) if Err, else fn(Result.value)

        Examples:

        - Ok(1).map_or_else(lambda x: x + 1, lambda e: e + 5) -> 2
        - Err(1).map_or_else(lambda x: x + 1, lambda e: e + 5) -> 6

        :param fn: Function that takes one argument T and returns U
        :param default: Default function that takes one argument E and returns U
        :return: fn(Result.value) or default(Result.error)
        """
        match self:
            case Ok(o):
                return fn(o)

            case Err(e):
                return default(e)

            case _:
                raise ResultException('Unreachable')

    def ok(self) -> Option[T]:
        """
        Converts from Result[T] to Option[T]

        Examples:

        - Ok(1).ok() -> Some(1)
        - Err(1).ok() -> Nada()

        :return: Option
        """
        match self:
            case Ok(o):
                return Some(o)
            case Err(_):
                return Nada()
            case _:
                raise ResultException('Unreachable')

    def or_else[F](self, fn: Callable[[E], Result[T, F]]) -> "Result[T, F]":
        """
        Returns self if Result is Ok, or else a new Result sourced from called function

        Example:

        - Ok(1).or_else(lambda e: Err(150)) -> Ok(1)
        - Err(1).or_else(lambda e: Err(150)) -> Err(150)

        :param fn: function to get a value from
        :return: self or fn(Result.error)
        """
        match self:
            case Ok(o):
                return Ok(o)

            case Err(e):
                return fn(e)

            case _:
                raise ResultException('Unreachable')

    def other_if_ok(self, other: "Result[T, E]") -> "Result[T, E]":
        """
        Return another Result if current Result is Ok, else return self

        Examples:

        - Ok(1).other_if_ok(Err(1)) -> Err(1)
        - Err(1).other_if_ok(Ok(1)) -> Err(1)

        :param other: Other Result
        :return: other if self is Ok, else self
        """
        match self:
            case Ok(_):
                return other

            case Err(e):
                return Err(e)

            case _:
                raise ResultException('Unreachable')

    def other_if_err(self, other: "Result[T, E]") -> "Result[T, E]":
        """
        Return another Result if current Result is Err, else return self

        Examples:

        - Ok(1).other_if_err(Err(1)) -> Ok(1)
        - Err(1).other_if_err(Ok(1)) -> Ok(1)

        :param other: Other Result
        :return: other if self is Err, else self
        """
        match self:
            case Ok(o):
                return Ok(o)

            case Err(_):
                return other

            case _:
                raise ResultException('Unreachable')

    def unwrap(self) -> T:
        """
        Get Result.value if Result.state is Ok, or raise a ResultException

        Examples:

        - Ok(1).unwrap() -> 1
        - Err('This is not OK.').unwrap() -> raise ResultException('This is not OK.')

        :return: Result.value
        """
        match self:
            case Ok(o):
                return o

            case Err(e):
                raise ResultException(e)

            case _:
                raise ResultException('Unreachable')

    def unwrap_err(self) -> E:
        """
        Return contained error if Err, else raises exception

        Examples:

        - Ok(1).unwrap_err() -> raise ResultException('Result is not an error.')
        - Err(1).unwrap_err() -> 1

        :return: Error value
        """
        match self:
            case Ok(_):
                raise ResultException('Result is not an error.')

            case Err(e):
                return e

            case _:
                raise ResultException('Unreachable')

    def unwrap_or(self, default: T) -> T:
        """
        Get Result.value if Result.state is Ok, or else a default value

        Examples:

        - Ok(1).unwrap_or(5) -> 1
        - Err('Error').unwrap_or(5) -> 5

        :param default: Default value
        :return: Result.value or default value
        """
        match self:
            case Ok(o):
                return o

            case Err(_):
                return default

            case _:
                raise ResultException('Unreachable')

    def unwrap_or_else(self, fn: Callable[[E], T]) -> T:
        """
        Return contained Ok value or compute it from fn(Result.value) if Err

        Examples:

        - Ok(1).unwrap_or_else(lambda x: x + 'Test') -> 1
        - Err('Error').unwrap_or_else(lambda x: x + 'Test') -> 'ErrorTest'

        :param fn: function to get a value from
        :return: Result.value or fn(Result.value)
        """
        match self:
            case Ok(o):
                return o

            case Err(e):
                return fn(e)

            case _:
                raise ResultException('Unreachable')


class Ok[T, E](Result[T, E]):
    """Create a Result[T, E] with an Ok variant"""

    def __init__(self, value: T) -> None:
        super().__init__(value, ResultVariant.OK)


class Err[T, E](Result[T, E]):
    """Create a Result[T, E] with an Err variant"""

    def __init__(self, error: E) -> None:
        super().__init__(error, ResultVariant.ERR)
