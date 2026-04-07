from dataclasses import dataclass, field
from typing import Any

@dataclass
class Vertex:
    id: int
    data: Any = None

@dataclass
class Edge:
    u: Vertex
    v: Vertex
    w: int

@dataclass
class Graph:
    vertices: list[Vertex] = field(default_factory=list[Vertex])
    edges: list[Edge] = field(default_factory=list[Vertex])
    def add_Vertex(self, id: int, data: any):
        self.vertices.append(Vertex(id, data))
    def add_Edge(self, u: Vertex, v: Vertex, w: int = 1):
        self.edges.append(Edge(u, v, w))
        self.edges.append(Edge(v, u, w))

def create_complete_underected_graph(n: int) -> Graph:
    g = Graph()
    for i in range(n):
        g.add_Vertex(i, chr(ord('a')+i))
    for i in range(n):
        for j in range(i+1, n):
            g.add_Edge(g.vertices[i], g.vertices[j])
    return g


def main():
    g = create_complete_underected_graph(5)
if __name__ == "__main__":
    main()