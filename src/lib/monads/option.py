from collections.abc import Callable

from abstract.iequality import IEquality
from abstract.ifunctor import IFunctor
from abstract.irepr import IRepr
from .imonad import IMonad
from monads.exceptions.option_exception import OptionException
from monads.result import Result

# Map function type alias
type MapFn[T] = Callable[[T], T]
type Predicate[T] = Callable[[T], bool]


class Option[T](IRepr, IFunctor[T], IMonad[T], IEquality):
    """Rust-style option"""

    def __init__(self, value: T | None):
        super().__init__(value)

    def __bool__(self) -> bool:
        """Return true if option is Some, false if Nada"""
        return self.is_some()

    # -- IRepr Implementation

    def __repr__(self) -> str:
        """Return string representation of option"""
        if self.is_some():
            return f"some({self.value})"

        return "nada"

    # -- IEquality Implementation

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Option):
            return NotImplemented

        return self.value == other.value

    def __ne__(self, other: object) -> bool:
        if not isinstance(other, Option):
            return NotImplemented

        return self.value != other.value

    # --- IMonad Implementation

    def expect[E](self, message: E) -> T:
        """Get value if Some, else raise custom ValueError"""
        if self.value is None:
            raise OptionException(message)

        return self.value

    def unwrap(self) -> T:
        """Get the value if Some, else raise ValueError"""
        if self.value is None:
            raise OptionException("Cannot unwrap Nada")

        return self.value

    def unwrap_or(self, default: T) -> T:
        """Get value if variant is Some, else return default value"""
        if self.value is None:
            return default

        return self.value

    def unwrap_or_else(self, fn: Callable, *args, **kwargs) -> T | Callable:
        """Get value if Some, else get value from passed function"""
        if self.value is not None:
            return self.value

        return fn(*args, **kwargs)

    def or_else(self, fn: Callable, *args, **kwargs) -> "Option[T] | Option[MapFn]":
        """Returns option if it is Some, else calls fn and returns result"""
        if self.is_some():
            return self

        result = fn(*args, **kwargs)

        if result is None:
            return Option.nada()

        return Option.some(result)

    # -- IFunctor Implementation

    def flatten(self) -> 'Option[T]':
        while isinstance(self.value, Option):
            self.value = self.value.value

        return self

    def map(self, fn: MapFn) -> 'Option[T]':
        if self.is_nada():
            return self

        self.value = fn(self.value)
        return self

    def flatmap(self, fn: MapFn) -> 'Option[T]':
        return self.flatten().map(fn)

    # --- END Interface Implementations

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
        return self.value is not None

    def is_some_and(self, predicate: Predicate) -> bool:
        """Return true if variant is Some and matches predicate"""
        if self.is_nada():
            return False

        return predicate(self.value)

    def is_nada(self) -> bool:
        """Return true if variant is Nada"""
        return self.value is None

    def is_nada_or(self, predicate: Predicate) -> bool:
        """Return true if variant is Nada or matches predicate"""
        return self.is_nada() or predicate(self.value)

    def ok_or[E](self, error: E) -> "Result[T,E]":
        """Return a result"""
        if self.is_nada():
            return Result.err(error)

        return Result.ok(self.value)

    def ok_or_else[E](self, fn: Callable, *args, **kwargs) -> "Result[T,E]":
        """Return a result. If option is Nada, error will be the result of a function."""
        if self.is_nada():
            return Result.err(fn(*args, **kwargs))

        return Result.ok(self.value)

    def filter(self, predicate: Predicate) -> "Option[T]":
        """Return Option.some(self.value) if predicate returns True, else return Option.none()"""
        if self.is_nada():
            return self

        if predicate(self.value):
            return Option.some(self.value)

        return Option.nada()

    def other_if_some(self, other_option: "Option[T]") -> "Option[T]":
        """Return Nada if option is Nada, otherwise return other_option"""
        if self.is_some():
            return other_option

        return self

    def other_if_nada(self, other_option: "Option[T]") -> "Option[T]":
        """Returns the option if it is Some, otherwise returns other_option"""
        if self.is_nada():
            return other_option

        return self

    def zip(self, other_option: "Option[T]") -> "Option[tuple[T, T]]":
        """Return tuple if both options are Some, else return Nada"""
        if self.is_some() and other_option.is_some():
            return Option.some((self.value, other_option.value))

        return Option.nada()

    def unzip(self) -> "tuple[Option[T], Option[T]]":
        """Unzips an option containing a tuple of values. Returns (Nada, Nada) if tuple not present."""
        if not isinstance(self.value, tuple):
            return Option.nada(), Option.nada()

        first = self.value[0]
        second = self.value[1]
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
