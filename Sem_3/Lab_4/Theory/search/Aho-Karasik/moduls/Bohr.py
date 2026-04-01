def num(c: str) -> int:
    return ord(c) - ord('a')
class Vertex:
    def __init__(self, id, alpha, parent, pchar) -> None:
        self.id = id
        self.next = [None] * alpha
        self.parent = parent
        self.is_terminal = False
        self.pchar = pchar
        self.sufflink = None
        self.go = [None] * alpha

class Trie:
    def __init__(self, alpha):
        self.alpha = alpha
        self.vertices = [Vertex(0, alpha, None, None)]
        self.root = self.vertices[0]

    def size(self) -> "int":
        return len(self.vertices)

    def last(self) -> "Vertex":
        return self.vertices[-1]

    def add(self, s) -> None:
        v = self.root
        for i in range(len(s)):
            if v.next[num(s[i])] is None:
                self.vertices.append(Vertex(self.size(), self.alpha, v, s[i]))
                v.next[num(s[i])] = self.last()
            v = v.next[num(s[i])]
        v.is_terminal = True

    def find(self, s) -> bool:
        v = self.root
        for i in range(len(s)):
            if v.next[num(s[i])] is None:
                return False
            v = v.next[num(s[i])]
        return v.is_terminal

    def get_link(self, v: Vertex) -> "Vertex":
        if v.sufflink is None:
            if v == self.root or v.parent == self.root:
                v.sufflink = self.root
            else:
                v.sufflink = self.go(self.get_link(v.parent), v.pchar)
        return v.sufflink
    def go(self, v: Vertex, c: str) -> Vertex:
        if v.go[num(c)] is None:
            if v.next[num(c)] is not None:
                v.go[num(c)] = v.next[num(c)]
            elif v == self.root:
                v.go[num(c)] = self.root
            else:
                v.go[num(c)] = self.go(self.get_link(v), c)
        return v.go[num(c)]
