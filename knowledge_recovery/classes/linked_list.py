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

            if self.head.data <= data:
                newNode.next = current
                newNode.prev = current.prev
                current.prev = newNode
                self.head = newNode
                return

            while(current.data > data and current.next is not None):
                current = current.next

            if current.data <= data:
                newNode.next = current
                newNode.prev = current.prev
                current.prev.next = newNode
                current.prev = newNode

            else:
                newNode.prev = current
                current.next = newNode
                self.tail = newNode

    def del_before(self, target):
        current = self.head
        while(True):
            if current.data == target and current.prev is not None:
                current.prev.prev = current.next
                # curre



class Node():
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None


def main():
    List = LinList()
    a = [1,1,0,8,2,0,0,6]
    for i in a:
        List.append(i)
    print("done")

if __name__ == "__main__":
    main()