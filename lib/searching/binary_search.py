from typing import TypeVar

T = TypeVar('T')


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

def recursive_binary_search[T](arr: list[T], target: T, low: int | None = None, high: int | None = None) -> int | None:
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
