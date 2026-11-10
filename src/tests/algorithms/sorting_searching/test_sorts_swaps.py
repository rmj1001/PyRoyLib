import unittest
from random import randint

from algorithms.sorting.swap import swap
from algorithms.sorting import bubble_sort
from algorithms.sorting.insertion_sort import insertion_sort
from algorithms.sorting.merge_sort import merge_sort
from algorithms.sorting.quick_sort import quick_sort
from algorithms.sorting.selection_sort import selection_sort

def unsorted_arr() -> list[int]:
    return [randint(0, 100) for _ in range(10)]

def sorted_arr(arr: list[int]) -> list[int]:
    new = arr.copy()
    new.sort()
    return new

class TestSortingAlgorithms(unittest.TestCase):
    def test_swap(self):
        array = [1, 2, 3]
        swapped = [2, 1, 3]

        swap(array, 0, 1)

        self.assertEqual(array, swapped)

    def test_bubble_sort(self):
        unsorted = unsorted_arr()
        test_case = sorted_arr(unsorted)

        bubble_sort(unsorted)
        self.assertEqual(unsorted, test_case)

    def test_insertion_sort(self):
        unsorted = unsorted_arr()
        test_case = sorted_arr(unsorted)

        insertion_sort(unsorted)
        self.assertEqual(unsorted, test_case)

    def test_merge_sort(self):
        unsorted = unsorted_arr()
        test_case = sorted_arr(unsorted)

        unsorted = merge_sort(unsorted)
        self.assertEqual(unsorted, test_case)

    def test_quick_sort(self):
        unsorted = unsorted_arr()
        test_case = sorted_arr(unsorted)

        quick_sort(unsorted)
        self.assertEqual(unsorted, test_case)

    def test_selection_sort(self):
        unsorted = unsorted_arr()
        test_case = sorted_arr(unsorted)

        selection_sort(unsorted)
        self.assertEqual(unsorted, test_case)

if __name__ == '__main__':
    unittest.main()
