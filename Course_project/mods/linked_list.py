class ListNode:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None


class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def append(self, data):
        node = ListNode(data)

        if self.head is None:
            self.head = node
            self.tail = node
            self.size += 1
            return

        node.prev = self.tail
        self.tail.next = node
        self.tail = node
        self.size += 1

    def remove_by_reference(self, data):
        current = self.head

        while current is not None:
            if current.data is data:
                if current.prev is None:
                    self.head = current.next
                else:
                    current.prev.next = current.next

                if current.next is None:
                    self.tail = current.prev
                else:
                    current.next.prev = current.prev

                self.size -= 1
                return True

            current = current.next

        return False

    def is_empty(self):
        return self.size == 0

    def __len__(self):
        return self.size

    def __iter__(self):
        current = self.head

        while current is not None:
            yield current.data
            current = current.next