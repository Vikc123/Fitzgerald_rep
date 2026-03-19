class Node:
    def __init__(self, value):
        self.value = value
        self.next = None
        self.prev = None

class DoubleLinkedList:
    def __init__(self):
        self.head = None
    def insert(self, value):
        new_node = Node(value)
        if not self.head:
            self.head = new_node
            return
        else:
            if value > self.head.value:
                new_node.next = self.head
                self.head.prev = new_node
                self.head = new_node
                return
            current = self.head
            while current.next and value <= current.next.value:
                current = current.next

            new_node.prev = current

            if current.next:
                new_node.next = current.next
                current.next.prev = new_node
                current.next = new_node
                return
            else:
                new_node.prev = current
                current.next = new_node
                return
    def print(self):
        if not self.head:
            print("Пустой список!")
            return
        else:
            currrnt = self.head
            while currrnt:
                print(currrnt.value, end = "<->")
                currrnt = currrnt.next
            return
    def delete(self, target):
        current = self.head
        while current:
            if current.value == target:
                if current == self.head:

                    # self.head = current.next
                    # current.next = None
                    # self.head.prev = None
                    current = current.next
                    continue
                else:
                    current_prev = current.prev
                    if current_prev.prev:
                        current_prev.prev.next = current
                        current.prev = current_prev.prev
                        current_prev.prev = None
                        current_prev.next = None
                        current = current.next
                        continue
                    else:
                        self.head = current
                        current_prev.next = None
                        current.prev = None
                        current = current.next
                        continue
            else:
                current = current.next
                continue

def intersection(list1, list2):
    result = DoubleLinkedList()
    values = set()
    current = list1.head
    while current:
        values.add(current.value)
        current = current.next

    current = list2.head
    while current:
        if current.value in values:
            result.insert(current.value)
        current = current.next
    return result




def main():
    a = DoubleLinkedList()
    a.insert(6)
    a.insert(6)
    a.insert(6)
    a.insert(6)
    a.print()
    print("\n")
    b = DoubleLinkedList()
    b.insert(6)
    b.insert(4)
    b.insert(3)
    b.insert(1)
    b.print()
    print("\n")
    c = DoubleLinkedList()
    c = intersection(a,b)
    c.print()
    # a.delete(6)
    # print("\n")
    # a.print()

if __name__ == '__main__':
    main()