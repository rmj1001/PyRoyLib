from typing import TypeVar

T = TypeVar("T")


class SLLNode[T]:
    """Node for single-linked-list"""
    def __init__(self, data: T) -> None:
        self.data = data
        self.next = None


class SingleLinkedList[T]:
    """Single-linked list"""
    head: SLLNode[T] | None
    _max: int

    def __init__(self, starting_data: list[T] | None = None) -> None:
        """Create a single-linked list with either no data or a list of starting data"""
        self.head = None
        self._max = 0

        if starting_data is not None:
            for item in starting_data:
                self.add(item)

    def __len__(self) -> int:
        """Get the number of nodes in the list"""
        return self._max

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
        if self.head is None:
            raise IndexError("List is empty")

        if index < 0 and index + len(self) < 0:
            # Negative index when combined with the list length should be greater than 0
            raise IndexError(
                "Index is out of range: Negative index's absolute value is greater than the length of the list")

        if not 0 <= index < len(self):
            # Index goes from 0 to len(self)-1
            raise IndexError("Index is out of range: Index is greater than the last element's index")

    def add(self, data: T) -> None:
        """Add a new node to the end of the list with the provided data"""
        if self.head is None:
            self.head = SLLNode(data)
            self._max = 1
            return

        current = self.head

        while current.next is not None:
            current = current.next

        current.next = SLLNode(data)
        self._max += 1

    def remove(self, data: T) -> None:
        """Remove the first node with the provided data"""
        if self.head is None:
            raise Exception("Single linked list is empty")

        if self.head.data == data and self.head.next is None:
            self.head = None
            self._max = 0
            return

        if self.head.data == data and self.head.next is not None:
            self.head = self.head.next
            self._max -= 1
            return

        current = self.head

        while current.next is not None:
            if current.next.data == data:
                current.next = current.next.next
                self._max -= 1
                return

            current = current.next

        raise Exception(f"List did not contain data: {data}")

    def get(self, index: int) -> T:
        """Get the item at the provided index"""
        try:
            self.valid_index(index)
        except IndexError as e:
            # Propagate the IndexError up
            raise e

        if index == 0:
            return self.head.data

        if index < 0:
            # Negative indexes will get the item from that position at the end of the list
            return self.get(index + len(self))

        current_index = 0
        current_item = self.head

        while current_index < index:
            current_item = current_item.next
            current_index += 1

        return current_item.data

    def remove_at(self, index: int) -> None:
        """Remove the item at the provided index"""
        try:
            self.valid_index(index)
        except IndexError as e:
            raise e

        if index == 0:
            if self.head.next is None:
                self.head = None
            else:
                self.head = self.head.next

            self._max -= 1
            return

        if index < 0:
            self.remove_at(index + len(self))

        current_index = 0
        current_item = self.head

        while current_index < index - 1:
            current_item = current_item.next
            current_index += 1

        if current_item.next.next is None:
            current_item.next = None
        else:
            current_item.next = current_item.next.next

        self._max -= 1

    def search(self, data: T) -> int:
        """Get the index of the item that matches the provided data"""
        if self.head is None:
            raise Exception("Single linked list is empty")

        current = self.head
        index: int = 0
        found: bool = False

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
