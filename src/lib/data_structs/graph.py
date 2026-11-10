from .nodes.graph_node import GraphNode

type NodeEdge[I] = tuple[I, I]

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

    def insert(self, node_id: I, value: T) -> None:
        """
        Insert a node into the graph
        :param node_id: The ID for the new node
        :param value: The node's value
        """
        if node_id in self.nodes:
            raise GraphException(f'Node with id {node_id} already exists.')

        self.nodes[node_id] = GraphNode(node_id, value)

    def remove_node(self, node_id: I) -> None:
        """
        Remove a node from the graph by its id
        :param node_id: The node's id
        """
        if node_id not in self.nodes:
            raise GraphException(f'Node with id {node_id} does not exist.')

        del self.nodes[node_id]

        for node in self.nodes.values():
            try:
                node.remove_edge(node_id)
            except GraphException:
                continue

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

    def add_bidirectional_edge(self, node_one: I, node_two: I, weight: int = 0) -> None:
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

    def search(self, value: T) -> I | list[I] | None:
        """
        Find ID(s) of nodes whose value matches the given value
        :param value: The value to search for
        :return: ID, list of IDs, or None, depending on how many IDs were found
        """
        nodes: list[I] = []

        for node in self.nodes.values():
            if node.value == value:
                nodes.append(node.node_id)

        if len(nodes) == 0:
            return None
        elif len(nodes) == 1:
            return nodes[0]
        else:
            return nodes

    def all_edges(self) -> list[NodeEdge]:
        """
        Get a list of all edges in the graph, denoted by tuple[node_id, node_id]
        :return: List of edges
        """
        edges: list[NodeEdge] = []

        for node in self.nodes.values():
            edges.extend(node.all_edges())

        return edges

    def node_in_edges(self, node_id: I) -> bool:
        """
        Check to see if a node ID is contained in any edges
        :param node_id: The ID of the node
        :return: True if any edges contain the node ID, False otherwise
        """
        for node_one, node_two in self.all_edges():
            if node_id == node_one or node_id == node_two:
                return True

        return False
