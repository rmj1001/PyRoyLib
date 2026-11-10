lazy from src.lib.data_structs.graph import GraphException


type Neighbors[I] = dict[I, int]


class GraphNode[I, T]:
    def __init__(self, node_id: I, value: T, neighbors: Neighbors | None = None) -> None:
        self.node_id = node_id
        self.value = value
        self.neighbors = neighbors if neighbors is not None else {}

    def is_edge(self, other_node: I) -> bool:
        return other_node in self.neighbors

    def add_edge(self, other_node: I, weight: int) -> None:
        if other_node in self.neighbors:
            raise GraphException(f'Unidirectional edge exists from {self.node_id} to {other_node}.')

        self.neighbors[other_node] = weight

    def remove_edge(self, other_node: I) -> None:
        if other_node not in self.neighbors:
            raise GraphException(f'Unidirectional edge does not exist from {self.node_id} to {other_node}.')

        del self.neighbors[other_node]
