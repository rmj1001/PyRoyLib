from typing import TypeVar, Iterable

T = TypeVar("T")


class SLLNode[T]:
    """Node for single-linked-list"""

    def __init__(self, data: T) -> None:
        self.data = data
        self.next = None


class SingleLinkedList[T]:
    """Single-linked list"""
    head: SLLNode[T] | None
    _nodes: int

    def __init__(self, starting_data: Iterable[T] | None = None) -> None:
        """Create a single-linked list with either no data or a list of starting data"""
        self.head = None
        self._nodes = 0

        # If a list is provided, add each item in the list as a new node
        if starting_data is not None:
            for item in starting_data:
                self.add(item)

    def __len__(self) -> int:
        """Get the number of nodes in the list without traversal"""
        return self._nodes

    def __str__(self) -> str:
        """Get the string representation of the list"""
        if self.head is None:
            return "SLL()"

        output = "SLL("

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

    def valid_index(self, index) -> None:
        """Raise an IndexError exception if the provided index is out of range"""
        if index + len(self) < 0:
            # Negative index when combined with the list length should be greater than 0
            raise IndexError(
                "Index is out of range: Negative index's absolute value is greater than the length of the list")

        if index >= len(self):
            # Index goes from 0 to len(self)-1
            raise IndexError("Index is out of range: Index is greater than the last element's index")

    def add(self, data: T) -> None:
        """Add a new node to the end of the list with the provided data"""
        # New node is the head if a head didn't exist
        if self.head is None:
            self.head = SLLNode(data)
            self._nodes = 1
            return

        # Traverse until tail is found
        current = self.head

        while current.next is not None:
            current = current.next

        # Add new node to end of the linked list, increment nodes counter by 1
        current.next = SLLNode(data)
        self._nodes += 1

    def remove(self, data: T) -> None:
        """Remove the first node with the provided data"""
        if self.head is None:
            raise Exception("Single linked list is empty")

        # Remove head if it is the only node in the linked list
        if self.head.data == data and self.head.next is None:
            self.head = None
            self._nodes = 0
            return

        # Replace the head with the next node in the list
        if self.head.data == data and self.head.next is not None:
            self.head = self.head.next
            self._nodes -= 1
            return

        # Traverse until node with matching data is found, replace that node with the next node
        current = self.head

        while current.next is not None:
            if current.next.data == data:
                current.next = current.next.next
                self._nodes -= 1
                return

            current = current.next

        raise Exception(f"List did not contain data: {data}")

    def get(self, index: int) -> T:
        """Get the item at the provided index"""
        if self.head is None:
            raise Exception("Single linked list is empty")

        # Propagate the IndexError up
        try:
            self.valid_index(index)
        except IndexError as e:
            raise e

        # Return head if index is 0
        if index == 0:
            return self.head.data

        # Convert negative index to positive index (neg. index corresponds with position from tail going backwards)
        if index < 0:
            # Negative indexes will get the item from that position at the end of the list
            return self.get(index + len(self))

        # Traverse list until finding the node with the specified index and return its data
        current_index = 0
        current_item = self.head

        while current_index < index:
            current_item = current_item.next
            current_index += 1

        return current_item.data

    def remove_at(self, index: int) -> None:
        """Remove the item at the provided index"""
        if self.head is None:
            raise Exception("Single linked list is empty")

        # Propagate the index error up
        try:
            self.valid_index(index)
        except IndexError as e:
            raise e

        # Remove head if index is 0
        if index == 0:
            # Head is replaced with next node if next node is not None
            if self.head.next is None:
                self.head = None
            else:
                self.head = self.head.next

            # Decrement nodes counter
            self._nodes -= 1
            return

        # Convert neg. index to positive index (corresponds with position from tail going backwards)
        if index < 0:
            self.remove_at(index + len(self))

        # Traverse list until node at index is reached
        current_index = 0
        current_item = self.head

        while current_index < index - 1:
            current_item = current_item.next
            current_index += 1

        # Replace tail with None
        if current_item.next.next is None:
            current_item.next = None

        # Replace node with its next node
        else:
            current_item.next = current_item.next.next

        # Decrement nodes counter
        self._nodes -= 1

    def search(self, data: T) -> int:
        """Get the index of the first item that matches the provided data"""
        if self.head is None:
            raise Exception("Single linked list is empty")

        current = self.head
        index: int = 0
        found: bool = False

        # Traverse nodes until node's data matches passed data, increment counter if going to next node
        while current is not None:
            if current.data == data:
                found = True
                break
            else:
                current = current.next
                index += 1

        if not found:
            raise Exception(f"List did not contain data: {data}")

        return index


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
        self.head = None
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
        """Check if list has nodes"""
        return self._nodes == 0

    def valid_index(self, index: int) -> None:
        """Raise an IndexError exception if the provided index is out of range"""
        if index + len(self) < 0:
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
        else:
            current = self.head

            while current.next is not None:
                current = current.next

            current.next = DLLNode(data, previous=current)

        self._nodes += 1

    def get(self, index: int) -> T:
        """Get data from node at given index"""
        if self.head is None:
            raise Exception("Single linked list is empty")

        # Propagate IndexError up
        try:
            self.valid_index(index)
        except IndexError as e:
            raise e

        # Convert negative index to positive index (corresponding to position from tail going backwards)
        if index < 0:
            return self.get(index + len(self))

        # Traverse list
        current = self.head
        current_index = 0

        while current is not None:
            # Return data if index matches the current node's index, or else traverse again
            if index == current_index:
                return current.data
            else:
                current = current.next
                current_index += 1

        raise IndexError(f"Index {index} is out of range")

    def search(self, data: T) -> int:
        """Search for first node index with given data"""
        if self.head is None:
            raise Exception("Single linked list is empty")

        current = self.head
        index: int = 0

        while current is not None:
            if current.data == data:
                return index
            else:
                current = current.next
                index += 1

        raise Exception(f"List did not contain data: {data}")

    def remove(self, data: T) -> None:
        """Remove first node from list with given data"""
        if self.head is None:
            raise Exception("Single linked list is empty")

        # Remove head if it is the only node in the linked list
        if self.head.data == data and self.head.next is None:
            self.head = None
            self._nodes -= 1
            return

        # Replace head with next node in the list
        if self.head.data == data and self.head.next is not None:
            self.head = self.head.next
            self.head.previous = None
            self._nodes -= 1
            return

        # Traverse until node with matching data is found, then delete it
        current = self.head

        while current.next is not None:
            if current.next.data != data:
                current = current.next
                continue

            current.next = current.next.next

            if current.next is not None:
                current.next.previous = current

            self._nodes -= 1
            return

        raise Exception(f"List did not contain data: {data}")

    def remove_at(self, index: int) -> None:
        """Remove node from list at given index"""
        if self.head is None:
            raise Exception("Single linked list is empty")

        # Propagate IndexError
        try:
            self.valid_index(index)
        except IndexError as e:
            raise e

        # Remove head if it is the only node in the linked list
        if index == 0 and self.head.next is None:
            self.head = None
            self._nodes -= 1
            return None

        # Replace head with next node in the list
        if index == 0 and self.head.next is not None:
            self.head = self.head.next
            self.head.previous = None
            self._nodes -= 1
            return None

        # Convert negative index to positive index corresponding with position from tail going backwards
        if index < 0:
            return self.remove_at(index + len(self))

        # Traverse list until node at index is reached
        current_index = 0
        current_item = self.head

        while current_index < index - 1:
            current_item = current_item.next
            current_index += 1

        # Replace tail with None
        if current_item.next.next is None:
            current_item.next = None

        # Replace node with its next node
        else:
            current_item.next = current_item.next.next
            current_item.next.previous = current_item

        # Decrement nodes counter
        self._nodes -= 1
        return None
