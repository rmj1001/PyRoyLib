class SingleLinkedNode[T]:
    """Data container for individual items in a Stack"""
    value: T
    next: SingleLinkedNode[T] | None

    def __init__(self, value: T, next_node: SingleLinkedNode[T] | None = None) -> None:
        self.value = value
        self.next = next_node
