type NodeData[K, V] = tuple[K, V]


class KeyedBSTException[T](Exception):
    def __init__(self, message: T) -> None:
        self.message = message


class KeyedBSTNode[K, V]:
    def __init__(self, key: K, value: V):
        self.key: K = key
        self.value: V = value
        self.left: "KeyedBSTNode[K, V] | None" = None
        self.right: "KeyedBSTNode[K, V] | None" = None

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, KeyedBSTNode):
            return NotImplemented

        return self.data() == other.data()

    def is_leaf(self):
        """
        Check if node doesn't have any children
        :return: True if no children exist, False otherwise
        """
        return self.left is None and self.right is None

    def has_children(self) -> bool:
        """
        Check if node has children
        :return: True if children exist, False otherwise
        """
        return not self.is_leaf()

    def children(self) -> list[KeyedBSTNode[K, V]]:
        """
        Create a list of child nodes
        :return: List of child nodes
        """
        nodes = []

        if self.left is not None:
            nodes.append(self.left)

        if self.right is not None:
            nodes.append(self.right)

        return nodes

    def data(self) -> NodeData:
        """
        Create a key/value pair from data contained in the node
        :return: Tuple key/value pair
        """
        return self.key, self.value


class KeyedBST[K, V]:
    def __init__(self, root: KeyedBSTNode[K, V] | None = None) -> None:
        self.root: KeyedBSTNode[K, V] | None = root

    def __eq__(self, other: object) -> bool:
        """
        Compare the preorder lists of two binary search trees
        :param other: Other binary search tree
        :return: True if other is BST and preorder lists are equal, False otherwise
        """
        if not isinstance(other, KeyedBST):
            return NotImplemented

        return self.pre_order() == other.pre_order()

    def is_empty(self) -> bool:
        """
        Check if tree has a root node
        :return: True if tree has a root node, False otherwise
        """
        return self.root is None

    def insert(self, key: K, value: V) -> KeyedBSTNode[K, V] | None:
        """
        Insert node with given value at root of tree
        :param key: The value to insert
        :param value: The value to insert
        :return: The root node
        """
        result = self.insert_rec(self.root, key, value)

        if self.root is None:
            self.root = result

        return result

    def insert_rec(self, node: KeyedBSTNode[K, V] | None, key: K, value: V) -> KeyedBSTNode[K, V]:
        """
        Recursively walk tree until space found to insert node
        :param node: The starting node to walk from
        :param key: The id of the value to insert
        :param value: The value to insert
        :return: The inserted node
        """
        if node is None:
            return KeyedBSTNode(key, value)

        if key < node.key:
            node.left = self.insert_rec(node.left, key, value)

        if key > node.key:
            node.right = self.insert_rec(node.right, key, value)

        return node

    def search(self, key: K) -> bool:
        """
        Determine if tree contains a node with given value
        :param key: The ID of the value to search for
        :return: True if found, False otherwise
        """
        return self.get(key) is not None

    def search_rec(self, node: KeyedBSTNode[K, V] | None, key: K) -> bool:
        """
        Determine if node or its descendants contain given value
        :param node: The node to start searching from
        :param key: The ID of the value to search for
        :return: True if found, False otherwise
        """
        return self.get_rec(node, key) is not None

    def get(self, key: K) -> KeyedBSTNode[K, V] | None:
        """
        Get node from tree with given value
        :param key: The value to search for
        :return: The node with given value
        """
        return self.get_rec(self.root, key)

    def get_rec(self, node: KeyedBSTNode[K, V] | None, key: K) -> KeyedBSTNode[K, V] | None:
        """
        Get node or its descendant with given value
        :param node: The node to start searching from
        :param key: The ID of the value to search for
        :return: The node with given value
        """
        if node is None:
            return None

        if key < node.key:
            return self.get_rec(node.left, key)

        if key > node.key:
            return self.get_rec(node.right, key)

        return node

    def pre_order(self) -> list[NodeData]:
        """
        Return a list of values from the BST in pre-order.
        :return: List of pre-order values
        """
        items: list[NodeData] = []
        self.pre_order_rec(self.root, items)
        return items

    def pre_order_rec(self, node: KeyedBSTNode[K, V] | None, items: list[NodeData]) -> None:
        """
        Append a list of values from a node in pre-order.
        """
        if node is None:
            return

        items.append(node.data())
        self.pre_order_rec(node.left, items)
        self.pre_order_rec(node.right, items)

    def in_order(self) -> list[NodeData]:
        """
        Return a list of values from the BST in-order.
        :return: List of in-order values
        """
        items: list[NodeData] = []
        self.in_order_rec(self.root, items)
        return items

    def in_order_rec(self, node: KeyedBSTNode[K, V] | None, items: list[NodeData]) -> None:
        """
        Append a list of values from a node in-order.
        """
        if node is None:
            return

        self.in_order_rec(node.left, items)
        items.append(node.data())
        self.in_order_rec(node.right, items)

    def post_order(self) -> list[NodeData]:
        """
        Return a list of values from the BST in post-order.
        :return: List of post-order values
        """
        items: list[NodeData] = []
        self.post_order_rec(self.root, items)
        return items

    def post_order_rec(self, node: KeyedBSTNode[K, V] | None, items: list[NodeData]) -> None:
        """
        Append a list of values from a node in post-order.
        """
        if node is None:
            return

        self.post_order_rec(node.left, items)
        self.post_order_rec(node.right, items)
        items.append(node.data())

    def minimum(self, node: KeyedBSTNode[K, V] | None = None) -> K:
        """
        Get the minimum value in BST
        :param node: The starting node, or tree root if node is None
        :return: The minimum value
        """
        if node is None:
            node = self.root

        current: KeyedBSTNode[K, V] | None = node

        while current.left is not None:
            current = current.left

        return current.key

    def maximum(self, node: KeyedBSTNode[K, V] | None = None) -> K:
        """
        Get the maximum value in BST
        :param node: The starting node, or tree root if node is None
        :return: The maximum value
        """
        if node is None:
            node = self.root

        current: KeyedBSTNode[K, V] | None = node

        while current.right is not None:
            current = current.right

        return current.key

    def delete(self, key: K):
        """
        Delete node with given value starting at root of tree
        :param key: The ID of the value to delete
        """
        return self.delete_rec(key, self.root)

    def delete_rec(self, key: K, node: KeyedBSTNode[K, V] | None = None) -> KeyedBSTNode[K, V] | None:
        """
        Delete a node with given value, while preserving its descendants.
        :param key: The ID of the value to delete
        :param node: The current node
        :return:
        """
        if node is None:
            return node

        if key < node.key:
            node.left = self.delete_rec(key, node.left)
        elif key > node.key:
            node.right = self.delete_rec(key, node.right)
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
            minimum = self.minimum(node.right)
            node.key = minimum.key
            node.value = minimum.value
            node.right = self.delete_rec(node.key, node.right)

        return node

    def height(self) -> int:
        """Get the height of the tree"""
        return self.height_rec(self.root)

    def height_rec(self, node: KeyedBSTNode[K, V] | None = None) -> int:
        """Get the height of a node recursively"""
        if node is None:
            return 0

        return 1 + max(self.height_rec(node.left), self.height_rec(node.right))

    def is_balanced(self):
        """Check if the tree is balanced"""
        return self.is_balanced_rec(self.root)

    def is_balanced_rec(self, node: KeyedBSTNode[K, V] | None = None) -> bool:
        """Check if a node is balanced recursively"""
        if node is None:
            return True

        left_height = self.height_rec(node.left)
        right_height = self.height_rec(node.right)
        height_diff = left_height - right_height

        if height_diff < -1 or height_diff > 1:
            return False

        return self.is_balanced_rec(node.left) and self.is_balanced_rec(node.right)
