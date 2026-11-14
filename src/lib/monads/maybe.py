from collections.abc import Callable
from functools import wraps

lazy from src.lib.monads.result import Result, Ok, Err, panic


class MaybeException[E](Exception):
    """Custom exception for Maybe type"""

    def __init__(self, message: E) -> None:
        self.message = message
        super().__init__(self.message)


class Maybe[T]:
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

    def and_then[U](self, fn: "Callable[[T], Maybe[U]]") -> "Maybe[U]":
        """
        Return a new Maybe created from fn return if Maybe is Some, else return Nada()

        Examples:

        - Some(1).and_then(lambda x: Some(x + 1)) -> Some(2)
        - Nada().and_then(lambda x: Some(x + 1)) -> Nada()

        :param fn: Function that takes one argument T and returns Maybe[U]
        :return: Mapped Maybe
        """
        match self:
            case Some(s):
                return fn(s)
            case Nada():
                return Nada()
            case _:
                panic('Unreachable', maybe=True)

    def expect(self, message: str) -> T:
        """
        Get Maybe.value if it is not None, or panic with a custom message

        Examples:

        - Some(1).expect('Not a number') -> 1
        - Nada().expect('Not a number') -> panic('Not a number')

        :param message: Error message
        :return: Maybe.value
        """
        match self:
            case Some(s):
                return s
            case Nada():
                panic(message, maybe=True)
            case _:
                panic('Unreachable', maybe=True)

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
        match self:
            case Some(s):
                if predicate(s):
                    return Some(s)
                else:
                    return Nada()
            case Nada():
                return Nada()
            case _:
                panic('Unreachable', maybe=True)

    def flatten(self, recursive: bool = False) -> "Maybe[T]":
        """
        Return innermost Maybe in nested Options

        Examples:

        - Some(Some(Some(1))).flatten(recursive=True) -> Some(1)
        - Some(Some(1)).flatten() -> Some(1)
        - Nada().flatten() -> Nada()

        :param recursive: Flattens all layers if True, otherwise flattens one layer
        :return: Innermost Maybe
        """
        match self:
            case Some(s):
                inner: T | None = s

                if isinstance(inner, Maybe) and recursive:
                    return inner.flatten(recursive)
                elif isinstance(inner, Maybe):
                    return inner
                else:
                    return Some(s)
            case Nada():
                return Nada()
            case _:
                panic('Unreachable', maybe=True)

    def inspect(self, fn: Callable[[T], None]) -> "Maybe[T]":
        """
        Calls fn with contained value if Some. Always returns original Maybe object.

        Examples:

        - Some(1).inspect(lambda x: print(x)) -> prints 1 to STDOUT
        - Nada().inspect(lambda x: print(x)) -> does nothing

        :param fn: function that takes one argument T and returns None
        :return: Original Maybe
        """
        match self:
            case Some(s):
                fn(s)
                return Some(s)
            case Nada():
                return Nada()
            case _:
                panic('Unreachable', maybe=True)

    def is_nada(self) -> bool:
        """
        Check that Maybe.value is None

        Examples:

        - Some(10).is_nada() -> False
        - Nada().is_nada() -> True

        :return: True if value is None, else False
        """
        match self:
            case Some(_):
                return False
            case Nada():
                return True
            case _:
                panic('Unreachable', maybe=True)

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
        match self:
            case Some(s):
                return predicate(s)
            case Nada():
                return True
            case _:
                panic('Unreachable', maybe=True)

    def is_some(self) -> bool:
        """
        Check that Maybe.value is not None

        Examples:

        - Some(10).is_some() -> True
        - Nada().is_some() -> False

        :return: True if Maybe.value is not None, else False
        """
        match self:
            case Some(_):
                return True
            case Nada():
                return False
            case _:
                panic('Unreachable', maybe=True)

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
        match self:
            case Some(s):
                return predicate(s)
            case Nada():
                return False
            case _:
                panic('Unreachable', maybe=True)

    def map[U](self, fn: Callable[[T], U]) -> "Maybe[U]":
        """
        Create a Maybe where Maybe.value = fn(Maybe.value).

        Examples:

        - Some(1).map(lambda x: x + 1) -> Some(2)
        - Nada().map(lambda x: x + 1) -> Nada()

        :param fn: Function that takes one argument T and returns another U
        :return: Mapped Maybe
        """
        match self:
            case Some(s):
                return Some(fn(s))
            case Nada():
                return Nada()
            case _:
                panic('Unreachable', maybe=True)

    def map_or[U](self, default: U, fn: Callable[[T], U]) -> U:
        """
        Convert Maybe to fn(T) if Some, else convert to default

        Examples:

        - Some(1).map_or(3, lambda x: x + 1) -> 2
        - Nada().map_or(3, lambda x: x + 1) -> 3

        :param default: Default value
        :param fn: Function that takes one argument T and returns U
        :return: default or fn(Maybe.value)
        """
        match self:
            case Some(s):
                return fn(s)
            case Nada():
                return default
            case _:
                panic('Unreachable', maybe=True)

    def map_or_else[U](self, default: Callable[[], U], fn: Callable[[T], U]) -> U:
        """
        Convert Maybe to default() if Nada, else fn(Maybe.value)

        Examples:

        - Some(1).map_or_else(lambda: 6, lambda x: x + 1) -> 2
        - Nada().map_or_else(lambda: 6, lambda x: x + 1) -> 6

        :param default: Default function taking no arguments
        :param fn: Function that takes one argument T and returns U
        :return: default() or fn(Maybe.value)
        """
        match self:
            case Some(s):
                return fn(s)
            case Nada():
                return default()
            case _:
                panic('Unreachable', maybe=True)

    def ok_or[E](self, err: E) -> Result[T, E]:
        """
        Convert Maybe to Result.ok() if Maybe.value is Some, else Result.err() with custom error message.

        Examples:

        - Some(10).ok_or('Maybe is None') -> Ok(10)
        - Nada().ok_or('Maybe is None') -> Err('Maybe is None')

        :param err: Error message
        :return: Result
        """
        match self:
            case Some(s):
                return Ok(s)
            case Nada():
                return Err(err)
            case _:
                panic('Unreachable', maybe=True)

    def ok_or_else[E](self, fn: Callable[[], E]) -> Result[T, E]:
        """
        Convert Maybe to Result.ok() if Maybe.value is Some, else Result.err() with value from fn's return

        Examples:

        - Some(10).ok_or_else(lambda: 'Custom error') -> Ok(10)
        - Nada().ok_or_else(lambda: 'Custom error') -> Err('Custom error')

        :param fn: Function to create error content from
        :return: Result
        """
        match self:
            case Some(s):
                return Ok(s)
            case Nada():
                return Err(fn())
            case _:
                panic('Unreachable', maybe=True)

    def or_else(self, fn: "Callable[[], Maybe[T]]") -> "Maybe[T]":
        """
        Returns self if Maybe is Some, or else a new Maybe sourced from called function

        Examples:

        - Some(1).or_else(lambda: Some(150)) -> Some(1)
        - Nada().or_else(lambda: Some(150)) -> Some(150)

        :param fn: function to get a Maybe from
        :return: self or fn()
        """
        match self:
            case Some(s):
                return Some(s)
            case Nada():
                return fn()
            case _:
                panic('Unreachable', maybe=True)

    def other_if_some[U](self, other: "Maybe[U]") -> "Maybe[T|U]":
        """
        Returns Nada if self is Nada, else returns other Maybe object

        Examples:

        - Some(1).other_if_some(Some(10)) -> Some(10)
        - Nada().other_if_some(Some(10)) -> Nada()

        :param other: Other Maybe
        :return: Maybe object
        """
        match self:
            case Some(s):
                return other
            case Nada():
                return Nada()
            case _:
                panic('Unreachable', maybe=True)

    def other_if_nada[U](self, other: "Maybe[U]") -> "Maybe[T|U]":
        """
        Returns self if self is Some, else returns other Maybe object

        Examples:

        - Some(1).other_if_nada(Some(10)) -> Some(1)
        - Nada().other_if_nada(Some(10)) -> Some(10)

        :param other: Other Maybe
        :return: Maybe object
        """
        match self:
            case Some(s):
                return Some(s)
            case Nada():
                return other
            case _:
                panic('Unreachable', maybe=True)

    def reduce(self, other: "Maybe[T]", fn: Callable[[T, T], T]) -> "Maybe[T]":
        """
        Reduces two Options into one by applying a function.
        If one is Nada, returns the other. If both are Nada, returns Nada.

        Examples:
        - Some(2).reduce(Some(3), lambda x, y: x + y) -> Some(5)
        - Some(2).reduce(Nada(), lambda x, y: x + y) -> Some(2)
        - Nada().reduce(Nada(), lambda x, y: x + y) -> Nada()
        """
        match self, other:
            case Some(x), Some(y):
                return Some(fn(x, y))
            case Some(x), Nada():
                return Some(x)
            case Nada(), Some(y):
                return Some(y)
            case Nada(), Nada():
                return Nada()
            case _:
                panic('Unreachable', maybe=True)

    def unwrap(self) -> T:
        """
        Get Maybe.value if it is not None, or panic

        Examples:

        - Some(1).unwrap() -> 1
        - Nada().unwrap() -> panic("Option is Nada")

        :return: Maybe.value
        """
        match self:
            case Some(s):
                return s
            case Nada():
                panic('Option is Nada', maybe=True)
            case _:
                panic('Unreachable', maybe=True)

    def unwrap_or(self, default: T) -> T:
        """
        Get Maybe.value if it is not None, or else a default value

        Examples:

        - Some(1).unwrap_or(10) -> 1
        - Nada().unwrap_or(10) -> 10

        :param default: Default value
        :return: Maybe.value or default value
        """
        match self:
            case Some(s):
                return s
            case Nada():
                return default
            case _:
                panic('Unreachable', maybe=True)

    def unwrap_or_else(self, fn: Callable[[], T]) -> T:
        """
        Get Maybe.value if it is not None, or else the returned value of a function

        Examples:

        - Some(1).unwrap_or_else(lambda: 150) -> 1
        - Nada().unwrap_or_else(lambda: 150) -> 150

        :param fn: function to get a default value from
        :return: Maybe.value or function return
        """
        match self:
            case Some(s):
                return s
            case Nada():
                return fn()
            case _:
                panic('Unreachable', maybe=True)

    def unzip[U](self: "Maybe[tuple[T, U]]") -> "tuple[Maybe[T], Maybe[U]]":
        """
        Return a tuple of Options from a Maybe with an internal tuple value

        Examples:

        - Some((10, 15)).unzip() -> (Some(10), Some(15))
        - Nada().unzip() -> (Nada(), Nada())

        :return: tuple(Maybe, Maybe)
        """
        match self:
            case Some((x, y)):
                return Some(x), Some(y)
            case Nada():
                return Nada(), Nada()
            case _:
                panic('Unreachable', maybe=True)

    def xor(self, other: "Maybe[T]") -> "Maybe[T]":
        """
        Return Some if only self is Some or if only other is Some, else Nada

        Examples:

        - Some(10).xor(Nada()) -> Some(10)
        - Nada().xor(Some(10)) -> Some(10)
        - Some(10).xor(Some(20)) -> Nada()
        - Nada().xor(Nada()) -> Nada()

        :param other: Other Maybe object
        :return: Maybe object
        """
        match self, other:
            case Some(x), Nada():
                return Some(x)
            case Nada(), Some(x):
                return Some(x)
            case _:
                return Nada()

    def zip[U](self, other: "Maybe[U]") -> "Maybe[tuple[T, U]]":
        """
        Return tuple in a Maybe if both Options are not Nada(), else return Nada()

        Examples:

        - Some(10).zip(Some(15)) -> Some((10, 15))
        - Some(10).zip(Nada()) -> Nada()
        - Nada().zip(Some(10)) -> Nada()
        - Nada().zip(Nada()) -> Nada()

        :param other: Another Maybe
        :return: Some(tuple()) or Nada()
        """
        match self, other:
            case Some(x), Some(y):
                return Some((x, y))
            case Nada(), _:
                return Nada()
            case _, Nada():
                return Nada()
            case _:
                panic('Unreachable', maybe=True)


class Some[T](Maybe[T]):
    """Creates a Maybe[T] with a non-None value"""

    def __init__(self, value: T):
        if value is None:
            panic('Some(value: T) cannot take None as a value argument', maybe=True)

        super().__init__(value)


class Nada[T](Maybe[T]):
    """Creates a Maybe[T] with a None value"""

    def __init__(self):
        super().__init__(None)

def maybeify[T, **P](fn: Callable[P, T | None]) -> Callable[P, Maybe[T]]:
    """
    Convert any function that could raise an Exception to a Maybe type,
    with the Exception becoming Nada. Use as a decorator above a function.

    Example
    ==========

    @maybeify

    def raises(_) -> bool: ...


    raises(False).unwrap() == True

    raises(True) == Nada()

    :param fn: function to wrap
    :return: function converting exceptions to Maybe Nada types
    """
    @wraps(fn)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> Maybe[T]:
        try:
            res = fn(*args, **kwargs)

            return Nada() if res is None else Some(res)
        except Exception as e:
            return Nada()

    return wrapper
