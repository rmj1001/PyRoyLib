from collections.abc import Callable, Iterable

type MapFn[T] = Callable[[T], T]

class FunctorException[T](Exception):
    def __init__(self, message: T):
        super().__init__(message)

class Functor[T]:
    def __init__(self, value: T):
        self.value = value

    def __eq__(self, other: object) -> bool:
        if self.value is None and other is None:
            return True

        if not isinstance(other, Functor):
            return NotImplemented

        return self.value == other.value

    def map(self, fn: MapFn) -> 'Functor[T]':
        """
        Call a function that takes one argument, T, and change internal value to its result of type T.
        :param fn: Function to apply to T
        :return: Self with value changed to fn(self.value)
        """
        if self.value is None:
            return self

        try:
            self.value = fn(self.value)
        except Exception as e:
            raise FunctorException(e)

        return self

    def flatten(self) -> 'Functor[T]':
        """
        If self.value is of type Functor[T], flatten until self.value is of type T.
        :return: Self with flattened value
        """
        while isinstance(self.value, Functor):
            self.value = self.value.value

        return self

    def flatmap(self, fn: MapFn) -> 'Functor[T]':
        """
        Call a function that takes one argument, T, and change internal value to its result of type T.
        If self.value is a Functor, then flatten until self.value is of type T.
        :param fn: Function to apply to T
        :return: Self with flattened value changed to fn(self.value)
        """
        return self.flatten().map(fn)

    def take(self) -> T:
        """
        Return the contained value, replacing it with None inside the functor.
        Raises FunctorException if self.value is None
        :return: contained value
        """
        if self.value is None:
            raise FunctorException(f'Value cannot be taken, it is None.')

        tmp: T = self.value
        self.value = None
        return tmp

    def replace(self, value: T) -> 'Functor[T]':
        """
        Replace contained value with a new value
        :param value: The new value for Functor to contain
        :return: self
        """
        self.value = value
        return self
