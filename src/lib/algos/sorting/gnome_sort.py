def gnome_sort[T](items: list[T]) -> list[T]:
    index = 0

    while index < len(items):
        if index == 0:
            index += 1
        elif items[index] >= items[index - 1]:
            index += 1
        else:
            tmp = items[index]
            items[index] = items[index - 1]
            items[index - 1] = tmp
            index -= 1

    return items
