import unittest
from src.lib.data_structs.graph import Graph, GraphException
from random import randint

def create_random_graph(nodes: int = 10, edges: bool = False) -> Graph[int, int]:
    graph = Graph()
    rand = lambda: randint(0, 100)

    for num in range(0, nodes, 1):
        graph.insert(num, rand())

    if edges and nodes > 3:
        graph.nodes[0].add_edge(1)
        graph.nodes[0].add_edge(2)
        graph.nodes[1].add_edge(2)
        graph.nodes[2].add_edge(3)
        graph.nodes[2].add_edge(0)
        graph.nodes[3].add_edge(4)

    return graph

class TestGraph(unittest.TestCase):
    def test_insert(self):
        """Test inserting new nodes in the graph"""
        graph: Graph = create_random_graph(10)
        graph2: Graph = create_random_graph(0)

        # Tests insertion, len(), bool(), is_empty(),
        self.assertEqual(len(graph), 10)
        self.assertTrue(graph)

        self.assertFalse(graph2)
        self.assertTrue(graph2.is_empty())

        with self.assertRaises(GraphException):
            graph.insert(0, 10)

    def test_node_equality(self):
        """Check that the values of nodes can be equal"""
        graph: Graph = Graph()

        graph.insert(0, 10)
        graph.insert(1, 10)
        graph.insert(2, 20)

        self.assertEqual(graph.nodes[0], graph.nodes[1])
        self.assertNotEqual(graph.nodes[0], graph.nodes[2])

    def test_unidirectional_edges(self):
        graph: Graph = create_random_graph(10, edges=True)

        # No edges have been made yet
        self.assertEqual(graph.count_edges(), 6)

        # Check number of edges for each node
        self.assertEqual(graph.nodes[0].count_edges(), 2)
        self.assertEqual(graph.nodes[1].count_edges(), 1)
        self.assertEqual(graph.nodes[2].count_edges(), 2)
        self.assertEqual(graph.nodes[3].count_edges(), 1)

        # Check total number of edges
        self.assertEqual(graph.count_edges(), 6)

    def test_remove_node(self):
        graph: Graph = create_random_graph(10, edges=True)

        # Remove node with no edges
        graph.remove_node(1)
        self.assertFalse(graph.node_in_edges(1))

        # Remove node with edges
        graph.remove_node(0)
        self.assertFalse(graph.node_in_edges(0))

    def test_is_bidirectional(self):
        graph: Graph = create_random_graph(10, edges=True)

        # No edges exist
        self.assertFalse(graph.is_bidirectional_edge(3, 0))

        # One edge exists
        self.assertFalse(graph.is_bidirectional_edge(1, 2))

        # Two edges exist
        self.assertTrue(graph.is_bidirectional_edge(0, 2))

    def test_add_bidirectional(self):
        graph: Graph = create_random_graph(10, edges=False)

        graph.add_bidirectional_edge(0, 2)
        self.assertTrue(graph.is_bidirectional_edge(0, 2))

    def test_remove_bidirectional(self):
        graph: Graph = create_random_graph(10, edges=False)

        graph.add_bidirectional_edge(0, 2)
        graph.remove_bidirectional_edge(0, 2)
        self.assertFalse(graph.node_in_edges(0))
        self.assertFalse(graph.node_in_edges(2))

    def test_search(self):
        graph: Graph = Graph()

        graph.insert(0, 10)
        graph.insert(1, 2)
        graph.insert(2, 3)
        graph.insert(3, 4)
        graph.insert(4, 10)

        self.assertEqual(graph.search(2), 1)
        self.assertEqual(graph.search(11), None)
        self.assertEqual(graph.search(10), [0, 4])

    def test_all_edges(self):
        graph: Graph = create_random_graph(10, edges=True)

        edges = [
            (0, 1),
            (0, 2),
            (1, 2),
            (2, 3),
            (2, 0),
            (3, 4)
        ]

        self.assertEqual(graph.all_edges(), edges)

    def test_in_edge(self):
        graph: Graph = create_random_graph(10, edges=True)

        self.assertTrue(graph.node_in_edges(0))
        self.assertFalse(graph.node_in_edges(9))

if __name__ == '__main__':
    unittest.main()
