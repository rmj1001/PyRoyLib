def swap(arr: list, index1: int, index2: int) -> None:
    """Swap two elements in-place in an array"""
    temp = arr[index1]
    arr[index1] = arr[index2]
    arr[index2] = temp
