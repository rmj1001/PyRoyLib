import unittest

from lib.data_structs.single_linked_list import SingleLinkedList


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
        self.assertEqual(not_empty.get_data(0), 2)

        not_empty.remove(6)
        self.assertEqual(not_empty.get_data(-1), 5)
        self.assertEqual(not_empty.tail.data, 5)

    def test_get(self):
        empty = SingleLinkedList()
        not_empty: SingleLinkedList[int] = SingleLinkedList([1, 2, 3, 4, 5, 6])

        with self.assertRaises(Exception):
            empty.get_data(1)

        with self.assertRaises(Exception):
            not_empty.get_data(10)

        six = not_empty.get_data(5)

        self.assertEqual(six, 6)
        self.assertEqual(not_empty.get_node(-1), not_empty.tail)

    def test_remove_at(self):
        empty = SingleLinkedList()
        not_empty: SingleLinkedList[int] = SingleLinkedList([1, 2, 3, 4, 5, 6])

        with self.assertRaises(Exception):
            empty.remove_at(2)

        with self.assertRaises(Exception):
            not_empty.remove_at(10)

        not_empty.remove_at(0)
        self.assertEqual(not_empty.get_data(0), 2)
        self.assertEqual(len(not_empty), 5)

        not_empty.remove_at(-1)
        self.assertEqual(not_empty.get_data(-1), 5)
        self.assertEqual(not_empty.tail, not_empty.get_node(-1))

    def test_search(self):
        empty = SingleLinkedList()
        not_empty: SingleLinkedList[int] = SingleLinkedList([1, 2, 3, 4, 5, 6])

        with self.assertRaises(Exception):
            empty.search(1)
            empty.search(conditional=lambda x: x == 5)

        def is_five(num: int) -> bool:
            return num == 5

        self.assertEqual(not_empty.search(5), 4)
        self.assertEqual(not_empty.search(conditional=is_five), 4)

    def test_update(self):
        empty = SingleLinkedList()
        not_empty: SingleLinkedList[int] = SingleLinkedList([1, 2, 3, 4, 5, 6])

        with self.assertRaises(Exception):
            empty.update(1, 1)

        not_empty.update(0, 3)
        self.assertEqual(not_empty.get_data(0), 3)

        not_empty.update(5, 1)
        self.assertEqual(not_empty.get_data(5), 1)


if __name__ == '__main__':
    unittest.main()
