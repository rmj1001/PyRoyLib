from monads.maybe import Maybe, Some, Nada
from src.lib.algos.sorting.merge_sort import merge_sort


def binary_search[T](arr: list[T], target: T) -> int | None:
    current_low = 0
    current_high = len(arr) - 1

    while current_low <= current_high:
        mid = (current_high + current_low) // 2

        if arr[mid] == target:
            return mid
        elif arr[mid] > target:
            current_high = mid - 1
        else:
            current_low = mid + 1

    return None


def binary_search_maybe[T](arr: list[T], target: T) -> Maybe[int]:
    current_low = 0
    current_high = len(arr) - 1

    while current_low <= current_high:
        mid = (current_high + current_low) // 2

        if arr[mid] == target:
            return Some(mid)
        elif arr[mid] > target:
            current_high = mid - 1
        elif arr[mid] < target:
            current_low = mid + 1

    return Nada()


def recursive_binary_search[T](
        arr: list[T],
        target: T,
        low: int | None = None,
        high: int | None = None
) -> int | None:
    low = low if low is not None else 0
    high = high if high is not None else len(arr) - 1

    if low > high:
        return None

    mid = (low + high) // 2

    if arr[mid] == target:
        return mid

    elif target < arr[mid]:
        return recursive_binary_search(arr, target, low, mid - 1)

    else:
        return recursive_binary_search(arr, target, mid + 1, high)


def recursive_binary_search_maybe[T](
        arr: list[T],
        target: T,
        sort: bool = False,
        low: Maybe[int] = Nada(),
        high: Maybe[int] = Nada()
) -> Maybe[int]:
    def search(array: list[T], low_val: int, high_val: int) -> Maybe[int]:
        if low_val > high_val:
            return Nada()

        mid = (low_val + high_val) // 2

        if array[mid] == target:
            return Some(mid)

        elif target < array[mid]:
            return search(array, low_val, mid - 1)

        else:
            return search(array, mid + 1, high_val)

    low: int = low.unwrap_or(0)
    high: int = high.unwrap_or(len(arr) - 1)

    if sort:
        arr = merge_sort(arr)

    return search(arr, low, high)
