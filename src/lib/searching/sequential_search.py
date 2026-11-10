from collections.abc import Callable

type Predicate[T] = Callable[[T], bool]


class SequentialSearchError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)


def sequential_search[T](
        arr: list[T],
        target: T | None = None,
        condition: Predicate | None = None
) -> int | None:
    """Search each element in arr, return first index for element where condition returns True"""
    if target is None and condition is None:
        raise SequentialSearchError("Either target or condition is required")

    for index, item in enumerate(arr):
        if target is not None and item == target:
            return index
        elif condition(item):
            return index

    return None


def sorted_sequential_search[T](
        arr: list[T],
        target: T
) -> int | None:
    """Sequential search but for sorted arrays"""
    elements = len(arr)
    last_idx = elements - 1

    if elements == 0 or target < arr[0] or target > arr[last_idx]:
        return None

    idx = 0

    while idx < elements:
        if arr[idx] > target:
            return None
        elif arr[idx] == target:
            return idx
        else:
            idx += 1

    return None
