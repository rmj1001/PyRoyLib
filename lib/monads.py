from enum import Enum
from typing import TypeVar, Callable

# Generic types
T = TypeVar("T") # Generic type for Option class
V = TypeVar("V") # Generic type for Options passed as parameters
R = TypeVar("R") # Return type when Callable[[T], R]
E = TypeVar("E")  # For errors

# Used for Option functions that pass value to function and return generic result
MapFunc = Callable[[T], R]

# Used for Option functions that pass value to function and return boolean (i.e. for validation)
PredicateFunc = Callable[[T], bool]

class OptionException[E](Exception):
    """Custom exception for Option type"""

    def __init__(self, message: E) -> None:
        self.message = message
        super().__init__(self.message)


class ResultException[E](Exception):
    """Custom exception for Result type"""

    def __init__(self, message: E) -> None:
        self.message = message
        super().__init__(self.message)


class Option[T]:
    """Rust-style option"""
    _value = None

    def __init__(self, value: T | None):
        self._value = value

    def __str__(self) -> str:
        """Return string representation of option"""
        if self.is_some():
            return f"some({self.unwrap()})"

        return "nada"

    def __bool__(self) -> bool:
        """Return true if option is Some, false if Nada"""
        if self.is_some():
            return True
        return False

    def __eq__(self, other: object) -> bool:
        """Return True if Options are identical, else False"""
        if self.is_nada() and other is None:
            return True

        if not isinstance(other, Option):
            return NotImplemented

        if self._value == other._value:
            return True

        return False

    @classmethod
    def some(cls, value: T) -> "Option[T]":
        """Create an option with Some variant"""
        return cls(value)

    @classmethod
    def nada(cls) -> "Option":
        """Create an option with Nada variant"""
        return cls(None)

    def is_some(self) -> bool:
        """Return true if variant is Some"""
        return self._value is not None

    def is_some_and(self, predicate: PredicateFunc) -> bool:
        """Return true if variant is Some and matches predicate"""
        if self.is_nada():
            return False

        return predicate(self._value)

    def is_nada(self) -> bool:
        """Return true if variant is Nada"""
        return self._value is None

    def is_nada_or(self, predicate: PredicateFunc) -> bool:
        """Return true if variant is Nada or matches predicate"""
        if self.is_nada() or predicate(self._value):
            return True

        return False

    def expect(self, error: E) -> T:
        """Get value if Some, else raise custom ValueError"""
        if self.is_nada():
            raise OptionException(error)

        return self._value

    def unwrap(self) -> T:
        """Get the value if Some, else raise ValueError"""
        if self.is_nada():
            raise OptionException("Cannot unwrap Nada")

        return self._value

    def unwrap_or(self, default: T) -> T:
        """Get value if variant is Some, else return default value"""
        if self.is_nada():
            return default

        return self._value

    def unwrap_or_else(self, func: Callable) -> T | Callable:
        """Get value if Some, else get value from passed function"""
        if self.is_some():
            return self._value

        return func()

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
        return self.map(func).flatten()

    def ok_or(self, error: E) -> "Result[T,E]":
        """Return a result"""
        if self.is_nada():
            return Result.err(error)

        return Result.ok(self._value)

    def ok_or_else(self, error: Callable) -> "Result[T,E]":
        """Return a result. If option is Nada, error will be the result of a function."""
        if self.is_nada():
            return Result.err(error())

        return Result.ok(self._value)

    def filter(self, predicate: PredicateFunc) -> "Option[T]":
        """Return Option.some(self._value) if predicate returns True, else return Option.none()"""
        if self.is_nada():
            return self

        if predicate(self._value):
            return Option.some(self._value)

        return Option.nada()

    def other_if_some(self, other_option: Option[V]) -> "Option[T] | Option[V]":
        """Return Nada if option is Nada, otherwise return other_option"""
        if self.is_some():
            return other_option

        return self

    def other_if_nada(self, other_option: Option[V]) -> "Option[T] | Option[V]":
        """Returns the option if it is Some, otherwise returns other_option"""
        if self.is_nada():
            return other_option

        return self

    def or_else(self, func: MapFunc) -> "Option[MapFunc]":
        """Returns option if it is Some, else calls func and returns result"""
        if self.is_some():
            return self

        result = func(self._value)

        if result is None:
            return Option.nada()

        return Option.some(result)

    def take(self) -> T:
        """Return the value in the Option and set it to Nada"""
        value = self._value

        self._value = None

        return value

    def replace(self, value: T) -> None:
        """Replace the current value with another value"""
        self._value = value

    def zip(self, other_option: Option[V]) -> Option[tuple[T,V]]:
        """Return tuple if both options are Some, else return Nada"""
        if self.is_some() and other_option.is_some():
            return Option.some((self._value, other_option._value))

        return Option.nada()

    def unzip(self) -> tuple[Option[T], Option[V]]:
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


def some(value: T) -> Option[T]:
    """Shorthand for Option.some(value)"""
    return Option.some(value)


def nada() -> Option:
    """Shorthand for Option.nada()"""
    return Option.nada()


class ResultVariant(Enum):
    """State variants for Result monad"""
    OK = 0
    ERR = 1


class Result[T, E]:
    """Rust-style result"""

    _value = None
    _state: ResultVariant = ResultVariant.ERR

    def __init__(self, value: T, state: ResultVariant = ResultVariant.OK):
        if value is None:
            raise ResultException("Value cannot be None. Try using Option?")

        self._value = value
        self._state = state

    def __str__(self):
        """String representation for Result[T,E]"""
        if self.is_ok():
            return f"ok({self._value})"
        else:
            return f"err({self._value})"

    def __bool__(self) -> bool:
        """Return True if Result[T,E] is Ok, else return False"""
        return self.is_ok()

    def __eq__(self, other: object) -> bool:
        """Compare Result objects for equality"""
        if not isinstance(other, Result):
            return NotImplemented

        if self._value != other._value:
            return False

        if self._state != other._state:
            return False

        return True

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
        return self._state == ResultVariant.OK

    def is_ok_and(self, predicate: Callable[[R], bool]) -> bool:
        """Return True if variant is OK and predicate returns True"""
        return self.is_ok() and predicate(self._value)

    def is_err(self) -> bool:
        """Return True if variant is ERR"""
        return self._state == ResultVariant.ERR

    def is_err_and(self, predicate: Callable[[R], bool]) -> bool:
        """Return True if variant is ERR and predicate returns True"""
        return self.is_err() and predicate(self._value)

    def map(self, func: Callable[[R], R]) -> "Result[T,E]":
        """Create a new result with value mapped to func"""
        if self.is_err():
            return self

        return ok(func(self._value))

    def map_or(self, func: Callable[[R], R], default: R) -> "Result[T,E]":
        """Returns the provided default if Err or applies func to value"""
        if self.is_err():
            return default

        return ok(func(self._value))

    def map_or_else(self, success: Callable[[R], R], default: Callable[[E], E]) -> "Result[T,E]":
        """Returns the function on Err if Err or function on Ok"""
        if self.is_err():
            return err(default(self._value))

        return ok(success(self._value))

    def map_err(self, func: Callable[[E], E]) -> "Result[T,E]":
        """Maps an Err value, leaving Ok untouched"""
        if self.is_ok():
            return self

        return err(func(self._value))

    def expect(self, message: E) -> T:
        """Returns Ok value or throws exception with custom error message"""
        if self.is_err():
            raise ResultException(message)

        return self._value

    def unwrap(self) -> T:
        """Returns Ok value or throws exception with Err value"""
        if self.is_err():
            raise ResultException(self._value)

        return self._value

    def expect_err(self, message: T) -> E:
        """Returns contained Err, or else raises exception if Ok"""
        if self.is_err():
            return self._value

        raise ResultException(message)

    def unwrap_err(self) -> E:
        """Returns contained Err, or else raises exception with Ok value"""
        if self.is_err():
            return self._value

        raise ResultException(self._value)

    def into_ok(self) -> T:
        """Returns the contained Ok, never raises exception"""
        return self._value

    def into_err(self) -> E:
        """Returns the contained Err, never raises exception"""
        return self._value

    def both(self, res: Result[R, E]) -> Result[R, E]:
        """Result res if result is Ok, otherwise return Err of self"""
        if self.is_ok():
            return res

        return self

    def and_then(self, func: Callable[[R], R]) -> "Result[R, E]":
        """Calls func if result is Ok, otherwise returns Err of self"""
        if self.is_err():
            return self

        return ok(func(self._value))

    def either(self, res: Result[R, E]) -> Result[R, E]:
        """Returns res if result is Err, otherwise returns Ok value of self"""
        if self.is_ok():
            return self

        return res

    def or_else(self, func: Callable[[E], E]) -> Result[R, E]:
        """Calls func if result is Err, otherwise returns Ok of self"""
        if self.is_ok():
            return self

        return err(func(self._value))

    def unwrap_or(self, default: T) -> T:
        """Returns contained Ok value or default if Err"""
        if self.is_err():
            return default

        return self._value

    def unwrap_or_else(self, func: Callable[[], R]) -> R:
        """Returns contained Ok value or value from func if Err"""
        if self.is_ok():
            return self._value

        return func()


def ok(value: T) -> Result[T, E]:
    """Shorthand for Result.ok(), useful for pattern matching"""
    return Result.ok(value)


def err(value: E) -> Result[T, E]:
    """Shorthand for Result.err(), useful for pattern matching"""
    return Result.err(value)
