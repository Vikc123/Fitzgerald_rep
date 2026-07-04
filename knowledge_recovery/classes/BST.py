class node:
    def __init__(self, value: int):
        self.value = None
        self.left = None
        self.right = None

class bst:
    def __init__(self):
        self.top = None

    def insert(self, value):
        if self.top is None:
            self.top = node(value)



def main():
    pass

if __name__ == "__main__":
    main()