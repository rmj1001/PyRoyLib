import unittest

from lib.data_structs.double_linked_list import DoubleLinkedList


class TestDoubleLinkedList(unittest.TestCase):
    def test_init_add(self):
        empty = DoubleLinkedList()
        not_empty = DoubleLinkedList([1, 2, 3, 4, 5, 6])

        self.assertEqual(len(empty), 0)
        self.assertEqual(len(not_empty), 6)

        not_empty.add(7)

        self.assertEqual(len(not_empty), 7)

    def test_str(self):
        empty = DoubleLinkedList()
        not_empty = DoubleLinkedList([1, 2, 3, 4, 5, 6])

        self.assertEqual(str(empty), "DLL()")
        self.assertEqual(str(not_empty), "DLL(1, 2, 3, 4, 5, 6)")

    def test_is_empty(self):
        empty = DoubleLinkedList()
        not_empty = DoubleLinkedList([1, 2, 3, 4, 5, 6])

        self.assertTrue(empty.is_empty())
        self.assertFalse(not_empty.is_empty())

    def test_get(self):
        empty = DoubleLinkedList()
        not_empty = DoubleLinkedList([1, 2, 3, 4, 5, 6])

        with self.assertRaises(Exception):
            empty.get_data(1)

        with self.assertRaises(Exception):
            not_empty.get_data(10)

        self.assertEqual(not_empty.get_data(3), 4)
        self.assertEqual(not_empty.get_data(-1), 6)

        self.assertEqual(not_empty.get_node(-1), not_empty.tail)

    def test_search(self):
        empty = DoubleLinkedList()
        not_empty = DoubleLinkedList([1, 2, 3, 4, 5, 6])

        with self.assertRaises(Exception):
            empty.search(1)

        with self.assertRaises(Exception):
            not_empty.search(10)

        self.assertEqual(not_empty.search(3), 2)
        self.assertEqual(not_empty.search(conditional=lambda x: x == 6), 5)

    def test_remove(self):
        empty = DoubleLinkedList()
        not_empty = DoubleLinkedList([1, 2, 3, 4, 5, 6])

        with self.assertRaises(Exception):
            empty.remove(1)

        with self.assertRaises(Exception):
            not_empty.remove(10)

        not_empty.remove(1)
        self.assertEqual(not_empty.get_data(0), 2)
        self.assertEqual(len(not_empty), 5)

        not_empty.remove(6)
        self.assertEqual(not_empty.get_data(-1), 5)
        self.assertEqual(len(not_empty), 4)

    def test_remove_at(self):
        empty = DoubleLinkedList()
        not_empty = DoubleLinkedList([1, 2, 3, 4, 5, 6])

        with self.assertRaises(Exception):
            empty.remove_at(2)

        with self.assertRaises(Exception):
            not_empty.remove_at(10)

        not_empty.remove_at(2)
        self.assertEqual(not_empty.get_data(2), 4)
        self.assertEqual(len(not_empty), 5)

        not_empty.remove_at(-1)
        self.assertEqual(not_empty.get_data(-1), 5)
        self.assertEqual(len(not_empty), 4)

    def test_backwards_traversal(self):
        not_empty = DoubleLinkedList([1, 2, 3, 4, 5, 6])

        self.assertEqual(not_empty.head.previous, None)
        self.assertEqual(not_empty.head.next.next.next.previous.data, 3)

        not_empty.remove(3)
        self.assertEqual(not_empty.get_data(2), 4)

        not_empty.remove_at(3)
        self.assertEqual(not_empty.get_data(3), 6)

    def test_update(self):
        empty = DoubleLinkedList()
        not_empty = DoubleLinkedList([1, 2, 3, 4, 5, 6])

        with self.assertRaises(Exception):
            empty.update(1, 1)

        not_empty.update(0, 3)
        self.assertEqual(not_empty.get_data(0), 3)

        not_empty.update(5, 1)
        self.assertEqual(not_empty.get_data(5), 1)

    def iter(self):
        empty = DoubleLinkedList()
        not_empty = DoubleLinkedList([1, 2, 3, 4, 5, 6])

        with self.assertRaises(StopIteration):
            next(empty)

        for data in not_empty:
            print(data)


if __name__ == '__main__':
    unittest.main()
