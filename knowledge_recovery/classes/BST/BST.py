from mods import linked_list

class BST():
    def __init__(self):
        self.root = None
    def insert(self, data):
        if self.root is None:
            self.root = Node(data)
        else:
            current = self.root
            while True:
                if current.data.head == data:
                    break
                else:
                    if current.data.head < data:
                        current = current.left
                        


class Node():
    def __init__(self, data):
        self.data = linked_list.LinkedList()
        self.next = None
        self.prev = None

def main():
    bst = BST()

if __name__ == "__main__":
    main()