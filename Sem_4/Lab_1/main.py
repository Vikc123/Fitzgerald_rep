from mods.Graph import Graph, Edge

def read(filename: str) -> Graph:
    g = Graph()
    with open(filename, 'r') as f:
        f.readline()
        for line in f:
            u, v, w = line.split()
            g.add_Vertex(u)
            g.add_Vertex(v)
            g.add_Edge(u, v, int(w))
    return g

def main():
    g = read("data/input")
    g.dfs("B")
    mst = g.prim("B")
    for u, v, w in mst:
        print(f"{u} — {v} (w={w})")

if __name__ == "__main__":
    main()