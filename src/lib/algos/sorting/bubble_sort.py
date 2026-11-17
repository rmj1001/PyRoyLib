from copy import deepcopy
from src.lib.algos.sorting.swap import swap

def bubble_up[T](arr: list[T], top_index: int) -> list[T]:
    for j in range(0, top_index, 1):
        if arr[j] > arr[j + 1]:
            swap(arr, j, j + 1)

    return arr


def bubble_sort[T](arr: list[T], copy: bool = True) -> list[T]:
    if copy:
        arr = deepcopy(arr)

    size = len(arr)
    top_index = size - 1

    # At each iteration, the largest element is "bubbled up"
    while top_index > 1:
        arr = bubble_up(arr, top_index)
        top_index -= 1

    return arr
