from typing import TypeVar, Iterable, Callable

from lib.data_structs.single_linked_list import LinkedListException

T = TypeVar("T")
Predicate = Callable[[T], bool]


class DLLNode[T]:
    """Node for a double-linked list"""

    def __init__(self, data: T, previous: DLLNode | None = None):
        self.data = data
        self.previous = previous
        self.next = None


class DoubleLinkedList[T]:
    """Double linked list implementation"""

    def __init__(self, starting_data: Iterable[T] | None = None) -> None:
        """Constructor with optional parameter to populate list with items from iterable"""
        self.head: DLLNode[T] | None = None
        self.tail: DLLNode[T] | None = None
        self._nodes = 0

        if starting_data is not None:
            for item in starting_data:
                self.add(item)

    def __len__(self) -> int:
        """Get number of nodes without traversal"""
        return self._nodes

    def __str__(self) -> str:
        """Get the string representation of the list"""
        if self.head is None:
            return "DLL()"

        output = "DLL("

        current = self.head

        while current is not None:
            output += f"{current.data}, "
            current = current.next

        output = output.removesuffix(', ')
        output += ")"

        return output

    def is_empty(self) -> bool:
        """Check if the list is empty"""
        return len(self) == 0

    def is_tail(self, index: int) -> bool:
        """Check if index is the tail of the list"""
        return index == -1 or index == len(self) - 1

    def process_index(self, index: int) -> int:
        """Convert negative indexes to positive ones"""
        return index if index >= 0 else index + len(self)

    def valid_index(self, index) -> None:
        """Raise an IndexError exception if the provided index is out of range"""
        index = self.process_index(index)

        if index < 0:
            # Negative index when combined with the list length should be greater than 0
            raise IndexError(
                "Index is out of range: Negative index's absolute value is greater than the length of the list")

        if index >= len(self):
            # Index goes from 0 to len(self)-1
            raise IndexError("Index is out of range: Index is greater than the last element's index")

    def add(self, data: T) -> None:
        """Add node to end of list while specifying its parent"""
        if self.head is None:
            self.head = DLLNode(data)
            self.tail = self.head
            self._nodes += 1
            return

        self.tail.next = DLLNode(data=data, previous=self.tail)

        if self.tail is not None:
            self.tail = self.tail.next

        self._nodes += 1

    def get_node(self, index: int) -> DLLNode[T]:
        """Get the node address at the provided index"""
        if self.head is None:
            raise LinkedListException("Double linked list is empty")

        # Convert negative indexes to positive and validate
        index = self.process_index(index)
        self.valid_index(index)

        # Return head if index is 0
        if index == 0:
            return self.head

        # Return tail if index is -1 or len(self)-1
        if self.is_tail(index) and self.tail is not None:
            return self.tail

        # Get other nodes
        current_index = 0
        current_item: DLLNode[T] | None = self.head

        while current_index < index and current_item is not None:
            current_item = current_item.next
            current_index += 1

        if current_item is not None:
            return current_item
        else:
            raise LinkedListException(f"Double linked list does not contain node at index {index}")

    def get_data(self, index: int) -> T:
        """Get data from node at given index"""
        node = self.get_node(index)
        return node.data

    def search(self, data: T = None, conditional: Predicate | None = None) -> int:
        """Get the index of the first item that matches the provided data"""
        if self.head is None:
            raise LinkedListException("Double linked list is empty")

        if data is None and conditional is None:
            raise LinkedListException("You must provide data or a conditional.")

        current = self.head
        index: int = 0

        # Traverse nodes until node's data matches passed data, increment counter if going to next node
        while current is not None:
            if data is not None and current.data == data:
                return index
            elif conditional is not None and conditional(current.data):
                return index
            else:
                current = current.next
                index += 1

        if conditional is not None:
            raise LinkedListException(f"List did not contain data matching the condition: {conditional}")
        else:
            raise LinkedListException(f"List did not contain data: {data if data is not None else 'None'}")

    def remove_at(self, index: int) -> None:
        """Remove node from list at given index"""
        if self.head is None:
            raise LinkedListException("Double linked list is empty")

        # Convert negative indexes to positive ones and validate them
        index = self.process_index(index)
        self.valid_index(index)

        # Handle head index cases
        if index == 0 and len(self) == 1:
            self.head = None
            self.tail = None
            self._nodes -= 1
            return

        if index == 0 and len(self) > 1:
            self.head = self.head.next

            if self.head is not None:
                self.head.next.previous = None

            self._nodes -= 1
            return

        previous_node = self.get_node(index - 1)

        # The next node is the node at the passed index
        if previous_node.next is None:
            raise IndexError(f"No node exists at index {index}.")

        # Remove node at the provided index, replacing it with next node if it exists, or setting it to None
        previous_node.next = previous_node.next.next if previous_node.next.next is not None else None

        # Update the next node's previous field to the previous node
        if previous_node.next is not None:
            previous_node.next.previous = previous_node

        # Update tail address if necessary
        if self.is_tail(index):
            self.tail = previous_node.next if previous_node.next is not None else previous_node

        # Decrement nodes counter
        self._nodes -= 1

    def remove(self, data: T = None, conditional: Predicate | None = None) -> None:
        """Remove the first node with the provided data"""
        if self.head is None:
            raise LinkedListException("Double linked list is empty")

        index = self.search(data, conditional)
        self.remove_at(index)

    def update(self, index: int, data: T) -> None:
        """Update the data of a node at a given index"""
        if self.head is None:
            raise LinkedListException("Double linked list is empty")

        node = self.get_node(index)
        node.data = data
