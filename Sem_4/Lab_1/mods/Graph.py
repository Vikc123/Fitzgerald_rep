from dataclasses import dataclass, field
from typing import Any
import heapq
from typing import Tuple

@dataclass
class Edge:
    u: Any
    v: Any
    w: int

@dataclass
class Graph:
    vertices: set = field(default_factory=set)
    edges: list = field(default_factory=list)
    def add_Vertex(self, data: Any):
        self.vertices.add(data)
    def add_Edge(self, u: Any, v: Any, w: int = 1):
        self.edges.append(Edge(u, v, w))
        self.edges.append(Edge(v, u, w))

    def dfs(self, start, visited=None):
        if visited is None:
            visited = set()
        visited.add(start)
        print(start)
        for edge in self.edges:
            if edge.u == start and edge.v not in visited:
                self.dfs(edge.v, visited)

    def prim(self, start: Any) -> list[Tuple[Any, Any, int]]:
        mst = []
        in_mst = set([start])

        candidate_edges = []
        for edge in self.edges:
            if edge.u == start:
                heapq.heappush(candidate_edges, (edge.w, edge.u, edge.v))

        while candidate_edges and len(in_mst) < len(self.vertices):
            weight, u, v = heapq.heappop(candidate_edges)

            if v in in_mst:
                continue

            mst.append((u, v, weight))
            in_mst.add(v)

            for edge in self.edges:
                if edge.u == v and edge.v not in in_mst:
                    heapq.heappush(candidate_edges, (edge.w, edge.u, edge.v))

        return mst