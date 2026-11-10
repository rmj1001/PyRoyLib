from src.lib.custom_types.map_function import MapFn


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

        self.value = fn(self.value)
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
