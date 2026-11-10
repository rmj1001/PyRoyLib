from .nodes.graph_node import GraphNode

class GraphException[T](Exception):
    def __init__(self, message: T):
        super().__init__(message)

class Graph[I, T]:
    nodes: dict[I, GraphNode[I, T]]

    def __init__(self):
        self.nodes = {}

    def __len__(self) -> int:
        return len(self.nodes)

    def __bool__(self) -> bool:
        return len(self) > 0

    def insert(self, node: GraphNode[I, T]) -> None:
        if node.node_id in self.nodes:
            raise GraphException(f'Node with id {node.node_id} already exists.')

        self.nodes[node.node_id] = node

    def remove_node(self, node_id: I) -> None:
        if node_id not in self.nodes:
            raise GraphException(f'Node with id {node_id} does not exist.')

        del self.nodes[node_id]

        for node in self.nodes:
            if node_id in node.neighbors:
                node.neighbors.remove(node)

    def is_bidirectional_edge(self, node_one: I, node_two: I) -> bool:
        node_one: GraphNode[I, T] = self.nodes[node_one]
        node_two: GraphNode[I, T] = self.nodes[node_two]

        return node_one.is_edge(node_two.node_id) and node_two.is_edge(node_one.node_id)

    def add_bidirectional_edge(self, node_one: I, node_two: I, weight: int) -> None:
        node_one: GraphNode[I, T] = self.nodes[node_one]
        node_two: GraphNode[I, T] = self.nodes[node_two]

        node_one.add_edge(node_two.node_id, weight)
        node_two.add_edge(node_one.node_id, weight)

    def remove_bidirectional_edge(self, node_one: I, node_two: I) -> None:
        if not self.is_bidirectional_edge(node_one, node_two):
            raise GraphException(f'Bidirectional edge does not exist between nodes {node_one} and {node_two}.')

        node_one: GraphNode[I, T] = self.nodes[node_one]
        node_two: GraphNode[I, T] = self.nodes[node_two]

        node_one.remove_edge(node_two.node_id)
        node_two.remove_edge(node_one.node_id)

    def get_node(self, value: T) -> GraphNode[I, T] | None:
        return self.nodes.get(lambda node: node.value == value, None)
