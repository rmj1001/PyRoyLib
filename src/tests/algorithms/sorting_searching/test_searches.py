import unittest
from algorithms.searching.binary_search import binary_search, recursive_binary_search
from algorithms.searching.sequential_search import sequential_search, sorted_sequential_search, SequentialSearchError

class TestSearches(unittest.TestCase):
    def test_sequential_search(self):
        empty = []
        full = list(range(10))

        search_empty = sequential_search(empty, 0)
        search_full = sequential_search(full, 0)

        self.assertEqual(search_empty, None)
        self.assertEqual(search_full, 0)

        with self.assertRaises(SequentialSearchError):
            sequential_search(empty)

    def test_sorted_sequential_search(self):
        empty = []
        full = list(range(10))

        search_empty = sorted_sequential_search(empty, 0)
        search_full = sorted_sequential_search(full, 0)

        self.assertEqual(search_empty, None)
        self.assertEqual(search_full, 0)

    def test_binary_search(self):
        empty = []
        full = list(range(10))

        search_empty = binary_search(empty, 0)
        search_full = binary_search(full, 0)

        self.assertEqual(search_empty, None)
        self.assertEqual(search_full, 0)

    def test_recursive_binary_search(self):
        empty = []
        full = list(range(10))

        search_empty = recursive_binary_search(empty, 0)
        search_full = recursive_binary_search(full, 0)

        self.assertEqual(search_empty, None)
        self.assertEqual(search_full, 0)


if __name__ == '__main__':
    unittest.main()
