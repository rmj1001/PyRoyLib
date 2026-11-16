from collections.abc import Callable

from algos.sorting.merge_sort import merge_sort
from monads.maybe import Maybe, Some, Nada
from monads.result import Result, Ok, Err

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

def sequential_search_maybe[T](
        arr: list[T],
        target: Maybe[T] = Nada(),
        condition: Maybe[Predicate] = Nada()
) -> Result[int, str]:
    if target.is_nada() and condition.is_nada():
        return Err('Either a target or a condition is required')

    if target.is_some():
        target: T = target.expect('Target should be Some')

        for idx, item in enumerate(arr):
            if item == target:
                return Ok(idx)

    if condition.is_some():
        condition: Predicate = condition.expect('Condition should be Some')

        for idx, item in enumerate(arr):
            if condition(item):
                return Ok(idx)

    return Err(f'Index not found for item \'{target}\'.')


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

def sorted_sequential_search_maybe[T](
        arr: list[T],
        target: T,
        sort: bool = False
) -> Maybe[int]:
    """Sequential search but for sorted arrays"""
    if sort:
        arr = merge_sort(arr)

    elements = len(arr)
    last_idx = elements - 1

    if elements == 0 or target < arr[0] or target > arr[last_idx]:
        return Nada()

    idx = 0

    while idx < elements:
        if arr[idx] > target:
            return Nada()
        elif arr[idx] == target:
            return Some(idx)
        else:
            idx += 1

    return Nada()
