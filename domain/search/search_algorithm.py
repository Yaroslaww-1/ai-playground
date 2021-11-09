from typing import List, Optional

from domain.enemy.enemy import Enemy
from domain.map import MapTile
from domain.position import Position
from domain.search.graph import Graph


class SearchAlgorithm:
    def __init__(self, map):
        self.map = map
        self.vertices_count = self.get_vertices_count()
        self.initialize_graph()

    def get_vertices_count(self):
        empty_tiles = list(filter(lambda t: t == MapTile.EMPTY, self.map.get_tiles()))
        vertices_count = len(empty_tiles)
        return vertices_count

    def initialize_graph(self):
        graph = Graph(self.vertices_count)
        for x_from in range(0, self.map.width):
            for y_from in range(0, self.map.height):
                for x_to in range(x_from, self.map.width):
                    for y_to in range(y_from, self.map.height):
                        if abs(x_from - x_to) + abs(y_from - y_to) == 1 and \
                                self.map.is_tile_empty(x_from, y_from) and \
                                self.map.is_tile_empty(x_to, y_to):
                            graph.add_undirected_edge(Position(x_from, y_from), Position(x_to, y_to))
        self.graph = graph

    def find_path(
        self,
        starting_position: Position,
        ending_position: Position,
        enemy_positions: Optional[List[Position]] = [],
        avoid_positions: Optional[Position] = None,
    ) -> List[Position]:
        raise NotImplementedError()
