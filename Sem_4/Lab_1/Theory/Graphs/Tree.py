from dataclasses import dataclass, field
from typing import Any

@dataclass
class Vertex:
    id: int
    data: Any = int
    parent: 'Tree' = None
    children: list['Vertex'] = field(default_factory=list['Vertex'])

class Tree:
    def __init__(self, root: Vertex):
        self.root = root
        self.nodes = {root.id: root}
    def add_node(self, parent_id: int, node_id: int, data: Any = None):
        parent = self.nodes[parent_id]

        new_node = Vertex(node_id, data)
        new_node.parent = parent

        parent.children.append(new_node)
        self.nodes[node_id] = new_node

        return new_node



def main():
    root = Vertex(1, "root")
    tree = Tree(root)

    tree.add_node(1, 2, "A")
    tree.add_node(1, 3, "B")
    tree.add_node(2, 4, "C")

if __name__ == "__main__":
    main()