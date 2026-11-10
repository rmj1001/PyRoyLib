from algorithms.sorting.swap import swap


def find_min(arr: list, start_index: int):
    min_index = start_index
    size = len(arr)

    for current_index in range(start_index + 1, size, 1):
        if arr[min_index] > arr[current_index]:
            min_index = current_index

    return min_index


def selection_sort(arr: list):
    size = len(arr)
    for start_index in range(0, size - 1, 1):
        min_index = find_min(arr, start_index)
        swap(arr, min_index, start_index)
