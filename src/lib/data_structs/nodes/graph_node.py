lazy from src.lib.data_structs.graph import GraphException


type Neighbors[I] = dict[I, int]


class GraphNode[I, T]:
    def __init__(self, node_id: I, value: T, neighbors: Neighbors | None = None) -> None:
        self.node_id: I = node_id
        self.value: T = value
        self.neighbors: Neighbors[I] = neighbors if neighbors is not None else {}

    def __len__(self) -> int:
        """
        Alias for GraphNode.count_edges()
        :return: Number of edges
        """
        return self.count_edges()

    def __eq__(self, other: object) -> bool:
        """
        Check if values of two nodes are equal
        :param other: Other node
        :return: True if other object is GraphNode and values are equal, else False
        """
        if not isinstance(other, GraphNode):
            return NotImplemented

        return self.value == other.value

    def count_edges(self):
        """
        Get the number of edges between this node and other nodes
        :return: Number of edges
        """
        return len(self.neighbors)

    def is_edge(self, other_node: I) -> bool:
        """
        Check to see if other node has an edge with this node
        :param other_node: ID of other node
        :return: True if edge exists, else False
        """
        return other_node in self.neighbors

    def add_edge(self, other_node: I, weight: int = 0) -> None:
        """
        Add an edge between this node and another node
        :param other_node: ID of other node
        :param weight: The weight of the edge
        """
        if other_node in self.neighbors:
            raise GraphException(f'Unidirectional edge exists from {self.node_id} to {other_node}.')

        self.neighbors[other_node] = weight

    def remove_edge(self, other_node: I) -> None:
        """
        Remove an edge between this node and another node
        :param other_node: ID of other node
        """
        if other_node not in self.neighbors:
            raise GraphException(f'Unidirectional edge does not exist from {self.node_id} to {other_node}.')

        del self.neighbors[other_node]

    def all_edges(self) -> list[tuple[I, I]]:
        """
        Get a list of all edges for this node, denoted by tuple[node_id, node_id]
        :return: List of edges
        """
        edges: list[tuple[I, I]] = []

        for neighbor in self.neighbors:
            edges.append((self.node_id, neighbor))

        return edges
