import unittest
from src.lib.data_structs.graph import Graph
from src.lib.data_structs.nodes.graph_node import GraphNode
from random import randint

class TestGraph(unittest.TestCase):
    def test_insert(self):
        graph: Graph = Graph()

        rand = lambda: randint(0, 100)

        for num in range(0, 6, 1):
            graph.insert(GraphNode(num, rand()))

        self.assertEqual(len(graph), 6)
        self.assertTrue(graph)


if __name__ == '__main__':
    unittest.main()
