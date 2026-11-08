class DoubleLinkedNode[T]:
    """Node for a double-linked list"""
    data: T
    previous: DoubleLinkedNode[T] | None
    next: DoubleLinkedNode[T] | None

    def __init__(self, data: T, previous: DoubleLinkedNode | None = None):
        self.data = data
        self.previous = previous
        self.next = None
