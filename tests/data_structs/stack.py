import unittest
from lib.data_structs.stack import Stack, StackException


class TestStack(unittest.TestCase):
    def test_empty(self):
        empty = Stack()
        full = Stack([1, 2, 3, 4, 5, 6])

        self.assertEqual(empty.is_empty(), True)
        self.assertEqual(full.is_empty(), False)

    def test_push(self):
        empty = Stack()

        empty.push(1)

        self.assertEqual(empty.head.value, 1)

    def test_pop(self):
        empty = Stack()
        full = Stack([1, 2, 3, 4, 5, 6])

        with self.assertRaises(StackException):
            empty.pop()

        self.assertEqual(full.pop(), 6)
        self.assertEqual(full.head.value, 5)

        full.pop()
        full.pop()
        full.pop()
        full.pop()
        full.pop()

        with self.assertRaises(StackException):
            full.pop()

    def test_peek(self):
        empty = Stack()
        full = Stack([1, 2, 3, 4, 5, 6])

        with self.assertRaises(StackException):
            empty.peek()

        self.assertEqual(full.peek(), 6)
        self.assertEqual(full.head.value, 6)

    def test_len(self):
        empty = Stack()
        full = Stack([1, 2, 3, 4, 5, 6])

        self.assertEqual(len(empty), 0)
        self.assertEqual(len(full), 6)

        full.pop()

        self.assertEqual(len(full), 5)

        full.pop()
        full.pop()
        full.pop()
        full.pop()
        full.pop()

        self.assertEqual(len(full), 0)

    def test_str(self):
        empty = Stack()
        full = Stack([1, 2, 3, 4, 5, 6])

        self.assertEqual(str(empty), f"Stack()")
        self.assertEqual(str(full), f"Stack(6, 5, 4, 3, 2, 1)")

        full.pop()

        self.assertEqual(str(full), f"Stack(5, 4, 3, 2, 1)")


if __name__ == "__main__":
    unittest.main()
