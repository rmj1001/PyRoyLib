class BoxException(Exception):
    def __init__(self, message) -> None:
        super().__init__(message)


class Box[T]:
    def __init__(self, value: T):
        self.value: T = value

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
