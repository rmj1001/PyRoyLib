class TreeNode[T]:
    def __init__(self, value: T):
        self.value = value
        self.left: "TreeNode[T] | None" = None
        self.right: "TreeNode[T] | None" = None
