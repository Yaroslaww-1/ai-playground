import queue
from typing import List, Optional

from domain.enemy.enemy import Enemy
from domain.position import Position
from domain.search.search_algorithm import SearchAlgorithm


class VertexWithAStarInfo:
    def __init__(self, parent: Optional["VertexWithAStarInfo"], position: "Position"):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

    def __lt__(self, other):
        return self.f <= other.f


class SearchAlgorithmAstar(SearchAlgorithm):
    def __init__(self, map):
        super().__init__(map)

    def find_path(
        self,
        starting_position: Position,
        ending_position: Position,
        enemy_positions: Optional[List[Position]] = [],
        avoid_position: Optional[Position] = None
    ):
        start_vertex = VertexWithAStarInfo(None, starting_position)
        end_vertex = VertexWithAStarInfo(None, ending_position)
        avoid_positions = enemy_positions

        open_vertices = queue.PriorityQueue()
        open_vertices.put(start_vertex)
        visited_positions = {start_vertex.position: True}

        while not open_vertices.empty():
            current_vertex = open_vertices.get()
            visited_positions[current_vertex.position] = True

            if current_vertex == end_vertex:
                path = []
                while current_vertex is not None:
                    path.append(current_vertex.position)
                    current_vertex = current_vertex.parent
                return path[::-1]

            open_vertices_to_current = []
            for opened_direction in self.map.get_all_opened_directions(current_vertex.position.x, current_vertex.position.y):
                next_position = self.map.get_next_position_in_direction(current_vertex.position.x, current_vertex.position.y, opened_direction)
                if next_position is None:
                    continue

                new_vertex = VertexWithAStarInfo(current_vertex, next_position)
                open_vertices_to_current.append(new_vertex)

            for open_vertex in open_vertices_to_current:
                if visited_positions.get(open_vertex.position) is not None:
                    continue
                open_vertex.g = current_vertex.g + 1
                euclidean_heuristic = self.get_euclidean_distance(open_vertex.position, end_vertex.position)
                distance_to_closest_avoid_position = self.get_euclidean_distance(open_vertex.position, self.get_closest_avoid_position(starting_position, avoid_positions))
                avoid_positions_sensing_heuristic = (self.map.width * self.map.height - distance_to_closest_avoid_position) * 5
                open_vertex.h = euclidean_heuristic + avoid_positions_sensing_heuristic
                open_vertex.f = open_vertex.g + open_vertex.h

                open_vertices.put(open_vertex)

    def get_euclidean_distance(self, position1: Position, position2: Position):
        return (position1.x - position2.x) ** 2 + (position1.y - position2.y) ** 2

    def get_closest_avoid_position(self, current_position: Position, avoid_positions: List[Position]) -> Position:
        min_dist = self.get_euclidean_distance(current_position, avoid_positions[0])
        min_dist_position = avoid_positions[0]

        for avoid_position in avoid_positions:
            dist = self.get_euclidean_distance(current_position, avoid_position)
            if dist < min_dist:
                min_dist = dist
                min_dist_position = avoid_position

        return min_dist_position
