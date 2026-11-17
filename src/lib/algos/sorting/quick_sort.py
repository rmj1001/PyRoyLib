from copy import deepcopy
from src.lib.algos.sorting.swap import swap


def split[T](arr: list[T], start: int, end: int) -> int:
    """Split a list[T] into two halves, return new pivot index"""
    pivot_value = arr[end]
    i = start - 1

    for j in range(start, end):
        if arr[j] <= pivot_value:
            i += 1
            swap(arr, i, j)

    swap(arr, i+1, end)
    return i + 1


def quick_sort[T](arr: list[T], start: int = 0, end: int = -1, copy: bool = True) -> list[T]:
    """Quick sort a list[T]"""
    if copy:
        arr = deepcopy(arr)

    # Set start and end to the first and last element of the array if they aren't passed as args
    end = len(arr)-1 if end == -1 else end

    if start < end:
        pivot = split(arr, start, end)
        quick_sort(arr, start, pivot - 1)
        quick_sort(arr, pivot + 1, end)

    return arr
