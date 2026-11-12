import unittest

from nodes.binary_tree_nodes import TreeNode
from src.lib.data_structs.binary_search_tree import BinarySearchTree


class TestTreeNode(unittest.TestCase):
    def test_init(self):
        node: TreeNode = TreeNode(1)

        self.assertEqual(node.value, 1)

    def test_left_right(self):
        node: TreeNode = TreeNode(2)
        node.left = TreeNode(1)

        self.assertEqual(node.left.value, 1)

    def test_is_leaf_has_children(self):
        node: TreeNode = TreeNode(2)
        node.left = TreeNode(1)

        node2 = TreeNode(2)

        self.assertTrue(node.has_children())
        self.assertTrue(node2.is_leaf())

    def test_children(self):
        node: TreeNode = TreeNode(2)
        node.left = TreeNode(1)

        nodes = node.children()

        self.assertTrue(len(nodes) == 1)


class TestBinarySearchTree(unittest.TestCase):
    def test_equality(self):
        tree1: BinarySearchTree = BinarySearchTree()
        tree2: BinarySearchTree = BinarySearchTree()
        tree3: BinarySearchTree = BinarySearchTree()

        tree1.insert(1)
        tree1.insert(2)
        tree1.insert(3)

        tree2.insert(1)
        tree2.insert(2)
        tree2.insert(3)

        tree3.insert(0)
        tree3.insert(1)
        tree3.insert(2)

        self.assertEqual(tree1, tree2)
        self.assertNotEqual(tree1, tree3)

    def test_is_empty(self):
        tree: BinarySearchTree = BinarySearchTree()
        tree2: BinarySearchTree = BinarySearchTree()

        tree2.insert(1)

        self.assertTrue(tree.is_empty())
        self.assertFalse(tree2.is_empty())

    def test_insert(self):
        tree: BinarySearchTree = BinarySearchTree()

        # Initialization works, so this mainly
        # tests tree node insertion
        tree.insert(1)
        tree.insert(2)
        tree.insert(3)
        tree.insert(0)

        self.assertEqual(tree.root.value, 1)
        self.assertEqual(tree.root.right.value, 2)
        self.assertEqual(tree.root.right.right.value, 3)
        self.assertEqual(tree.root.left.value, 0)

    def test_search_get(self):
        tree: BinarySearchTree = BinarySearchTree()

        tree.insert(1)
        tree.insert(2)
        tree.insert(3)
        tree.insert(0)

        # tree.search() calls tree.get(), so both
        # functions are tested in this
        self.assertTrue(tree.search(1))
        self.assertFalse(tree.search(-1))

    def test_in_order(self):
        tree: BinarySearchTree = BinarySearchTree()

        tree.insert(1)
        tree.insert(2)
        tree.insert(3)
        tree.insert(0)

        ordered: list[int] = [0, 1, 2, 3]

        self.assertEqual(tree.in_order(), ordered)

    def test_pre_order_traverse(self):
        tree: BinarySearchTree = BinarySearchTree()

        tree.insert(1)
        tree.insert(2)
        tree.insert(3)
        tree.insert(0)

        ordered: list[int] = [1, 0, 2, 3]

        self.assertEqual(tree.pre_order(), ordered)

    def test_post_order_traverse(self):
        tree: BinarySearchTree = BinarySearchTree()

        tree.insert(1)
        tree.insert(2)
        tree.insert(3)
        tree.insert(0)

        ordered: list[int] = [0, 3, 2, 1]

        self.assertEqual(tree.post_order(), ordered)

    def test_minimum_maximum(self):
        tree: BinarySearchTree = BinarySearchTree()

        tree.insert(1)
        tree.insert(2)
        tree.insert(3)
        tree.insert(0)

        self.assertEqual(tree.minimum(), 0)
        self.assertEqual(tree.maximum(), 3)

    def test_delete(self):
        tree: BinarySearchTree[float] = BinarySearchTree()

        tree.insert(1.0)
        tree.insert(2.0)
        tree.insert(3.0)
        tree.insert(0.0)
        tree.insert(-1.0)
        tree.insert(0.5)

        self.assertEqual(tree.in_order(), [-1.0, 0.0, 0.5, 1.0, 2.0, 3.0])

        tree.delete(0.5)

        self.assertEqual(tree.in_order(), [-1.0, 0.0, 1.0, 2.0, 3.0])


if __name__ == '__main__':
    unittest.main()
