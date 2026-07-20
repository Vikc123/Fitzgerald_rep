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
        while(current is not None):
            if current.next is not None and current.next.data == target and current is self.head:
                self.head = current.next
                current = current.next
                self.head.prev = None
                continue
            elif current.next is not None and current.next.data == target and current.prev is not None:
                to_del = current
                current.prev.next = current.next
                current.next.prev = current.prev
                current = current.next
                del to_del
                continue
            elif current.data == target and current is self.head:
                if current.prev is not None and current.prev.prev is not None:
                    to_del = current.prev
                    current.prev = to_del.prev
                    to_del.prev.next = current
                    del to_del
                    break
                elif current.prev is not None:
                    del current.prev
                    break
                elif self.head == self.tail:
                    break
            elif current.next is not None:
                current = current.next
                continue
            break

class Node():
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None

