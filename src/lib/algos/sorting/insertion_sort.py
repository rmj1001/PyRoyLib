from copy import deepcopy

def insertion_sort[T](arr: list[T], copy: bool = True) -> list[T]:
    if copy:
        arr = deepcopy(arr)

    n = len(arr)

    for i in range(1, n):
        insert_idx = i
        current_val = arr.pop(i)

        for j in range(i-1, -1, -1):
            if arr[j] > current_val:
                insert_idx = j

        arr.insert(insert_idx, current_val)

    return arr