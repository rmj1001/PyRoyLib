from collections.abc import Iterable, Sized


class BoxException(Exception):
    def __init__(self, message) -> None:
        super().__init__(message)


class Box[T]:
    def __init__(self, value: T):
        self.value: T = value

    def __str__(self) -> str:
        return f'Box({self.value})'

    def __add__(self, other: T) -> "Box[T]":
        if not isinstance(other, Box):
            return NotImplemented

        return Box(self.value + other.value)

    def __sub__(self, other: T) -> "Box[T]":
        if not isinstance(other, Box):
            return NotImplemented

        return Box(self.value - other.value)

    def __mul__(self, other) -> 'Box[T]':
        if not isinstance(other, Box):
            return NotImplemented

        return Box(self.value * other.value)

    def __truediv__(self, other) -> 'Box[T]':
        if not isinstance(other, Box):
            return NotImplemented

        return Box(self.value / other.value)

    def __floordiv__(self, other) -> 'Box[T]':
        if not isinstance(other, Box):
            return NotImplemented

        return Box(self.value // other.value)

    def __mod__(self, other) -> 'Box[T]':
        if not isinstance(other, Box):
            return NotImplemented

        return Box(self.value % other.value)

    def __bool__(self) -> bool:
        return bool(self.value)

    def __ge__(self, other) -> bool:
        if not isinstance(other, Box):
            return NotImplemented

        return self.value >= other.value

    def __gt__(self, other) -> bool:
        if not isinstance(other, Box):
            return NotImplemented

        return self.value > other.value

    def __le__(self, other) -> bool:
        if not isinstance(other, Box):
            return NotImplemented

        return self.value <= other.value

    def __lt__(self, other) -> bool:
        if not isinstance(other, Box):
            return NotImplemented

        return self.value < other.value

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Box):
            return NotImplemented

        return self.value == other.value

    def __ne__(self, value: object, /) -> bool:
        return not self == value

    def __and__(self, other) -> bool:
        if not isinstance(other, Box):
            return NotImplemented

        return self.value and other.value

    def __or__(self, other) -> bool:
        if not isinstance(other, Box):
            return NotImplemented

        return self.value or other.value

    def __xor__(self, other) -> bool:
        if not isinstance(other, Box):
            return NotImplemented

        return self.value ^ other.value

    def __iter__(self) -> Iterable[T]:
        if not isinstance(self.value, Iterable):
            raise BoxException('Contained value is not iterable')

        return iter(self.value)

    def __len__(self):
        if isinstance(self.value, Sized):
            return len(self.value)
        elif self.value is not None:
            return 1
        else:
            return 0

    def __contains__(self, item) -> bool:
        if isinstance(self.value, Iterable):
            return item in self.value
        else:
            return self.value == item

    def take(self) -> T:
        """
        Remove contained item and return it
        :return: Contained item
        """
        if self.value is None:
            raise BoxException(f'Box contents are None')

        tmp = self.value
        self.value = None
        return tmp

    def replace(self, new_value: T) -> "Box[T]":
        """
        Replace the contained item and return self
        :param new_value: The new contained item
        :return: self
        """
        if self.value is None:
            raise BoxException(f'Box contents are None')

        self.value = new_value
        return self

    def peek(self) -> T:
        """
        Return the contained item without removing it
        :return: Contained item
        """
        if self.value is None:
            raise BoxException(f'Box contents are None')

        return self.value
