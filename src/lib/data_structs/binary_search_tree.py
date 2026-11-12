from .nodes.binary_tree_nodes import TreeNode


class BinarySearchTree[T]:
    def __init__(self, root: TreeNode[T] | None = None) -> None:
        self.root: TreeNode[T] | None = root

    def __eq__(self, other: object) -> bool:
        """
        Compare the preorder lists of two binary search trees
        :param other: Other binary search tree
        :return: True if other is BST and preorder lists are equal, False otherwise
        """
        if not isinstance(other, BinarySearchTree):
            return NotImplemented

        return self.pre_order() == other.pre_order()

    def is_empty(self) -> bool:
        """
        Check if tree has a root node
        :return: True if tree has a root node, False otherwise
        """
        return self.root is None

    def insert(self, value: T) -> TreeNode[T] | None:
        """
        Insert node with given value at root of tree
        :param value: The value to insert
        :return: The root node
        """
        result = self.insert_rec(self.root, value)

        if self.root is None:
            self.root = result

        return result

    def insert_rec(self, node: TreeNode[T] | None, value: T) -> TreeNode[T]:
        """
        Recursively walk tree until space found to insert node
        :param node: The starting node to walk from
        :param value: The value to insert
        :return: The inserted node
        """
        if node is None:
            return TreeNode(value)

        if value < node.value:
            node.left = self.insert_rec(node.left, value)

        if value > node.value:
            node.right = self.insert_rec(node.right, value)

        return node

    def search(self, value) -> bool:
        """
        Determine if tree contains a node with given value
        :param value: The value to search for
        :return: True if found, False otherwise
        """
        return self.get(value) is not None

    def search_rec(self, node: TreeNode[T] | None, value) -> bool:
        """
        Determine if node or its descendants contain given value
        :param node: The node to start searching from
        :param value: The value to search for
        :return: True if found, False otherwise
        """
        return self.get_rec(node, value) is not None

    def get(self, value: T) -> TreeNode[T] | None:
        """
        Get node from tree with given value
        :param value: The value to search for
        :return: The node with given value
        """
        return self.get_rec(self.root, value)

    def get_rec(self, node: TreeNode[T] | None, value: T) -> TreeNode[T] | None:
        """
        Get node or its descendant with given value
        :param node: The node to start searching from
        :param value: The value to search for
        :return: The node with given value
        """
        if node is None:
            return None

        if value < node.value:
            return self.get_rec(node.left, value)

        if value > node.value:
            return self.get_rec(node.right, value)

        return node

    def pre_order(self) -> list[T]:
        """
        Return a list of values from the BST in pre-order.
        :return: List of pre-order values
        """
        items: list[T] = []
        self.pre_order_rec(self.root, items)
        return items

    def pre_order_rec(self, node: TreeNode[T] | None, items: list[T]) -> None:
        """
        Append a list of values from a node in pre-order.
        """
        if node is None:
            return

        items.append(node.value)
        self.pre_order_rec(node.left, items)
        self.pre_order_rec(node.right, items)

    def in_order(self) -> list[T]:
        """
        Return a list of values from the BST in-order.
        :return: List of in-order values
        """
        items: list[T] = []
        self.in_order_rec(self.root, items)
        return items

    def in_order_rec(self, node: TreeNode[T] | None, items: list[T]) -> None:
        """
        Append a list of values from a node in-order.
        """
        if node is None:
            return

        self.in_order_rec(node.left, items)
        items.append(node.value)
        self.in_order_rec(node.right, items)

    def post_order(self) -> list[T]:
        """
        Return a list of values from the BST in post-order.
        :return: List of post-order values
        """
        items: list[T] = []
        self.post_order_rec(self.root, items)
        return items

    def post_order_rec(self, node: TreeNode[T] | None, items: list[T]) -> None:
        """
        Append a list of values from a node in post-order.
        """
        if node is None:
            return

        self.post_order_rec(node.left, items)
        self.post_order_rec(node.right, items)
        items.append(node.value)

    def minimum(self, node: TreeNode[T] | None = None) -> T:
        """
        Get the minimum value in BST
        :param node: The starting node, or tree root if node is None
        :return: The minimum value
        """
        if node is None:
            node = self.root

        current: TreeNode[T] | None = node

        while current.left is not None:
            current = current.left

        return current.value

    def maximum(self, node: TreeNode[T] | None = None) -> T:
        """
        Get the maximum value in BST
        :param node: The starting node, or tree root if node is None
        :return: The maximum value
        """
        if node is None:
            node = self.root

        current: TreeNode[T] | None = node

        while current.right is not None:
            current = current.right

        return current.value

    def delete(self, value: T) -> None:
        """
        Delete node with given value starting at root of tree
        :param value: The value to delete
        """
        self.delete_rec(value, self.root)

    def delete_rec(self, value: T, node: TreeNode[T] | None = None) -> TreeNode[T] | None:
        """
        Delete a node with given value, while preserving its descendants.
        :param value: The value to delete
        :param node: The current node
        :return:
        """
        if node is None:
            return node

        if value < node.value:
            node.left = self.delete_rec(value, node.left)
        elif value > node.value:
            node.right = self.delete_rec(value, node.right)
        else:
            # Handle cases where node has 0-1 children
            if not node.left:
                temp = node.right
                node = None
                return temp
            if not node.right:
                temp = node.left
                node = None
                return temp

            # Handle cases where node has 2 children
            # by replacing it with the in-order successor
            node.value = self.minimum(node.right).value
            node.right = self.delete_rec(node.value, node.right)

        return node
