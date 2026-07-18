from Sem_3.Lab_1.main import Node


class LinList():
    def __init__(self):
        self.head = None
        self.tail = None
    def append(self, data):
        if self.head is None:
            self.head = Node(data)
            self.tail = self.head
        else:
            current = self.head
            newNode = Node(data)

            while(current.data > data and current.next is not None):
                current = current.next

            if self.head.data <= data:
                newNode.next = current
                current.prev = newNode
                newNode.next = current
                self.head = newNode

            newNode.prev = current
            current.next = newNode
            self.tail = newNode


class Node():
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None


def main():
    List = LinList()
    a = [10, 3, 7]
    for i in a:
        List.append(i)
    print("done")

if __name__ == "__main__":
    main()