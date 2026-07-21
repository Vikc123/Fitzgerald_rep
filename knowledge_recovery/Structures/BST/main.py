from mods import generator as gt
class Tree:
    def __init__(self):
        self.root = None

    def insert(self, root, current):
        if root is None:
            self.root = current
            return
        else:
            if current.data < root.data:
                root.left = self.insert(root.left, current)
                current.parrent = root
                return current
            elif current.data > root.data:
                root.right = self.insert(root.right, current)
                current.parrent = root
                return current


class Node():
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None
        self.parent = None

def main():
    # gt.generate_file('data/bst.txt', 10)
    t = Tree()
    t.insert(t.root, Node(2))
    t.insert(t.root, Node(3))
    t.insert(t.root, Node(1))

if __name__ == '__main__':
    main()