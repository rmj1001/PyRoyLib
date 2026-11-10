from .nodes.binary_tree_nodes import TreeNode

class BinarySearchTree[T]:
    def __init__(self, root: TreeNode[T] | None = None) -> None:
        self.root: TreeNode[T] | None = root

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
