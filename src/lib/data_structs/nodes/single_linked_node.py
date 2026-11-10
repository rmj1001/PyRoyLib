class SingleLinkedNode[T]:
    """Data container for individual items in a Stack"""
    data: T
    next: SingleLinkedNode[T] | None

    def __init__(self, value: T, next_node: SingleLinkedNode[T] | None = None) -> None:
        self.data = value
        self.next = next_node
