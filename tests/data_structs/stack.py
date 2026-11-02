import unittest

from lib.data_structs.stack import Stack, StackException


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
