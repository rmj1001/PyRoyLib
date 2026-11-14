from collections.abc import Callable

from abstract.iequality import IEquality
from abstract.ifunctor import IFunctor
from abstract.irepr import IRepr
from abstract.imonad import IMonad
from monads.exceptions.option_exception import OptionException
from monads.result import Result, ok, err

# Map function type alias
type MapFn[T] = Callable[[T], T]
type Predicate[T] = Callable[[T], bool]


class Option[T](IRepr, IMonad[T], IFunctor[T], IEquality):
    """Rust-style option"""

    def __init__(self, value: T | None):
        self.value: T | None = value

    def __bool__(self) -> bool:
        """
        Convert Option to a truthy value

        Examples:

        - bool(some(10)) -> True

        - bool(nada()) -> False

        :return: True if internal value is not None, else False
        """
        return self.is_some()

    # -- IRepr Implementation

    def __repr__(self) -> str:
        """
        String representation of Option

        Examples:

        - str(some(10)) -> 'some(10)'

        - str(nada()) -> 'nada'

        :return: str(Option)
        """
        if self.value is not None:
            return f"some({self.value})"

        return "nada"

    # -- IEquality Implementation

    def __eq__(self, other: object) -> bool:
        """
        Check if two Options are equal

        Examples:

        - some(1) == some(2) -> False

        - some(10) == nada() -> False

        - some(10) == some(10) -> True

        - nada() == nada() -> True
        :param other: Second Option to compare with
        :return: True if both Options values are equal, else False
        """
        if not isinstance(other, Option):
            return NotImplemented

        return (self.value == other.value) or (self.value is None and other.value is None)

    def __ne__(self, other: object) -> bool:
        """
        Check if two Options are not equal

        Examples:

        - some(1) != some(2) -> True

        - some(10) != nada() -> True

        - some(10) != some(10) -> False

        - nada() != nada() -> False

        :param other: Second Option to compare with
        :return: True if both Options values are not equal, else False
        """
        if not isinstance(other, Option):
            return NotImplemented

        return self.value != other.value

    # --- IMonad Implementation

    def expect[E](self, message: E) -> T:
        """
        Get internal value if it is not None, or raise an OptionException with a custom message

        Examples:

        - some(1).expect('Not a number') -> 1

        - nada().expect('Not a number') -> raise OptionException('Not a number')

        :param message: Error message
        :return: Internal value
        """
        if self.value is None:
            raise OptionException(message)

        return self.value

    def unwrap(self) -> T:
        """
        Get internal value if it is not None, or raise an OptionException

        Examples:

        - some(1).unwrap() -> 1

        - nada().unwrap() -> raise OptionException("Cannot unwrap Nada")

        :return: Internal value
        """
        if self.value is None:
            raise OptionException("Cannot unwrap Nada")

        return self.value

    def unwrap_or(self, default: T) -> T:
        """
        Get internal value if it is not None, or else a default value

        Examples:

        - some(1).unwrap_or(10) -> 1

        - nada().unwrap_or(10) -> 10

        :return: Internal or default value
        """
        if self.value is None:
            return default

        return self.value

    def unwrap_or_else(self, fn: Callable, *args, **kwargs) -> T | Callable:
        """
        Get internal value if it is not None, or else the returned value of a function

        Examples:

        - some(1).unwrap_or_else(lambda: 100 + 50) -> 1

        - nada().unwrap_or_else(lambda: 100 + 50) -> 150

        :param fn: function to get a value from
        :param args: sequential arguments to pass to fn
        :param kwargs: keyword arguments to pass to fn
        :return: Internal value or function return
        """
        if self.value is not None:
            return self.value

        return fn(*args, **kwargs)

    def or_else(self, fn: Callable, *args, **kwargs) -> "Option[T | MapFn]":
        """
        Returns an Option whose internal value is either its original contents, or the result of fn

        Examples:

        - some(1).or_else(lambda: 100 + 50) -> some(1)

        - nada().or_else(lambda: 100 + 50) -> some(150)

        :param fn: function to get a value from
        :param args: sequential arguments to pass to fn
        :param kwargs: keyword arguments to pass to fn
        :return: Option with new internal value
        """
        if self.is_some():
            return self

        result = fn(*args, **kwargs)

        if result is None:
            return nada()

        return some(result)

    # -- IFunctor Implementation

    def flatten(self) -> 'Option[T]':
        """
        Create an Option whose internal value does not contain nested Options.

        Examples:

        - some(some(some(1))) -> some(1)

        - some(1) -> some(1)

        - nada() -> nada()

        :return: Flattened Option
        """
        if self.is_nada():
            return self

        current: Option[T] = some(self.value)

        while isinstance(current.value, Option):
            current: Option[T] = some(current.value.value)

        return current

    def map(self, fn: MapFn) -> 'Option[T]':
        """
        Create an Option whose internal value is changed by fn.

        Examples:

        - some(1).map(lambda x: x + 1) -> some(2)

        - nada().map(lambda x: x + 1) -> nada()

        :param fn: Function that takes one argument T and returns another T
        :return: Mapped Option
        """
        if self.is_nada():
            return self

        return some(fn(self.value))

    def flatmap(self, fn: MapFn) -> 'Option[T]':
        """
        Flatten an Option and map it with a function

        Examples:

        - some(some(1)).flatmap(lambda x: x + 1) -> some(2)

        - some(10).flatmap(lambda x: x + 1) -> some(11)

        - nada().flatmap(lambda x: x + 1) -> nada()

        :param fn: Function that takes one argument T and returns another T
        :return: Flattened and Mapped Option
        """
        return self.flatten().map(fn)

    # --- END Interface Implementations

    @classmethod
    def some(cls, value: T) -> "Option[T]":
        """
        Create an Option with a non-None value

        Examples:

        - Option.some(10) -> Option[int]

        - Option.some(None) -> Raises OptionException

        :param value: Any non-None value
        :return: Option(value)
        """
        if value is None:
            raise OptionException('Option.some(value: T) cannot take None as a value argument')

        return cls(value)

    @classmethod
    def nada(cls) -> "Option[T]":
        """
        Create an Option with None value

        Example: Option.nada() -> Option

        :return: Option(None)
        """
        return cls(None)

    def is_some(self) -> bool:
        """
        Check that Option's internal value is not None

        Examples:

        - some(10).is_some() -> True

        - nada() -> False

        :return: True if internal value is not None, else False
        """
        return self.value is not None

    def is_some_and(self, predicate: Predicate) -> bool:
        """
        Check that Option's internal value is not None, and predicate function
        returns True.

        Examples

        - some(2).is_some_and(lambda x: x % 2 == 0) -> True

        - some(5).is_some_and(lambda x: x % 2 == 0) -> False

        - nada().is_some_and(lambda x: x % 2 == 0) -> False

        :param predicate: Function taking internal value as only argument, returns bool
        :return: True if internal value is not None and predicate returns True, else False
        """
        if self.is_nada():
            return False

        return predicate(self.value)

    def is_nada(self) -> bool:
        """
        Check that Option's internal value is None

        Examples:

        - some(10).is_nada() -> False

        - nada().is_nada() -> True

        :return: True if value is None, else False
        """
        return self.value is None

    def is_nada_or(self, predicate: Predicate) -> bool:
        """
        Return True if internal value is None, or predicate is True

        Examples:

        - nada().is_nada_or(lambda x: x % 2 == 0) -> True

        - some(10).is_nada_or(lambda x: x % 2 == 0) -> True

        - some(5).is_nada_or(lambda x: x % 2 == 0) -> False

        :param predicate: Function taking internal value as only argument, returns bool
        :return: True if value is None or predicate returns True, else False
        """
        return self.is_nada() or predicate(self.value)

    def ok_or[E](self, error: E) -> "Result[T,E]":
        """
        Convert Option to Result.ok() if internal value is Some, else Result.err() with custom error message.

        Examples:

        - some(10).ok_or('Option is None') -> ok(10)

        - nada().ok_or('Option is None') -> err('Option is None')

        :param error: Error message
        :return: Result
        """
        if self.is_nada():
            return err(error)

        return ok(self.value)

    def ok_or_else[E](self, fn: Callable, *args, **kwargs) -> "Result[T,E]":
        """
        Convert Option to Result.ok() if internal value is Some, else Result.err() with value from
        fn's return value

        Examples:

        - some(10).ok_or_else(lambda x: f'Custom error: {x}', 10) -> ok(10)

        - nada().ok_or_else(lambda x: f'Custom error: {x}', 10) -> err('Custom error: 10')

        :param fn: Function to create error content from
        :return: Result
        """
        if self.is_nada():
            return err(fn(*args, **kwargs))

        return ok(self.value)

    def filter(self, predicate: Predicate) -> "Option[T]":
        """
        Return some(self.value) if predicate returns True, else return nada()

        Examples:

        - some(10).filter(lambda x: x % 2 == 0) -> some(10)

        - some(5).filter(lambda x: x % 2 == 0) -> nada()

        - nada().filter(lambda x: x % 2 == 0) -> nada()

        :param predicate: Function that takes internal value as only argument, returns bool
        :return: Option
        """
        if self.is_nada():
            return self

        if predicate(self.value):
            return some(self.value)

        return nada()

    def other_if_some(self, other_option: "Option[T]") -> "Option[T]":
        """
        Return nada() if Option's internal value is None, otherwise return a different Option

        Examples:

        - some(10).other_if_some(some(15)) -> some(15)

        - nada().other_if_some(some(15)) -> nada()

        :param other_option: Another Option
        :return: Option
        """
        if self.is_some():
            return other_option

        return self

    def other_if_nada(self, other_option: "Option[T]") -> "Option[T]":
        """
        Return another Option if internal value is None, otherwise return original Option

        Examples:

        - some(10).other_if_nada(some(15)) -> some(10)

        - nada().other_if_nada(some(15)) -> some(15)

        :param other_option: Another Option
        :return: Option
        """
        if self.is_nada():
            return other_option

        return self

    def zip(self, other_option: "Option[T]") -> "Option[tuple[T, T]]":
        """
        Return tuple in an Option if both Options' internal values are not None, else return nada()

        Examples:

        - some(10).zip(some(15)) -> some((10, 15))

        - some(10).zip(nada()) -> nada()

        - nada().zip(some(10)) -> nada()

        - nada().zip(nada()) -> nada()

        :param other_option: Another Option
        :return: some(tuple())
        """
        if self.is_some() and other_option.is_some():
            return some((self.value, other_option.value))

        return nada()

    def unzip(self) -> "tuple[Option[T], Option[T]]":
        """
        Return a tuple of Options from an Option with an internal tuple value

        Examples:

        - some((10, 15)).unzip() -> (some(10), some(15))

        - some((10, None)).unzip() -> (some(10), nada())

        - Option((None, None)).unzip() -> (nada(), nada())

        :return: tuple(Option, Option)
        """
        if not isinstance(self.value, tuple):
            return nada(), nada()

        first, second = self.value
        first_opt = nada()
        second_opt = nada()

        if first is not None:
            first_opt = some(first)

        if second is not None:
            second_opt = some(second)

        return first_opt, second_opt


def some[T](value: T) -> Option[T]:
    """
        Create an Option with a non-None value

        Examples:

        - some(10) -> Option[int]

        - some(None) -> Raises OptionException

        :param value: Any non-None value
        :return: Option(value)
        """
    return Option.some(value)


def nada() -> Option:
    """
        Create an Option with None value

        Example: nada() -> Option

        :return: Option(None)
        """
    return Option.nada()
