import unittest

from lib.sorting.swap import swap


class TestSwap(unittest.TestCase):
    def test_swap(self):
        array = [1, 2, 3]
        swapped = [2, 1, 3]

        swap(array, 0, 1)

        self.assertEqual(array, swapped)


if __name__ == '__main__':
    unittest.main()
