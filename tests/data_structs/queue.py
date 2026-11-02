import unittest

from lib.data_structs.queue import Queue, QueueException


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

        with self.assertRaises(QueueException):
            empty_queue.dequeue()

        self.assertEqual(full_queue.dequeue(), 1)
        self.assertEqual(full_queue.data[0], 2)

    def test_front(self):
        empty_queue = Queue()
        full_queue = Queue([1, 2, 3, 4, 5, 6])

        with self.assertRaises(QueueException):
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

    def test_iter(self):
        empty = Queue()
        full = Queue([1, 2, 3, 4, 5, 6])

        iter_empty = iter(empty)
        iter_full = iter(full)

        with self.assertRaises(StopIteration):
            next(iter_empty)

        self.assertEqual(next(iter_full), 1)
        self.assertEqual(next(iter_full), 2)
        self.assertEqual(next(iter_full), 3)
        self.assertEqual(next(iter_full), 4)
        self.assertEqual(next(iter_full), 5)
        self.assertEqual(next(iter_full), 6)

        with self.assertRaises(StopIteration):
            next(iter_full)


if __name__ == '__main__':
    unittest.main()
