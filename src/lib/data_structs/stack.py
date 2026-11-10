from typing import Iterable

from .exceptions.stack_exception import StackException
from .nodes.single_linked_node import SingleLinkedNode


class Stack[T]:
    """Last-in first-out (LIFO) dynamic-size data structure, implemented as a single-linked list"""
    head: SingleLinkedNode[T] | None
    _count: int

    def __init__(self, initial_data: Iterable[T] | None = None) -> None:
        self.head = None
        self._count = 0

        if initial_data is not None:
            for item in initial_data:
                self.push(item)

    def __len__(self) -> int:
        """Return the number of items in the stack"""
        return self._count

    def __str__(self) -> str:
        """Return a string representation of the stack"""
        string: str = 'Stack('
        values: list[T] = []

        current = self.head
        while current is not None:
            values.append(current.data)
            current = current.next

        string += ', '.join([str(item) for item in values])
        string += ')'

        return string

    def is_empty(self) -> bool:
        """Check to see if stack contains no nodes"""
        return self.head is None

    def push(self, item: T) -> None:
        """Add item to the top of the stack"""
        if self.head is None:
            self.head = SingleLinkedNode(item)
        else:
            temp = self.head
            self.head = SingleLinkedNode(item, temp)

        self._count += 1

    def pop(self) -> T:
        """Retrieve the value from the top of the stack and remove it"""
        if self.head is None:
            raise StackException("Stack is empty")

        data = self.head.data
        self.head = self.head.next
        self._count -= 1

        return data

    def peek(self) -> T:
        """Retrieve the value from the top of the stack without removing it"""
        if self.head is None:
            raise StackException("Stack is empty")
        else:
            return self.head.data
