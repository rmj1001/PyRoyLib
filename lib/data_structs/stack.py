import unittest
from typing import TypeVar, List, Iterable

T = TypeVar('T')

class StackException(Exception):
    def __init__(self, message) -> None:
        self.message = message
        super().__init__(message)

class Stack[T]:
    data: List[T]
    elements: int

    def __init__(self, starting_data: Iterable[T] | None = None) -> None:
        """Initialize a stack, with or without starting data"""
        self.data = []
        self.elements = 0

        if starting_data is not None:
            for item in starting_data:
                self.data.append(item)
                self.elements += 1

    def __len__(self) -> int:
        """Return the number of elements in the stack"""
        return self.elements

    def __str__(self) -> str:
        """String representation of the stack"""
        str_data = [str(item) for item in self.data]
        return f"Stack({', '.join(str_data)})" if len(self) > 0 else "Stack()"

    def is_empty(self) -> bool:
        """Check if the stack is empty."""
        return self.elements == 0

    def push(self, data: T) -> None:
        """Add data to the stack."""
        self.data.append(data)
        self.elements += 1

    def pop(self) -> T:
        """Remove data from the stack."""
        if self.is_empty():
            raise StackException('Stack is empty')

        data = self.data.pop()
        self.elements -= 1
        return data

    def peek(self) -> T:
        """Get the last data from the stack."""
        if self.is_empty():
            raise StackException('Stack is empty')

        return self.data[-1]


class TestStack(unittest.TestCase):
    def test_empty(self):
        empty_stack = Stack()
        full_stack = Stack([1, 2, 3, 4, 5, 6])

        self.assertEqual(empty_stack.is_empty(), True)
        self.assertEqual(full_stack.is_empty(), False)

    def test_push(self):
        empty_stack = Stack()

        empty_stack.push(1)

        self.assertEqual(empty_stack.data[0], 1)

    def test_pop(self):
        empty_stack = Stack()
        full_stack = Stack([1, 2, 3, 4, 5, 6])

        with self.assertRaises(StackException):
            empty_stack.pop()

        self.assertEqual(full_stack.pop(), 6)
        self.assertEqual(full_stack.data[-1], 5)

    def test_peek(self):
        empty_stack = Stack()
        full_stack = Stack([1, 2, 3, 4, 5, 6])

        with self.assertRaises(StackException):
            empty_stack.peek()

        self.assertEqual(full_stack.peek(), 6)
        self.assertEqual(full_stack.data[-1], 6)

    def test_len(self):
        empty_stack = Stack()
        full_stack = Stack([1, 2, 3, 4, 5, 6])

        self.assertEqual(len(empty_stack), 0)
        self.assertEqual(len(full_stack), 6)

    def test_str(self):
        empty_stack = Stack()
        full_stack = Stack([1, 2, 3, 4, 5, 6])

        self.assertEqual(str(empty_stack), f"Stack()")
        self.assertEqual(str(full_stack), f"Stack(1, 2, 3, 4, 5, 6)")

if __name__ == '__main__':
    unittest.main()
