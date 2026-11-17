from copy import deepcopy

def gnome_sort[T](arr: list[T], copy: bool = True) -> list[T]:
    """
    Sorting algorithm that works like a gnome sorting flowerpots
    :param arr: list of items to sort
    :param copy: Make a copy of the list before sorting
    :return: sorted list of items
    """
    if copy:
        arr = deepcopy(arr)

    index = 0

    while index < len(arr):
        if index == 0:
            index += 1
        elif arr[index] >= arr[index - 1]:
            index += 1
        else:
            tmp = arr[index]
            arr[index] = arr[index - 1]
            arr[index - 1] = tmp
            index -= 1

    return arr
