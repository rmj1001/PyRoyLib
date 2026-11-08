from collections.abc import Callable
from monads.exceptions.option_exception import OptionException
from monads.result import Result
from types.map_function import MapFunc
from types.predicate import Predicate


class Option[T]:
    """Rust-style option"""

    def __init__(self, value: T | None):
        self._value: T | None  = value

    def __str__(self) -> str:
        """Return string representation of option"""
        if self.is_some():
            return f"some({self.unwrap()})"

        return "nada"

    def __bool__(self) -> bool:
        """Return true if option is Some, false if Nada"""
        return self.is_some()

    def __eq__(self, other: object) -> bool:
        """Return True if Options are identical, else False"""
        if self.is_nada() and other is None:
            return True

        if not isinstance(other, Option):
            return NotImplemented

        return self._value == other._value

    @classmethod
    def some(cls, value: T, *args, **kwargs) -> "Option[T]":
        """Create an option with Some variant"""
        if isinstance(value, Callable):
            return cls(value(*args, **kwargs))

        return cls(value)

    @classmethod
    def nada(cls) -> "Option":
        """Create an option with Nada variant"""
        return cls(None)

    def is_some(self) -> bool:
        """Return true if variant is Some"""
        return self._value is not None

    def is_some_and(self, predicate: Predicate) -> bool:
        """Return true if variant is Some and matches predicate"""
        if self.is_nada():
            return False

        return predicate(self._value)

    def is_nada(self) -> bool:
        """Return true if variant is Nada"""
        return self._value is None

    def is_nada_or(self, predicate: Predicate) -> bool:
        """Return true if variant is Nada or matches predicate"""
        return self.is_nada() or predicate(self._value)

    def expect[E](self, error: E) -> T:
        """Get value if Some, else raise custom ValueError"""
        if self._value is None:
            raise OptionException(error)

        return self._value

    def unwrap(self) -> T:
        """Get the value if Some, else raise ValueError"""
        if self._value is None:
            raise OptionException("Cannot unwrap Nada")

        return self._value

    def unwrap_or(self, default: T) -> T:
        """Get value if variant is Some, else return default value"""
        if self._value is None:
            return default

        return self._value

    def unwrap_or_else(self, func: Callable, *args, **kwargs) -> T | Callable:
        """Get value if Some, else get value from passed function"""
        if self._value is not None:
            return self._value

        return func(*args, **kwargs)

    def map(self, func: MapFunc) -> "Option[MapFunc]":
        """Call a function on the option and return a new option"""
        if self._value is None:
            return Option.nada()

        return Option.some(func(self._value))

    def flatten(self) -> "Option[T]":
        """Recursively flatten nested options"""
        if isinstance(self._value, Option):
            return self._value.flatten()
        else:
            return self

    def flatmap(self, func: MapFunc) -> "Option[MapFunc]":
        """Call a function on the option and return a flattened option"""
        return self.flatten().map(func).flatten()

    def ok_or[E](self, error: E) -> "Result[T,E]":
        """Return a result"""
        if self.is_nada():
            return Result.err(error)

        return Result.ok(self._value)

    def ok_or_else[E](self, func: Callable, *args, **kwargs) -> "Result[T,E]":
        """Return a result. If option is Nada, error will be the result of a function."""
        if self.is_nada():
            return Result.err(func(*args, **kwargs))

        return Result.ok(self._value)

    def filter(self, predicate: Predicate) -> "Option[T]":
        """Return Option.some(self._value) if predicate returns True, else return Option.none()"""
        if self.is_nada():
            return self

        if predicate(self._value):
            return Option.some(self._value)

        return Option.nada()

    def other_if_some[V](self, other_option: "Option[V]") -> "Option[T] | Option[V]":
        """Return Nada if option is Nada, otherwise return other_option"""
        if self.is_some():
            return other_option

        return self

    def other_if_nada[V](self, other_option: "Option[V]") -> "Option[T] | Option[V]":
        """Returns the option if it is Some, otherwise returns other_option"""
        if self.is_nada():
            return other_option

        return self

    def or_else(self, func: Callable, *args, **kwargs) -> "Option[T] | Option[MapFunc]":
        """Returns option if it is Some, else calls func and returns result"""
        if self.is_some():
            return self

        result = func(*args, **kwargs)

        if result is None:
            return Option.nada()

        return Option.some(result)

    def take(self) -> T:
        """Return the value in the Option and set it to Nada"""
        value = self.unwrap()
        self._value = None

        return value

    def replace(self, value: T) -> None:
        """Replace the current value with another value"""
        self._value = value

    def zip[V](self, other_option: "Option[V]") -> "Option[tuple[T, V]]":
        """Return tuple if both options are Some, else return Nada"""
        if self.is_some() and other_option.is_some():
            return Option.some((self._value, other_option._value))

        return Option.nada()

    def unzip[V](self) -> "tuple[Option[T], Option[V]]":
        """Unzips an option containing a tuple of values. Returns (Nada, Nada) if tuple not present."""
        if not isinstance(self._value, tuple):
            return Option.nada(), Option.nada()

        first = self._value[0]
        second = self._value[1]
        first_opt = Option.nada()
        second_opt = Option.nada()

        if first is not None:
            first_opt = Option.some(first)

        if second is not None:
            second_opt = Option.some(second)

        return first_opt, second_opt


def some[T](value: T, *args, **kwargs) -> Option[T]:
    """Shorthand for Option.some(value)"""
    if isinstance(value, Callable):
        return Option.some(value, *args, **kwargs)

    return Option.some(value)


def nada() -> Option:
    """Shorthand for Option.nada()"""
    return Option.nada()
