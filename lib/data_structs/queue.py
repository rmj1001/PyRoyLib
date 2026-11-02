from typing import TypeVar, List, Iterable

T = TypeVar('T')

class QueueException(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class Queue[T]:
    data: List[T]
    elements: int

    def __init__(self, starting_data: Iterable[T] | None = None) -> None:
        """Initialize a queue, with or without starting data"""
        self.data = []
        self.elements = 0

        if starting_data is not None:
            for item in starting_data:
                self.data.append(item)
                self.elements += 1

    def __len__(self) -> int:
        """Return the number of elements in the queue"""
        return self.elements

    def __str__(self) -> str:
        """String representation of the queue"""
        str_data = [str(item) for item in self.data]
        return f"Queue({', '.join(str_data)})" if len(self) > 0 else "Queue()"

    def is_empty(self) -> bool:
        """Check if the queue is empty."""
        return self.elements == 0

    def enqueue(self, data: T) -> None:
        """Add data to the queue."""
        self.data.insert(0, data)
        self.elements += 1

    def dequeue(self) -> T:
        """Remove data from the queue."""
        if self.is_empty():
            raise QueueException('Queue is empty')

        data = self.data.pop(0)
        self.elements -= 1
        return data

    def front(self) -> T:
        """Get the last data from the queue."""
        if self.is_empty():
            raise QueueException('Queue is empty')

        return self.data[0]
