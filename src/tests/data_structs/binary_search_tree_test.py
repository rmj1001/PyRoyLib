import unittest
from src.lib.data_structs.binary_search_tree import BinarySearchTree


class TestBinarySearchTree(unittest.TestCase):
    def test_init_insert(self):
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

if __name__ == '__main__':
    unittest.main()
