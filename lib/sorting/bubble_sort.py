from lib.sorting.swap import swap

def bubble_up[T](arr: list[T], top_index: int) -> None:
    for j in range(0, top_index, 1):
        if arr[j] > arr[j + 1]:
            swap(arr, j, j + 1)


def bubble_sort[T](arr: list[T]) -> None:
    size = len(arr)
    top_index = size - 1

    # At each iteration, the largest element is "bubbled up"
    while top_index > 1:
        bubble_up(arr, top_index)
        top_index -= 1
