from .nodes.graph_node import GraphNode

class GraphException[T](Exception):
    def __init__(self, message: T):
        super().__init__(message)

class Graph[I, T]:
    nodes: dict[I, GraphNode[I, T]]

    def __init__(self) -> None:
        self.nodes = {}

    def __len__(self) -> int:
        """
        Get the number of nodes in the graph
        :return: Number of nodes
        """
        return len(self.nodes)

    def __bool__(self) -> bool:
        """
        Check if the graph contains nodes
        :return:
        """
        return len(self) > 0

    def is_empty(self) -> bool:
        """
        Check if the graph does not have nodes
        :return: True if no nodes exist, else False
        """
        return len(self) == 0

    def count_edges(self) -> int:
        """
        Get the total number of edges in the graph
        :return: Number of edges
        """
        edges: int = 0

        for node in self.nodes.values():
            edges += node.count_edges()

        return edges

    def insert(self, node: GraphNode[I, T]) -> None:
        """
        Insert a node into the graph
        :param node: The node to insert
        """
        if node.node_id in self.nodes:
            raise GraphException(f'Node with id {node.node_id} already exists.')

        self.nodes[node.node_id] = node

    def remove_node(self, node_id: I) -> None:
        """
        Remove a node from the graph by its id
        :param node_id: The node's id
        """
        if node_id not in self.nodes:
            raise GraphException(f'Node with id {node_id} does not exist.')

        del self.nodes[node_id]

        for node in self.nodes:
            if node_id in node.neighbors:
                node.neighbors.remove(node)

    def is_bidirectional_edge(self, node_one: I, node_two: I) -> bool:
        """
        Check if edges exist in two directions between two nodes
        :param node_one: The first node's ID
        :param node_two: the second node's ID
        :return: True if two edges exist, else False
        """
        node_one: GraphNode[I, T] = self.nodes[node_one]
        node_two: GraphNode[I, T] = self.nodes[node_two]

        return node_one.is_edge(node_two.node_id) and node_two.is_edge(node_one.node_id)

    def add_bidirectional_edge(self, node_one: I, node_two: I, weight: int) -> None:
        """
        Create two edges between two nodes so that each node connects to the other bidirectionally
        :param node_one: The first node's ID
        :param node_two: The second node's ID
        :param weight: The weight of both edges
        :return:
        """
        node_one: GraphNode[I, T] = self.nodes[node_one]
        node_two: GraphNode[I, T] = self.nodes[node_two]

        node_one.add_edge(node_two.node_id, weight)
        node_two.add_edge(node_one.node_id, weight)

    def remove_bidirectional_edge(self, node_one: I, node_two: I) -> None:
        """
        Remove all edges between two nodes, so that both nodes do not connect to each other
        :param node_one: The first node's ID
        :param node_two: The second node's ID
        """
        if not self.is_bidirectional_edge(node_one, node_two):
            raise GraphException(f'Bidirectional edge does not exist between nodes {node_one} and {node_two}.')

        node_one: GraphNode[I, T] = self.nodes[node_one]
        node_two: GraphNode[I, T] = self.nodes[node_two]

        node_one.remove_edge(node_two.node_id)
        node_two.remove_edge(node_one.node_id)

    def get_node(self, value: T) -> GraphNode[I, T] | list[GraphNode[I, T]] | None:
        """
        Get a node by its contained value, multiple nodes if they match, or None if no node contains that value.
        :param value:
        :return:
        """
        return self.nodes.get(lambda node: node.value == value, None)
