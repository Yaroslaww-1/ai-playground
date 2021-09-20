from timeit import default_timer as timer

from domain.map import MapTile
from domain.position import Position
from domain.search.graph import Graph


class Search:
    def __init__(self, map):
        self.map = map
        self.vertices_count = self.get_vertices_count()
        self.graph = self.get_graph()
        self.start_time = None
        self.last_search_time = 0

    def get_vertices_count(self):
        empty_tiles = list(filter(lambda t: t == MapTile.EMPTY, self.map.tiles))
        vertices_count = len(empty_tiles)
        return vertices_count

    def get_graph(self):
        graph = Graph(self.vertices_count)
        for x_from in range(0, self.map.width):
            for y_from in range(0, self.map.height):
                for x_to in range(x_from, self.map.width):
                    for y_to in range(y_from, self.map.height):
                        if abs(x_from - x_to) + abs(y_from - y_to) == 1 and \
                                self.map.is_tile_empty(x_from, y_from) and \
                                self.map.is_tile_empty(x_to, y_to):
                            graph.add_undirected_edge(Position(x_from, y_from), Position(x_to, y_to))
        return graph

    def bfs(self, starting_vertex, ending_vertex):
        self.start_timer()

        queue = [starting_vertex]
        visited = {starting_vertex: True}
        parents = {starting_vertex: None}
        while len(queue) > 0:
            current = queue.pop(0)
            for connected_vertex in self.graph.get_vertex_connections(current):
                if visited.get(connected_vertex) is None:
                    visited[connected_vertex] = True
                    parents[connected_vertex] = current
                    queue.append(connected_vertex)

        self.end_timer()
        return self.get_path(parents, ending_vertex)

    def get_path(self, parents, ending_vertex):
        path = []
        current = ending_vertex
        while current is not None:
            path.insert(0, current)
            current = parents.get(current)
        return path

    def start_timer(self):
        self.start_time = timer()

    def end_timer(self):
        self.last_search_time = round((timer() - self.start_time) * 1000, 2)
