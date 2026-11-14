from collections.abc import Callable

lazy from src.lib.abstract.iequality import IEquality
lazy from src.lib.abstract.ifunctor import IFunctor
lazy from src.lib.abstract.imonad import IMonad
lazy from src.lib.abstract.irepr import IRepr
lazy from src.lib.monads.result import Result, Ok, Err


class MaybeException[E](Exception):
    """Custom exception for Maybe type"""

    def __init__(self, message: E) -> None:
        self.message = message
        super().__init__(self.message)


class Maybe[T](IRepr, IMonad[T], IFunctor[T], IEquality):
    """Rust-style option"""
    __match_args__ = ('value',)

    def __init__(self, value: T | None):
        self.value: T | None = value

    def __bool__(self) -> bool:
        """
        Convert Maybe to a truthy value

        Examples:

        - bool(Some(10)) -> True
        - bool(Nada()) -> False

        :return: True if Maybe.value is not None, else False
        """
        return self.is_some()

    # -- IRepr Implementation

    def __repr__(self) -> str:
        """
        String representation of Maybe

        Examples:

        - str(Some(10)) -> 'Some(10)'
        - str(Nada()) -> 'Nada'

        :return: str(Maybe)
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

        :param other: Second Maybe to compare with
        :return: True if both Options values are equal, else False
        """
        if not isinstance(other, Maybe):
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

        :param other: Second Maybe to compare with
        :return: True if both Options values are not equal, else False
        """
        if not isinstance(other, Maybe):
            return NotImplemented

        return self.value != other.value

    # --- IMonad Implementation

    def expect[E](self, message: E) -> T:
        """
        Get Maybe.value if it is not None, or raise an OptionException with a custom message

        Examples:

        - Some(1).expect('Not a number') -> 1
        - Nada().expect('Not a number') -> raise OptionException('Not a number')

        :param message: Error message
        :return: Maybe.value
        """
        if self.value is None:
            raise MaybeException(message)

        return self.value

    def unwrap(self) -> T:
        """
        Get Maybe.value if it is not None, or raise an OptionException

        Examples:

        - Some(1).unwrap() -> 1
        - Nada().unwrap() -> raise OptionException("Cannot unwrap Nada")

        :return: Maybe.value
        """
        if self.value is None:
            raise MaybeException("Cannot unwrap Nada")

        return self.value

    def unwrap_or(self, default: T) -> T:
        """
        Get Maybe.value if it is not None, or else a default value

        Examples:

        - Some(1).unwrap_or(10) -> 1
        - Nada().unwrap_or(10) -> 10

        :param default: Default value
        :return: Maybe.value or default value
        """
        if self.value is None:
            return default

        return self.value

    def unwrap_or_else(self, fn: Callable, *args, **kwargs) -> T | Callable:
        """
        Get Maybe.value if it is not None, or else the returned value of a function

        Examples:

        - Some(1).unwrap_or_else(lambda: 100 + 50) -> 1
        - Nada().unwrap_or_else(lambda: 100 + 50) -> 150

        :param fn: function to get a value from
        :param args: sequential arguments to pass to fn
        :param kwargs: keyword arguments to pass to fn
        :return: Maybe.value or function return
        """
        if self.value is not None:
            return self.value

        return fn(*args, **kwargs)

    def or_else(self, fn: Callable, *args, **kwargs) -> "Maybe[T | Callable[[T], T]]":
        """
        Returns a Maybe with Maybe.value being either original Maybe.value or the result of fn

        Examples:

        - Some(1).or_else(lambda: 100 + 50) -> Some(1)
        - Nada().or_else(lambda: 100 + 50) -> Some(150)

        :param fn: function to get a value from
        :param args: sequential arguments to pass to fn
        :param kwargs: keyword arguments to pass to fn
        :return: self or Maybe(fn(*args, **kwargs))
        """
        if self.is_some():
            return Some(self.value)

        result = fn(*args, **kwargs)

        if result is None:
            return Nada()

        return Some(result)

    # -- IFunctor Implementation

    def flatten(self) -> 'Maybe[T]':
        """
        Return innermost Maybe in nested Options

        Examples:

        - Some(Some(Some(1))).flatten() -> Some(1)
        - Some(1).flatten() -> Some(1)
        - Nada().flatten() -> Nada()

        :return: Innermost Maybe
        """
        if self.is_nada():
            return Nada()

        current: Maybe[T] = Some(self.value)

        while isinstance(current.value, Maybe):
            current: Maybe[T] = Some(current.value.value)

        return current

    def map(self, fn: Callable[[T], T]) -> 'Maybe[T]':
        """
        Create a Maybe where Maybe.value = fn(Maybe.value).

        Examples:

        - Some(1).map(lambda x: x + 1) -> Some(Some(2))
        - Nada().map(lambda x: x + 1) -> Nada()

        :param fn: Function that takes one argument T and returns another T
        :return: Mapped Maybe
        """
        if self.is_nada():
            return Nada()

        return Some(fn(self.value))

    def flatmap(self, fn: Callable[[T], T]) -> 'Maybe[Callable[[T], T]]':
        """
        Flatten a Maybe and map it with a function

        Examples:

        - Some(Some(1)).flatmap(lambda x: x + 1) -> Some(2)
        - Some(10).flatmap(lambda x: x + 1) -> Some(11)
        - Nada().flatmap(lambda x: x + 1) -> Nada()

        :param fn: Function that takes one argument T and returns another T
        :return: Flattened and Mapped Maybe
        """
        return self.flatten().map(fn)

    # --- END Interface Implementations

    @classmethod
    def some(cls, value: T) -> "Maybe[T]":
        """
        Create a Maybe with a non-None value

        Examples:

        - Maybe.some(10) -> Maybe[int]
        - Maybe.some(None) -> Raises OptionException

        :param value: Any non-None value
        :return: Maybe(value)
        """
        if value is None:
            raise MaybeException('Maybe.some(value: T) cannot take None as a value argument')

        return cls(value)

    @classmethod
    def nada(cls) -> "Maybe[T]":
        """
        Create a Maybe with None value
        Example: Maybe.nada() -> Maybe
        :return: Maybe(None)
        """
        return cls(None)

    def is_some(self) -> bool:
        """
        Check that Maybe.value is not None

        Examples:

        - Some(10).is_some() -> True
        - Nada() -> False

        :return: True if Maybe.value is not None, else False
        """
        return self.value is not None

    def is_some_and(self, predicate: Callable[[T], bool]) -> bool:
        """
        Check that Maybe.value is not None, and predicate function
        returns True.

        Examples

        - Some(2).is_some_and(lambda x: x % 2 == 0) -> True
        - Some(5).is_some_and(lambda x: x % 2 == 0) -> False
        - Nada().is_some_and(lambda x: x % 2 == 0) -> False

        :param predicate: Function taking Maybe.value as only argument, returns bool
        :return: True if Maybe.value is not None and predicate returns True, else False
        """
        if self.is_nada():
            return False

        return predicate(self.value)

    def is_nada(self) -> bool:
        """
        Check that Maybe.value is None

        Examples:

        - Some(10).is_nada() -> False
        - Nada().is_nada() -> True

        :return: True if value is None, else False
        """
        return self.value is None

    def is_nada_or(self, predicate: Callable[[T], bool]) -> bool:
        """
        Return True if Maybe.value is None, or predicate is True

        Examples:

        - Nada().is_nada_or(lambda x: x % 2 == 0) -> True
        - Some(10).is_nada_or(lambda x: x % 2 == 0) -> True
        - Some(5).is_nada_or(lambda x: x % 2 == 0) -> False

        :param predicate: Function taking Maybe.value as only argument, returns bool
        :return: True if value is None or predicate returns True, else False
        """
        return self.is_nada() or predicate(self.value)

    def ok_or[E](self, error: E) -> "Result[T,E]":
        """
        Convert Maybe to Result.ok() if Maybe.value is Some, else Result.err() with custom error message.

        Examples:

        - Some(10).ok_or('Maybe is None') -> ok(10)
        - Nada().ok_or('Maybe is None') -> err('Maybe is None')

        :param error: Error message
        :return: Result
        """
        if self.is_nada():
            return Err(error)

        return Ok(self.value)

    def ok_or_else(self, fn: Callable, *args, **kwargs) -> "Result[T,Callable[[T], T]]":
        """
        Convert Maybe to Result.ok() if Maybe.value is Some, else Result.err() with value from
        fn's return value

        Examples:

        - Some(10).ok_or_else(lambda x: f'Custom error: {x}', 10) -> ok(10)
        - Nada().ok_or_else(lambda x: f'Custom error: {x}', 10) -> err('Custom error: 10')

        :param fn: Function to create error content from
        :return: Result
        """
        if self.is_nada():
            return Err(fn(*args, **kwargs))

        return Ok(self.value)

    def filter(self, predicate: Callable[[T], bool]) -> "Maybe[T]":
        """
        Return Some(self.value) if predicate returns True, else return Nada()

        Examples:

        - Some(10).filter(lambda x: x % 2 == 0) -> Some(10)
        - Some(5).filter(lambda x: x % 2 == 0) -> Nada()
        - Nada().filter(lambda x: x % 2 == 0) -> Nada()

        :param predicate: Function that takes Maybe.value as only argument, returns bool
        :return: Maybe
        """
        if self.is_nada():
            return Nada()

        if predicate(self.value):
            return Some(self.value)

        return Nada()

    def other_if_some(self, other: "Maybe[T]") -> "Maybe[T]":
        """
        Return Nada() if Maybe.value is None, otherwise return a different Maybe

        Examples:

        - Some(10).other_if_some(Some(15)) -> Some(15)
        - Nada().other_if_some(Some(15)) -> Nada()

        :param other: Another Maybe instance
        :return: Maybe
        """
        if self.is_some():
            return other

        return self

    def other_if_nada(self, other: "Maybe[T]") -> "Maybe[T]":
        """
        Return another Maybe if Maybe.value is None, otherwise return original Maybe

        Examples:

        - Some(10).other_if_nada(Some(15)) -> Some(10)
        - Nada().other_if_nada(Some(15)) -> Some(15)

        :param other: Another Maybe instance
        :return: Maybe
        """
        if self.is_nada():
            return other

        return self

    def zip(self, other: "Maybe[T]") -> "Maybe[tuple[T, T]]":
        """
        Return tuple in a Maybe if both Options are not Nada(), else return Nada()

        Examples:

        - Some(10).zip(Some(15)) -> Some((10, 15))
        - Some(10).zip(Nada()) -> Nada()
        - Nada().zip(Some(10)) -> Nada()
        - Nada().zip(Nada()) -> Nada()

        :param other: Another Maybe
        :return: Some(tuple())
        """
        if self.is_some() and other.is_some():
            return Some((self.value, other.value))

        return Nada()

    def unzip(self) -> "tuple[Maybe[T], Maybe[T]]":
        """
        Return a tuple of Options from a Maybe with an internal tuple value

        Examples:

        - Some((10, 15)).unzip() -> (Some(10), Some(15))
        - Some((10, None)).unzip() -> (Some(10), Nada())
        - Maybe((None, None)).unzip() -> (Nada(), Nada())

        :return: tuple(Maybe, Maybe)
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


class Some[T](Maybe[T]):
    """Creates a Maybe[T] with a non-None value"""

    def __init__(self, value: T):
        if value is None:
            raise MaybeException('Some(value: T) cannot take None as a value argument')

        super().__init__(value)


class Nada[T](Maybe[T]):
    """Creates a Maybe[T] with a None value"""

    def __init__(self):
        super().__init__(None)
