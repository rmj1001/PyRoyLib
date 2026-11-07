from typing import Iterable

class QueueException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class QueueNode[T]:
    value: T
    next: QueueNode[T] | None

    def __init__(self, value: T, next_node: QueueNode[T] | None = None):
        self.value = value
        self.next = next_node


class Queue[T]:
    head: QueueNode[T] | None
    tail: QueueNode[T] | None
    _count: int

    def __init__(self, initial_data: Iterable[T] | None = None):
        self.head = None
        self.tail = None
        self._count = 0

        if initial_data is not None:
            for item in initial_data:
                self.enqueue(item)

    def __len__(self) -> int:
        """Get the number of elements in the queue"""
        return self._count

    def __str__(self) -> str:
        """Get the string representation of the queue"""
        string: str = 'Queue('
        values: list[T] = []

        current = self.head
        while current is not None:
            values.append(current.value)
            current = current.next

        string += ', '.join([str(item) for item in values])
        string += ')'

        return string

    def is_empty(self) -> bool:
        """Check if the queue is empty"""
        return self._count == 0

    def enqueue(self, item: T) -> None:
        """Add an item to the end of the queue"""
        if self.head is None:
            self.head = QueueNode(item)
            self.tail = self.head
        else:
            self.tail.next = QueueNode(item)
            self.tail = self.tail.next

        self._count += 1

    def dequeue(self) -> T:
        """Remove and return the item from the front of the queue"""
        if self.head is None:
            raise QueueException("Queue is empty")

        data = self.head.value
        self.head = self.head.next

        self._count -= 1

        return data

    def front(self) -> T:
        """Preview the item at the front of the queue"""
        if self.head is None:
            raise QueueException("Queue is empty")

        return self.head.value
