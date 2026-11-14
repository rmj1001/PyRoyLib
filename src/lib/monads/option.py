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
    __match_args__ = ('value',)

    def __init__(self, value: T | None):
        self.value: T | None = value

    def __bool__(self) -> bool:
        """
        Convert Option to a truthy value

        Examples:

        - bool(Some(10)) -> True

        - bool(Nada()) -> False

        :return: True if internal value is not None, else False
        """
        return self.is_some()

    # -- IRepr Implementation

    def __repr__(self) -> str:
        """
        String representation of Option

        Examples:

        - str(Some(10)) -> 'Some(10)'

        - str(Nada()) -> 'Nada'

        :return: str(Option)
        """
        if self.value is not None:
            return f"Some({self.value})"

        return "Nada"

    # -- IEquality Implementation

    def __eq__(self, other: object) -> bool:
        """
        Check if two Options are equal

        Examples:

        - Some(1) == Some(2) -> False

        - Some(10) == Nada() -> False

        - Some(10) == Some(10) -> True

        - Nada() == Nada() -> True
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

        - Some(1) != Some(2) -> True

        - Some(10) != Nada() -> True

        - Some(10) != Some(10) -> False

        - Nada() != Nada() -> False

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

        - Some(1).expect('Not a number') -> 1

        - Nada().expect('Not a number') -> raise OptionException('Not a number')

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

        - Some(1).unwrap() -> 1

        - Nada().unwrap() -> raise OptionException("Cannot unwrap Nada")

        :return: Internal value
        """
        if self.value is None:
            raise OptionException("Cannot unwrap Nada")

        return self.value

    def unwrap_or(self, default: T) -> T:
        """
        Get internal value if it is not None, or else a default value

        Examples:

        - Some(1).unwrap_or(10) -> 1

        - Nada().unwrap_or(10) -> 10

        :return: Internal or default value
        """
        if self.value is None:
            return default

        return self.value

    def unwrap_or_else(self, fn: Callable, *args, **kwargs) -> T | Callable:
        """
        Get internal value if it is not None, or else the returned value of a function

        Examples:

        - Some(1).unwrap_or_else(lambda: 100 + 50) -> 1

        - Nada().unwrap_or_else(lambda: 100 + 50) -> 150

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

        - Some(1).or_else(lambda: 100 + 50) -> Some(1)

        - Nada().or_else(lambda: 100 + 50) -> Some(150)

        :param fn: function to get a value from
        :param args: sequential arguments to pass to fn
        :param kwargs: keyword arguments to pass to fn
        :return: Option with new internal value
        """
        if self.is_some():
            return self

        result = fn(*args, **kwargs)

        if result is None:
            return Nada()

        return Some(result)

    # -- IFunctor Implementation

    def flatten(self) -> 'Option[T]':
        """
        Create an Option whose internal value does not contain nested Options.

        Examples:

        - Some(Some(Some(1))) -> Some(1)

        - Some(1) -> Some(1)

        - Nada() -> Nada()

        :return: Flattened Option
        """
        if self.is_nada():
            return self

        current: Option[T] = Some(self.value)

        while isinstance(current.value, Option):
            current: Option[T] = Some(current.value.value)

        return current

    def map(self, fn: MapFn) -> 'Option[T]':
        """
        Create an Option whose internal value is changed by fn.

        Examples:

        - Some(1).map(lambda x: x + 1) -> Some(2)

        - Nada().map(lambda x: x + 1) -> Nada()

        :param fn: Function that takes one argument T and returns another T
        :return: Mapped Option
        """
        if self.is_nada():
            return self

        return Some(fn(self.value))

    def flatmap(self, fn: MapFn) -> 'Option[T]':
        """
        Flatten an Option and map it with a function

        Examples:

        - Some(Some(1)).flatmap(lambda x: x + 1) -> Some(2)

        - Some(10).flatmap(lambda x: x + 1) -> Some(11)

        - Nada().flatmap(lambda x: x + 1) -> Nada()

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

        - Some10).is_some() -> True

        - Nada() -> False

        :return: True if internal value is not None, else False
        """
        return self.value is not None

    def is_some_and(self, predicate: Predicate) -> bool:
        """
        Check that Option's internal value is not None, and predicate function
        returns True.

        Examples

        - Some(2).is_some_and(lambda x: x % 2 == 0) -> True

        - Some(5).is_some_and(lambda x: x % 2 == 0) -> False

        - Nada().is_some_and(lambda x: x % 2 == 0) -> False

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

        - Some(10).is_nada() -> False

        - Nada().is_nada() -> True

        :return: True if value is None, else False
        """
        return self.value is None

    def is_nada_or(self, predicate: Predicate) -> bool:
        """
        Return True if internal value is None, or predicate is True

        Examples:

        - Nada().is_nada_or(lambda x: x % 2 == 0) -> True

        - Some(10).is_nada_or(lambda x: x % 2 == 0) -> True

        - Some(5).is_nada_or(lambda x: x % 2 == 0) -> False

        :param predicate: Function taking internal value as only argument, returns bool
        :return: True if value is None or predicate returns True, else False
        """
        return self.is_nada() or predicate(self.value)

    def ok_or[E](self, error: E) -> "Result[T,E]":
        """
        Convert Option to Result.ok() if internal value is Some, else Result.err() with custom error message.

        Examples:

        - Some(10).ok_or('Option is None') -> ok(10)

        - Nada().ok_or('Option is None') -> err('Option is None')

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

        - Some(10).ok_or_else(lambda x: f'Custom error: {x}', 10) -> ok(10)

        - Nada().ok_or_else(lambda x: f'Custom error: {x}', 10) -> err('Custom error: 10')

        :param fn: Function to create error content from
        :return: Result
        """
        if self.is_nada():
            return err(fn(*args, **kwargs))

        return ok(self.value)

    def filter(self, predicate: Predicate) -> "Option[T]":
        """
        Return Some(self.value) if predicate returns True, else return Nada()

        Examples:

        - Some(10).filter(lambda x: x % 2 == 0) -> Some(10)

        - Some(5).filter(lambda x: x % 2 == 0) -> Nada()

        - Nada().filter(lambda x: x % 2 == 0) -> Nada()

        :param predicate: Function that takes internal value as only argument, returns bool
        :return: Option
        """
        if self.is_nada():
            return self

        if predicate(self.value):
            return Some(self.value)

        return Nada()

    def other_if_some(self, other_option: "Option[T]") -> "Option[T]":
        """
        Return Nada() if Option's internal value is None, otherwise return a different Option

        Examples:

        - Some(10).other_if_some(Some(15)) -> Some(15)

        - Nada().other_if_some(Some(15)) -> Nada()

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

        - Some(10).other_if_nada(Some(15)) -> Some(10)

        - Nada().other_if_nada(Some(15)) -> Some(15)

        :param other_option: Another Option
        :return: Option
        """
        if self.is_nada():
            return other_option

        return self

    def zip(self, other_option: "Option[T]") -> "Option[tuple[T, T]]":
        """
        Return tuple in an Option if both Options' internal values are not None, else return Nada()

        Examples:

        - Some(10).zip(Some(15)) -> some((10, 15))

        - Some(10).zip(Nada()) -> Nada()

        - Nada().zip(Some(10)) -> Nada()

        - Nada().zip(Nada()) -> Nada()

        :param other_option: Another Option
        :return: Some(tuple())
        """
        if self.is_some() and other_option.is_some():
            return Some((self.value, other_option.value))

        return Nada()

    def unzip(self) -> "tuple[Option[T], Option[T]]":
        """
        Return a tuple of Options from an Option with an internal tuple value

        Examples:

        - some((10, 15)).unzip() -> (Some(10), Some(15))

        - some((10, None)).unzip() -> (Some(10), Nada())

        - Option((None, None)).unzip() -> (Nada(), Nada())

        :return: tuple(Option, Option)
        """
        if not isinstance(self.value, tuple):
            return Nada(), Nada()

        first, second = self.value
        first_opt = Nada()
        second_opt = Nada()

        if first is not None:
            first_opt = Some(first)

        if second is not None:
            second_opt = Some(second)

        return first_opt, second_opt


class Some[T](Option[T]):
    """Creates an Option[T] with a non-None internal value"""
    def __init__(self, value: T):
        super().__init__(value)


class Nada[T](Option[T]):
    """Creates an Option[T] with a None internal value"""
    def __init__(self):
        super().__init__(None)
