import unittest

from lib.linked_list import SingleLinkedList, DoubleLinkedList


class TestSingleLinkedList(unittest.TestCase):

    def test_init_add(self):
        empty = SingleLinkedList()
        two = SingleLinkedList()

        two.add(1)
        two.add(2)

        not_empty = SingleLinkedList([1, 2, 3, 4, 5, 6])

        self.assertEqual(len(empty), 0)
        self.assertEqual(len(two), 2)
        self.assertEqual(len(not_empty), 6)

    def test_str(self):
        empty = SingleLinkedList()
        not_empty = SingleLinkedList([1, 2, 3, 4, 5, 6])

        self.assertEqual(str(empty), "SLL()")
        self.assertEqual(str(not_empty), "SLL(1, 2, 3, 4, 5, 6)")

    def test_is_empty(self):
        empty = SingleLinkedList()
        not_empty: SingleLinkedList[int] = SingleLinkedList([1, 2, 3, 4, 5, 6])

        self.assertTrue(empty.is_empty())
        self.assertFalse(not_empty.is_empty())

    def test_remove(self):
        empty = SingleLinkedList()
        not_empty: SingleLinkedList[int] = SingleLinkedList([1, 2, 3, 4, 5, 6])

        with self.assertRaises(Exception):
            empty.remove(1)

        with self.assertRaises(Exception):
            not_empty.remove(10)

        not_empty.remove(1)
        self.assertEqual(not_empty.get(0), 2)

        not_empty.remove(6)
        self.assertEqual(not_empty.get(-1), 5)

    def test_get(self):
        empty = SingleLinkedList()
        not_empty: SingleLinkedList[int] = SingleLinkedList([1, 2, 3, 4, 5, 6])

        with self.assertRaises(Exception):
            empty.get(1)

        with self.assertRaises(Exception):
            not_empty.get(10)

        six = not_empty.get(5)

        self.assertEqual(six, 6)

    def test_remove_at(self):
        empty = SingleLinkedList()
        not_empty: SingleLinkedList[int] = SingleLinkedList([1, 2, 3, 4, 5, 6])

        with self.assertRaises(Exception):
            empty.remove_at(2)

        with self.assertRaises(Exception):
            not_empty.remove_at(10)

        not_empty.remove_at(0)
        self.assertEqual(not_empty.get(0), 2)
        self.assertEqual(len(not_empty), 5)

        not_empty.remove_at(-1)
        self.assertEqual(not_empty.get(-1), 5)

    def test_search(self):
        empty = SingleLinkedList()
        not_empty: SingleLinkedList[int] = SingleLinkedList([1, 2, 3, 4, 5, 6])

        with self.assertRaises(Exception):
            empty.search(1)

        self.assertEqual(not_empty.search(5), 4)


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
            empty.get(1)

        with self.assertRaises(Exception):
            not_empty.get(10)

        self.assertEqual(not_empty.get(3), 4)

        self.assertEqual(not_empty.get(-1), 6)

    def test_search(self):
        empty = DoubleLinkedList()
        not_empty = DoubleLinkedList([1, 2, 3, 4, 5, 6])

        with self.assertRaises(Exception):
            empty.search(1)

        with self.assertRaises(Exception):
            not_empty.search(10)

        self.assertEqual(not_empty.search(3), 2)

    def test_remove(self):
        empty = DoubleLinkedList()
        not_empty = DoubleLinkedList([1, 2, 3, 4, 5, 6])

        with self.assertRaises(Exception):
            empty.remove(1)

        with self.assertRaises(Exception):
            not_empty.remove(10)

        not_empty.remove(1)
        self.assertEqual(not_empty.get(0), 2)
        self.assertEqual(len(not_empty), 5)

        not_empty.remove(6)
        self.assertEqual(not_empty.get(-1), 5)
        self.assertEqual(len(not_empty), 4)

    def test_remove_at(self):
        empty = DoubleLinkedList()
        not_empty = DoubleLinkedList([1, 2, 3, 4, 5, 6])

        with self.assertRaises(Exception):
            empty.remove_at(2)

        with self.assertRaises(Exception):
            not_empty.remove_at(10)

        not_empty.remove_at(2)
        self.assertEqual(not_empty.get(2), 4)
        self.assertEqual(len(not_empty), 5)

        not_empty.remove_at(-1)
        self.assertEqual(not_empty.get(-1), 5)
        self.assertEqual(len(not_empty), 4)

    def test_backwards_traversal(self):
        not_empty = DoubleLinkedList([1, 2, 3, 4, 5, 6])

        self.assertEqual(not_empty.head.previous, None)
        self.assertEqual(not_empty.head.next.next.next.previous.data, 3)

        not_empty.remove(3)
        self.assertEqual(not_empty.get(2), 4)

        not_empty.remove_at(3)
        self.assertEqual(not_empty.get(3), 6)


if __name__ == '__main__':
    unittest.main()
