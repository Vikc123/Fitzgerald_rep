class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
    def append(self, item):
        if self.head is None:
            self.head = Node(item)
            self.tail = self.head
        else:
            current = self.tail
            self.tail.next = Node(item)
            self.tail = self.tail.next
            self.tail.prev = current

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None




def main():
    List = LinkedList()
    collection = [1,2,3,4,5]
    for item in collection:
        List.append(item)
    print(List)

if __name__ == "__main__":
    main()