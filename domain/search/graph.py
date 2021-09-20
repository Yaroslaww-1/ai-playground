class Graph:
    def __init__(self, vertices_count):
        self.vertices = {0:[]}

    def add_undirected_edge(self, _from, to):
        self.add_directed_edge(_from, to)
        self.add_directed_edge(to, _from)

    def add_directed_edge(self, _from, to):
        if self.vertices.get(_from) is not None:
            if self.vertices[_from].count(to) == 0:
                self.vertices[_from].append(to)
        else:
            self.vertices[_from] = [to]

    def get_vertex_connections(self, vertex):
        if vertex in self.vertices:
            return self.vertices[vertex]
        else:
            return []
