from typing import Iterable

class StackException(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)

class StackNode[T]:
    value: T
    next: StackNode[T] | None

    def __init__(self, value: T, next_node: StackNode[T] | None = None) -> None:
        self.value = value
        self.next = next_node


class Stack[T]:
    head: StackNode[T] | None
    _count: int
    _current: StackNode[T] | None

    def __init__(self, initial_data: Iterable[T] | None = None) -> None:
        self.head = None
        self._count = 0
        self._current = None

        if initial_data is not None:
            for item in initial_data:
                self.push(item)

            self._current = self.head

    def __len__(self) -> int:
        """Return the number of items in the stack"""
        return self._count

    def __str__(self) -> str:
        """Return a string representation of the stack"""
        string: str = 'Stack('
        values: list[T] = []

        self._current = self.head
        while self._current is not None:
            values.append(self._current.value)
            self._current = self._current.next

        string += ', '.join([str(item) for item in values])
        string += ')'

        return string

    def is_empty(self) -> bool:
        """Check to see if stack contains no nodes"""
        return self.head is None

    def push(self, item: T) -> None:
        """Add item to the top of the stack"""
        if self.head is None:
            self.head = StackNode(item)
            self._current = self.head
        else:
            temp = self.head
            self.head = StackNode(item, temp)
            self._current = self.head

        self._count += 1

    def pop(self) -> T:
        """Retrieve the value from the top of the stack and remove it"""
        if self.head is None:
            raise StackException("Stack is empty")

        data = self.head.value
        self.head = self.head.next
        self._count -= 1

        return data

    def peek(self) -> T:
        """Retrieve the value from the top of the stack without removing it"""
        if self.head is None:
            raise StackException("Stack is empty")
        else:
            return self.head.value
