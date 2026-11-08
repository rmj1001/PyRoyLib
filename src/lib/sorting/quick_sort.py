from sorting.swap import swap


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


def quick_sort[T](arr: list[T], start: int | None = None, end: int | None = None) -> None:
    """Quick sort a list[T]"""
    # Set start and end to the first and last element of the array if they aren't passed as args
    start = 0 if start is None else start
    end = len(arr)-1 if end is None else end

    if start < end:
        pivot = split(arr, start, end)
        quick_sort(arr, start, pivot - 1)
        quick_sort(arr, pivot + 1, end)
