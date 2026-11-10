class TreeNodeException[T](Exception):
    def __init__(self, message: T) -> None:
        self.message = message


class TreeNode[T]:
    def __init__(self, value: T):
        self.value = value
        self.left: "TreeNode[T] | None" = None
        self.right: "TreeNode[T] | None" = None

    def is_leaf(self):
        return self.left is None and self.right is None

    def has_children(self) -> bool:
        return not self.is_leaf()

    def children(self) -> list[TreeNode[T]]:
        nodes = []

        if self.left is not None:
            nodes.append(self.left)

        if self.right is not None:
            nodes.append(self.right)

        return nodes
