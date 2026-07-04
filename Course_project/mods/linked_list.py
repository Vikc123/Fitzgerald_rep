class ListNode:
    def __init__(self, data):
        self.data = data
        self.next = None


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

        self.tail.next = node
        self.tail = node
        self.size += 1

    def remove_by_reference(self, data):
        previous = None
        current = self.head

        while current is not None:
            if current.data is data:
                if previous is None:
                    self.head = current.next
                else:
                    previous.next = current.next

                if current is self.tail:
                    self.tail = previous

                self.size -= 1
                return True

            previous = current
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