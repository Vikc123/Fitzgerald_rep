from dataclasses import dataclass, field
from typing import Any
@dataclass
class Vertex:
    id: int
    data: Any = int

@dataclass
class Edge:
    u: Vertex
    v: Vertex
    w: int
@dataclass
class Graph:
    vertices: list[Vertex] = field(default_factory=list[Vertex])
    edges: list[Edge] = field(default_factory=list[Edge])
    def add_Vertex(self, id: int, data: any) -> None:
        self.vertices.append(Vertex(id, data))

    def add_Edge(self, u: Vertex, v :Vertex, w: int = 1) -> None:
        self.edges.append(Edge(u, v, w))

def main():
    g = Graph()
    g.add_Vertex(0, "A")
    g.add_Vertex(1, "B")
    g.add_Vertex(2, "C")
    g.add_Vertex(3, "D")
    g.add_Vertex(4, "E")
    g.add_Vertex(5, "F")

    g.add_Edge(g.vertices[1], g.vertices[0])
    g.add_Edge(g.vertices[1], g.vertices[2])
    g.add_Edge(g.vertices[2], g.vertices[3])
    g.add_Edge(g.vertices[3], g.vertices[2])
    g.add_Edge(g.vertices[3], g.vertices[4])
    g.add_Edge(g.vertices[3], g.vertices[1])
    g.add_Edge(g.vertices[4], g.vertices[5])
    g.add_Edge(g.vertices[5], g.vertices[1])


if __name__ == "__main__":
    main()