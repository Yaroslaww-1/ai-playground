from typing import Optional, List

from domain.position import Position
from domain.search.search_algorithm import SearchAlgorithm


class SearchAlgorithmDfs(SearchAlgorithm):
    def __init__(self, map):
        super().__init__(map)

    def find_path(
        self,
        starting_position: Position,
        ending_position: Position,
        enemy_positions: Optional[List[Position]] = [],
        avoid_position: Optional[Position] = None
    ) -> List[Position]:
        # DFS
        stack = [starting_position]
        visited = {starting_position: True}
        parents = {starting_position: None}
        while len(stack) > 0:
            current = stack.pop()  # Take LAST element because it is stack
            for connected_vertex in self.graph.get_vertex_connections(current):
                if visited.get(connected_vertex) is None:
                    visited[connected_vertex] = True
                    parents[connected_vertex] = current
                    stack.append(connected_vertex)

        # Getting path
        path = []
        current = ending_position
        while current is not None:
            path.insert(0, current)
            current = parents.get(current)
        return path
