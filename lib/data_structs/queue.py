import unittest
from typing import TypeVar, List, Iterable

T = TypeVar('T')


class Queue[T]:
    data: List[T]
    elements: int

    def __init__(self, starting_data: Iterable[T] | None = None) -> None:
        """Initialize a queue, with or without starting data"""
        self.data = []
        self.elements = 0

        if starting_data is not None:
            for item in starting_data:
                self.data.append(item)
                self.elements += 1

    def __len__(self) -> int:
        """Return the number of elements in the queue"""
        return self.elements

    def __str__(self) -> str:
        """String representation of the queue"""
        str_data = [str(item) for item in self.data]
        return f"Queue({', '.join(str_data)})" if len(self) > 0 else "Queue()"

    def is_empty(self) -> bool:
        """Check if the queue is empty."""
        return self.elements == 0

    def enqueue(self, data: T) -> None:
        """Add data to the queue."""
        self.data.insert(0, data)
        self.elements += 1

    def dequeue(self) -> T:
        """Remove data from the queue."""
        if self.is_empty():
            raise Exception('Queue is empty')

        data = self.data.pop(0)
        self.elements -= 1
        return data

    def front(self) -> T:
        """Get the last data from the queue."""
        if self.is_empty():
            raise Exception('Queue is empty')

        return self.data[0]


class TestQueue(unittest.TestCase):
    def test_empty(self):
        empty_queue = Queue()
        full_queue = Queue([1, 2, 3, 4, 5, 6])

        self.assertEqual(empty_queue.is_empty(), True)
        self.assertEqual(full_queue.is_empty(), False)

    def test_enqueue(self):
        empty_queue = Queue()

        empty_queue.enqueue(1)
        empty_queue.enqueue(2)
        empty_queue.enqueue(3)

        self.assertEqual(empty_queue.data[0], 3)

    def test_dequeue(self):
        empty_queue = Queue()
        full_queue = Queue([1, 2, 3, 4, 5, 6])

        with self.assertRaises(Exception):
            empty_queue.dequeue()

        self.assertEqual(full_queue.dequeue(), 1)
        self.assertEqual(full_queue.data[0], 2)

    def test_front(self):
        empty_queue = Queue()
        full_queue = Queue([1, 2, 3, 4, 5, 6])

        with self.assertRaises(Exception):
            empty_queue.front()

        self.assertEqual(full_queue.front(), 1)
        self.assertEqual(full_queue.data[0], 1)

    def test_len(self):
        empty_queue = Queue()
        full_queue = Queue([1, 2, 3, 4, 5, 6])

        self.assertEqual(len(empty_queue), 0)
        self.assertEqual(len(full_queue), 6)

    def test_str(self):
        empty_queue = Queue()
        full_queue = Queue([1, 2, 3, 4, 5, 6])

        self.assertEqual(str(empty_queue), f"Queue()")
        self.assertEqual(str(full_queue), f"Queue(1, 2, 3, 4, 5, 6)")

if __name__ == '__main__':
    unittest.main()
